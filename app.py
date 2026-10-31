import base64
import html
import io
from collections import OrderedDict
from pathlib import Path

import pandas as pd
import streamlit as st
from PIL import Image, ImageOps

from inventory_data import DETAILS, RECEIPTS

BASE = Path(__file__).parent
IMG_EXTS = (".jpg", ".jpeg", ".png", ".webp")

st.set_page_config(page_title="My Inventory", page_icon="👗", layout="wide")


# ---------- build the product list from the receipts ----------
def photo_path(code: str) -> Path | None:
    custom = DETAILS.get(code, {}).get("photo", "")
    if custom and (BASE / custom).exists():
        return BASE / custom
    folder = BASE / "images"
    if folder.exists():
        for f in folder.iterdir():
            if f.stem == code and f.suffix.lower() in IMG_EXTS:
                return f
    return None


@st.cache_data
def thumb_uri(path: str, mtime: float) -> str:
    img = Image.open(path).convert("RGB")
    img = ImageOps.pad(img, (240, 240), color=(245, 245, 245))
    buf = io.BytesIO()
    img.save(buf, "JPEG", quality=80)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


def build_products() -> pd.DataFrame:
    agg: "OrderedDict[str, dict]" = OrderedDict()
    for r in RECEIPTS:
        for code, name, qty, paid, listed in r["items"]:
            p = agg.setdefault(
                code,
                dict(code=code, name=name, qty=0, spent=0, list_price=listed,
                     brand=r["brand"], store=r["store"], date=r["date"], receipt=r["receipt_no"]),
            )
            p["qty"] += qty
            p["spent"] += qty * paid
            if r["date"] > p["date"]:
                p["date"] = r["date"]
    rows = []
    for code, p in agg.items():
        d = DETAILS.get(code, {})
        rows.append(
            dict(
                code=code,
                name=p["name"],
                color=d.get("color", ""),
                size=d.get("size", ""),
                qty=p["qty"],
                price=round(p["spent"] / p["qty"]),
                list_price=p["list_price"],
                brand=p["brand"],
                store=p["store"],
                date=p["date"],
                receipt=p["receipt"],
                photo=photo_path(code),
            )
        )
    return pd.DataFrame(rows)


df = build_products()

# ---------- sidebar ----------
st.sidebar.header("Filters")
brands = st.sidebar.multiselect("Brand", sorted(df["brand"].unique()), default=sorted(df["brand"].unique()))
search = st.sidebar.text_input("Search name / color / size / code")
sort_by = st.sidebar.selectbox("Sort by", ["Newest purchase", "Name A–Z", "Price high → low", "Price low → high", "Quantity"])
view = st.sidebar.radio("View", ["Gallery", "Table"], horizontal=True)
cols_n = st.sidebar.slider("Gallery columns", 2, 6, 4) if view == "Gallery" else 4

f = df[df["brand"].isin(brands)]
if search:
    s = search.lower()
    f = f[f.apply(lambda r: s in f"{r['name']} {r['color']} {r['size']} {r['code']}".lower(), axis=1)]
f = {
    "Newest purchase": f.sort_values(["date", "name"], ascending=[False, True]),
    "Name A–Z": f.sort_values("name"),
    "Price high → low": f.sort_values("price", ascending=False),
    "Price low → high": f.sort_values("price"),
    "Quantity": f.sort_values("qty", ascending=False),
}[sort_by]

# ---------- header ----------
st.title("👗 My Inventory")
m1, m2, m3, m4 = st.columns(4)
m1.metric("Products", len(f))
m2.metric("Total pieces", int(f["qty"].sum()))
m3.metric("Total spent", f"¥{int((f['price'] * f['qty']).sum()):,}")
m4.metric("Photos added", f"{f['photo'].notna().sum()} / {len(f)}")

missing = int(((df["color"] == "") | (df["size"] == "")).sum())
if missing:
    st.info(f"{missing} products still need a color or size — fill them in `inventory_data.py`.", icon="✏️")

# ---------- gallery ----------
if view == "Gallery":
    st.markdown(
        """
        <style>
        .inventory-card{height:100%;display:flex;flex-direction:column;margin-bottom:16px;padding:12px;border:1px solid rgba(128,128,128,.25);border-radius:12px}
        .inventory-photo{width:100%;aspect-ratio:1/1;display:flex;align-items:center;justify-content:center;overflow:hidden;border-radius:8px;background:rgba(128,128,128,.12);color:gray;font-size:.85rem}
        .inventory-photo img{display:block;width:100%;height:100%;object-fit:contain}
        .inventory-name{height:3em;margin:12px 0 4px;overflow:hidden;display:-webkit-box;-webkit-box-orient:vertical;-webkit-line-clamp:2;line-height:1.5em;font-weight:600}
        .inventory-detail{height:1.5em;overflow:hidden;color:rgba(128,128,128,.95);font-size:.85rem;white-space:nowrap;text-overflow:ellipsis}
        .inventory-price{height:1.8em;margin:8px 0 4px}
        </style>
        """,
        unsafe_allow_html=True,
    )
    rows = [f.iloc[i : i + cols_n] for i in range(0, len(f), cols_n)]
    for chunk in rows:
        cols = st.columns(cols_n, gap="large")
        for col, (_, p) in zip(cols, chunk.iterrows()):
            with col:
                photo = (
                    f"<img src='{thumb_uri(str(p['photo']), p['photo'].stat().st_mtime)}' "
                    f"alt='{html.escape(str(p['name']), quote=True)}'>"
                    if p["photo"] is not None
                    else "No photo yet"
                )
                price_txt = f"¥{p['price']:,}"
                if p["price"] < p["list_price"]:
                    price_txt += f"  <del>¥{p['list_price']:,}</del>"
                card = (
                    "<div class='inventory-card'>"
                    f"<div class='inventory-photo'>{photo}</div>"
                    f"<div class='inventory-name'>{html.escape(str(p['name']))}</div>"
                    f"<div class='inventory-detail'>Color: {html.escape(str(p['color'] or '—'))}"
                    f" · Size: {html.escape(str(p['size'] or '—'))}</div>"
                    f"<div class='inventory-price'>{price_txt} · <strong>Qty {int(p['qty'])}</strong></div>"
                    f"<div class='inventory-detail'>{html.escape(str(p['brand']))}"
                    f" · {html.escape(str(p['date'])[:10])}</div>"
                    "</div>"
                )
                st.markdown(card, unsafe_allow_html=True)

# ---------- table ----------
else:
    t = pd.DataFrame(
        {
            "Photo": [thumb_uri(str(x), x.stat().st_mtime) if x is not None else None for x in f["photo"]],
            "Color": f["color"],
            "Name": f["name"],
            "Size": f["size"],
            "Quantity": f["qty"],
            "Price (¥)": f["price"],
            "Brand": f["brand"],
            "Date": f["date"].str[:10],
            "Code": f["code"],
        }
    )
    st.dataframe(
        t,
        hide_index=True,
        width="stretch",
        row_height=70,
        column_config={
            "Photo": st.column_config.ImageColumn("Photo", width="small"),
            "Price (¥)": st.column_config.NumberColumn(format="¥%d"),
        },
    )
    st.download_button("⬇️ Download CSV", t.drop(columns="Photo").to_csv(index=False).encode("utf-8-sig"), "inventory.csv", "text/csv")

# ---------- receipts ----------
with st.expander("🧾 Receipts included"):
    st.dataframe(
        pd.DataFrame(
            [
                dict(Receipt=r["receipt_no"], Store=r["store"], Date=r["date"],
                     Pieces=sum(i[2] for i in r["items"]), Total=f"¥{r['total']:,}")
                for r in RECEIPTS
            ]
        ),
        hide_index=True,
        width="stretch",
    )
