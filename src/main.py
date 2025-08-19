import argparse
import pathlib
import importlib

from .llm import parse_user_query
from .parsers import route
from .mcp_browser import MCPBrowser
from .report import build_excel
from .utils import slugify


SCRAPER_MAP = {
    "amazon": ".scrapers.amazon.AmazonScraper",
    "flipkart": ".scrapers.flipkart.FlipkartScraper",
    "flights": ".scrapers.cleartrip.CleartripScraper",   # ✈️ flights ke liye Cleartrip
}


def _get_scraper(name, browser):
    qual = SCRAPER_MAP[name]  # e.g. ".scrapers.cleartrip.CleartripScraper"
    module_path, cls_name = qual.rsplit(".", 1)

    # NOTE: supply `package=__package__` so ".scrapers.…" is resolved
    module = importlib.import_module(module_path, package=__package__)
    cls = getattr(module, cls_name)

    return cls(browser)   # ✅ sirf browser dena hai


def run(query: str, headless=True):
    parsed = parse_user_query(query)
    jobs = route(parsed)
    slug = slugify(query)
    data_frames = []

    with MCPBrowser(headless=headless) as browser:
        for job in jobs:
            scraper = _get_scraper(job["site"], browser)
            scraper.run(**job)   # ✅ origin, destination, date yahan jayenge

            if hasattr(scraper, "get_data"):
                df = scraper.get_data()
            elif hasattr(scraper, "save_csv"):
                df = scraper.save_csv(slug)
            else:
                raise AttributeError("Scraper must define get_data() or save_csv()")

            # ✅ Add model name (e.g. "iPhone 15") only for product scrapes
            if parsed.get("type") == "product" and "title" in df.columns:
                df["model"] = df["title"].str.lower().str.extract(
                    r"(iphone.*?\d{1,2})", expand=False
                )

            df.attrs["sheet"] = job["site"][:31]
            data_frames.append(df)

    # 📜 Build final report
    report_path = build_excel(data_frames, parsed, f"{slug}.xlsx")
    print("✅ Report written:", report_path)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="AI-powered scraper")
    ap.add_argument("query", help="Natural language query")
    ap.add_argument(
        "--show", action="store_false", dest="headless", help="Show browser for debugging"
    )
    args = ap.parse_args()
    run(args.query, headless=args.headless)
