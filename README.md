# Scrape AI Agent

🚀 An AI-powered scraping agent that understands **natural language queries** and extracts structured data (flights, e-commerce products, etc.) from different websites.

---

## ✨ Features
- 📝 **Natural Language Queries** – Just type what you want, e.g.:
  ```bash
  python -m src.main "flights from BOM to GOI on 2025-08-20" --show
🌐 Multi-site Scraping – Currently supports:

✈️ Cleartrip (Flights)

🛒 Amazon

🛍️ Flipkart

👀 Headless or Visible Mode – Debug with --show or run silently.

📊 Excel & CSV Reports – Data is automatically saved inside the outputs/ folder.

⚡ Modular Design – Add new scrapers easily.

## 📂 Project Structure

```bash
scrape_ai_agent/
├── outputs/                 # 📊 Generated CSV/XLSX reports
├── src/
│   ├── __init__.py
│   ├── main.py              # 🚀 Entry point (parses query, routes scraper, builds report)
│   ├── base.py              # 🏗️ Abstract BaseScraper class
│   ├── utils.py             # 🔧 Utility functions (slugify, helpers)
│   ├── llm.py               # 🧠 Parses natural language queries
│   ├── parsers.py           # 📌 Routes parsed query to correct scraper
│   ├── report.py            # 📑 Builds Excel reports
│   ├── mcp_browser.py       # 🌐 Browser wrapper (Playwright)
│   └── scrapers/            # 🕸️ Individual scrapers
│       ├── __init__.py
│       ├── amazon.py        # 🛒 Amazon scraper
│       ├── flipkart.py      # 🛍️ Flipkart scraper
│       └── cleartrip.py     # ✈️ Cleartrip flight scraper
├── requirements.txt         # 📦 Dependencies
└── README.md                # 📘 Project documentation
```
⚙️ Installation
Clone the repo and install dependencies:

```bash
Copy
Edit
git clone https://github.com/vikshittindwani/scrape_ai_agent.git
cd scrape_ai_agent
pip install -r requirements.txt

```
🚀 Usage
Run with a natural language query:

```bash
Copy
Edit
# Example: Flight Search
python -m src.main "flights from BOM to GOI on 2025-08-20"
```

# Example: With visible browser (debug mode)
python -m src.main "amazon iphone 15" --show
## 📂 Results will be saved in outputs/.

## 🔧 How It Works
>Parse query → (parse_user_query) extracts type, origin, destination, date, etc.

>Route job → (route()) decides which scraper to call.

>Scraper execution → Instantiates scraper class (CleartripScraper, AmazonScraper, etc.).

>Data collection → Extracts flights/products.

>Export → Saves into CSV/Excel via pandas.

## 🤝 Contributing
>Contributions are welcome! 🎉

>Add support for more websites

>Improve error handling

>Enhance natural language parsing

## Steps:

>Fork this repo

>Create a new branch (feature-xyz)

>Commit changes

>Submit a PR 🚀

## 📜 License
This project is licensed under the MIT License.

!<img width="1920" height="1080" alt="Screenshot (77)" src="https://github.com/user-attachments/assets/7f3501ee-364b-4d3e-a511-4b93fed7a214" />
!<img width="1920" height="1080" alt="Screenshot (78)" src="https://github.com/user-attachments/assets/2dc51316-e826-4c9e-b87c-b8158e5b27c5" />

