# Clothing Inventory Automation

A soft, boutique-style inventory manager built with Streamlit. Track clothing
products and photos, stock, purchases, sales, expenses, and pricing from one
dashboard.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

On Windows, activate the environment with `.venv\Scripts\activate`.

## Deploy to Streamlit Community Cloud

1. Push this repository to GitHub.
2. In [Streamlit Community Cloud](https://share.streamlit.io/), choose **Create app**.
3. Select this repository, the `main` branch, and `app.py` as the main file.
4. Deploy. Streamlit installs the packages listed in `requirements.txt`.

### Optional receipt scanning

Receipt scanning uses the Anthropic API. Add the key in the app's Streamlit
Cloud **Settings → Secrets**:

```toml
ANTHROPIC_API_KEY = "your-api-key"
```

The API key is not stored in the repository. Without it, the app still supports
manual product entry and all inventory, pricing, sales, and expense features.

## Data storage

The app stores its SQLite database in `clothing_inventory.db` beside `app.py`.
For local use, that database persists between runs. Streamlit Community Cloud
does not provide durable local disk storage for production data; connect a
managed database before relying on Cloud deployments for long-term records.
Set `CLOTHING_DB_PATH` to change the SQLite file location when running locally.
