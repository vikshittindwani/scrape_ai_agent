from abc import ABC, abstractmethod
from ..utils import slugify
import pandas as pd, pathlib

class BaseScraper(ABC):
    SITE = "base"

    def __init__(self, browser):
        self.browser = browser
        self.data = []

    @abstractmethod
    def run(self, **params): ...

    def save_csv(self, query_slug):
        if not self.data:
            print(f"⚠️ No data scraped for {self.SITE}, skipping CSV.")
            return pd.DataFrame()

        df = pd.DataFrame(self.data)
        df.attrs["sheet"] = self.SITE
        path = pathlib.Path("outputs")
        path.mkdir(parents=True, exist_ok=True)
        out_file = path / f"{self.SITE}_{query_slug}.csv"
        df.to_csv(out_file, index=False)
        print(f"✅ CSV saved: {out_file}")
        return df
