"""
YOUR PRODUCT DATA  --  edit this file, no database needed.

1) Fill in COLOR and SIZE for each product in DETAILS (receipts don't print them).
2) Add photos later: drop a file named after the product code into the `images/` folder,
   e.g. images/2200079328649.jpg   (.jpg / .jpeg / .png / .webp all work).
   Or point to a photo yourself with "photo": "images/anything.jpg" in DETAILS.
"""

# ---------------------------------------------------------------------------
# Color / size per product code.  Fill the empty strings in.
# ---------------------------------------------------------------------------
DETAILS = {
    "2200079328649": {"color": "", "size": "", "photo": ""},  # Double-layered corduroy coat
    "2200083187959": {"color": "", "size": "", "photo": ""},  # Double Metal Button Cardigan
    "2200082429869": {"color": "Black", "size": "S", "photo": "img/2200082429869.png"},  # W Bra Feel Lace Tank Top
    "2200083377817": {"color": "", "size": "", "photo": ""},  # W Satin Dot Flare Skirt
    "2200082907190": {"color": "", "size": "", "photo": ""},  # Double-breasted front button sweater
    "2200082126645": {"color": "", "size": "", "photo": ""},  # W Satin Dot Flare Skirt
    "2200083187881": {"color": "", "size": "", "photo": ""},  # Double Metal Button Cardigan
    "2200083200030": {"color": "", "size": "", "photo": ""},  # W Bra Feel Lace Tank Top
    "2200082429791": {"color": "", "size": "", "photo": ""},  # W Bra Feel Lace Tank Top
    "2200079948434": {"color": "", "size": "", "photo": ""},  # Double-layered openwork knit cardigan
    "2200082429876": {"color": "Black", "size": "M", "photo": "img/2200082429869.png"},  # W Bra Feel Lace Tank Top
    "2200082907404": {"color": "", "size": "", "photo": ""},  # Double-breasted front button sweater
    "2200079948496": {"color": "", "size": "", "photo": ""},  # Double-layered openwork knit cardigan
    "2200080457680": {"color": "", "size": "", "photo": ""},  # W-Scalloped Mini Camisole Tunic
    "2200082126638": {"color": "", "size": "", "photo": ""},  # W Satin Dot Flare Skirt
    "2200079328632": {"color": "", "size": "", "photo": ""},  # Double Corduroy Coat
    "2200082429807": {"color": "Off White", "size": "M", "photo": "img/2200082429807.png"},  # W Bra Feel Lace Tank Top
    "2200082907336": {"color": "", "size": "", "photo": ""},  # Double-breasted front button sweater
    "2200082927044": {"color": "", "size": "", "photo": ""},  # Double-ribbed boat neck cardigan
    "2200082926832": {"color": "", "size": "", "photo": ""},  # Double-ribbed boat neck cardigan
    "2200082926900": {"color": "", "size": "", "photo": ""},  # Double-ribbed boat neck cardigan
    "2200082907268": {"color": "", "size": "", "photo": ""},  # Double-breasted front button sweater
    "2200082926979": {"color": "", "size": "", "photo": ""},  # Double-ribbed boat neck cardigan
    "2200083188246": {"color": "", "size": "", "photo": ""},  # Double Crew Neck Sweater
    "2000211226457": {"color": "", "size": "", "photo": ""},  # Double-breasted bootcut jeans
    "2000223607428": {"color": "", "size": "", "photo": ""},  # Double Jersey Barrel Leg Pants
    "2000217468141": {"color": "", "size": "", "photo": ""},  # Washable Milano Rib Knit T-shirt
    "2000224036081": {"color": "Off White", "size": "XL", "photo": "img/2000224036081.png"},  # Double Ribbed Henry Neck T-shirt
    "2000215227634": {"color": "", "size": "", "photo": ""},  # Cargo shorts
    "2000205690073": {"color": "", "size": "", "photo": ""},  # Double Heattech Tights
    "2000217997917": {"color": "", "size": "", "photo": ""},  # Crewneck T-shirt
    "2000217997894": {"color": "", "size": "", "photo": ""},  # Crewneck T-shirt
    "2000223047958": {"color": "", "size": "", "photo": ""},  # Washable Milano Rib Knit T-shirt
    "2000200542186": {"color": "", "size": "", "photo": ""},  # AIRism Cotton Kanoko Polo Shirt
    "2000221120004": {"color": "", "size": "", "photo": ""},  # Cargo shorts
    "2000217997900": {"color": "", "size": "", "photo": ""},  # Crewneck T-shirt
    "2000194175193": {"color": "", "size": "", "photo": ""},  # Double-washable knit ribbed pants
    "2000221120318": {"color": "", "size": "", "photo": ""},  # Cargo shorts
    "2000219787301": {"color": "", "size": "", "photo": ""},  # W-Shearing T/N
    "2000215227627": {"color": "", "size": "", "photo": ""},  # Cargo shorts
    "2000217014294": {"color": "Navy", "size": "S", "photo": "img/2000217014294.png"},  # Double Crepe Jersey Bra Top
    "2000217014157": {"color": "", "size": "", "photo": ""},  # Double Crepe Jersey Bra Top
    "2000211703750": {"color": "", "size": "", "photo": ""},  # AIRism Cotton Kanoko Polo Shirt
}

# ---------------------------------------------------------------------------
# Receipt lines, copied from your 3 PDFs.
# item = (product code, name, qty, price paid per unit, list price per unit)
# Discounts printed on the receipt are already applied to "price paid".
# ---------------------------------------------------------------------------
RECEIPTS = [
    {
        "receipt_no": "0623-2026-09-12-52-0096",
        "brand": "GU",
        "store": "GU Frespo Sendai Store",
        "date": "2026-09-12 16:37",
        "total": 15230,
        "items": [
            ('2200079328649', 'Double-layered corduroy coat', 1, 790, 790),
            ('2200083187959', 'Double Metal Button Cardigan', 1, 1490, 1490),
            ('2200082429869', 'W Bra Feel Lace Tank Top', 1, 790, 790),
            ('2200083377817', 'W Satin Dot Flare Skirt', 1, 990, 990),
            ('2200082907190', 'Double-breasted front button sweater', 1, 590, 590),
            ('2200082126645', 'W Satin Dot Flare Skirt', 1, 990, 990),
            ('2200083187881', 'Double Metal Button Cardigan', 1, 1490, 1490),
            ('2200083200030', 'W Bra Feel Lace Tank Top', 1, 790, 790),
            ('2200082429791', 'W Bra Feel Lace Tank Top', 1, 790, 790),
            ('2200079948434', 'Double-layered openwork knit cardigan', 1, 790, 790),
            ('2200082429876', 'W Bra Feel Lace Tank Top', 1, 790, 790),
            ('2200082907404', 'Double-breasted front button sweater', 1, 590, 590),
            ('2200079948496', 'Double-layered openwork knit cardigan', 1, 790, 790),
            ('2200080457680', 'W-Scalloped Mini Camisole Tunic', 1, 990, 990),
            ('2200082126638', 'W Satin Dot Flare Skirt', 1, 990, 990),
            ('2200079328632', 'Double Corduroy Coat', 1, 790, 790),
            ('2200082429807', 'W Bra Feel Lace Tank Top', 1, 790, 790),
        ],
    },
    {
        "receipt_no": "0623-2026-10-12-53-0013",
        "brand": "GU",
        "store": "GU Frespo Sendai Store",
        "date": "2026-10-12 11:59",
        "total": 5330,
        "items": [
            ('2200082907336', 'Double-breasted front button sweater', 1, 590, 590),
            ('2200082927044', 'Double-ribbed boat neck cardigan', 1, 990, 990),
            ('2200082926832', 'Double-ribbed boat neck cardigan', 1, 990, 990),
            ('2200082926900', 'Double-ribbed boat neck cardigan', 1, 990, 990),
            ('2200082907268', 'Double-breasted front button sweater', 1, 590, 590),
            ('2200082926979', 'Double-ribbed boat neck cardigan', 1, 590, 590),
            ('2200083188246', 'Double Crew Neck Sweater', 1, 590, 590),
        ],
    },
    {
        "receipt_no": "0582-2026-09-12-32-0026",
        "brand": "UNIQLO",
        "store": "Uniqlo Wakabayashi Arai Store",
        "date": "2026-09-12 11:29",
        "total": 22990,
        "items": [
            ('2000211226457', 'Double-breasted bootcut jeans', 1, 990, 990),
            ('2000223607428', 'Double Jersey Barrel Leg Pants', 1, 3990, 3990),
            ('2000211226457', 'Double-breasted bootcut jeans', 1, 990, 990),
            ('2000217468141', 'Washable Milano Rib Knit T-shirt', 1, 1490, 2990),
            ('2000224036081', 'Double Ribbed Henry Neck T-shirt', 1, 990, 1990),
            ('2000215227634', 'Cargo shorts', 1, 990, 990),
            ('2000205690073', 'Double Heattech Tights', 1, 390, 390),
            ('2000217997917', 'Crewneck T-shirt', 1, 790, 790),
            ('2000217997894', 'Crewneck T-shirt', 1, 790, 790),
            ('2000223047958', 'Washable Milano Rib Knit T-shirt', 1, 990, 2990),
            ('2000200542186', 'AIRism Cotton Kanoko Polo Shirt', 1, 790, 790),
            ('2000205690073', 'Double Heattech Tights', 1, 390, 390),
            ('2000221120004', 'Cargo shorts', 1, 990, 990),
            ('2000217997900', 'Crewneck T-shirt', 1, 790, 790),
            ('2000194175193', 'Double-washable knit ribbed pants', 1, 1290, 1290),
            ('2000221120318', 'Cargo shorts', 1, 990, 990),
            ('2000219787301', 'W-Shearing T/N', 1, 990, 990),
            ('2000215227627', 'Cargo shorts', 1, 990, 990),
            ('2000217014294', 'Double Crepe Jersey Bra Top', 1, 1290, 1290),
            ('2000217014157', 'Double Crepe Jersey Bra Top', 1, 1290, 1290),
            ('2000211703750', 'AIRism Cotton Kanoko Polo Shirt', 1, 790, 790),
        ],
    },
]
