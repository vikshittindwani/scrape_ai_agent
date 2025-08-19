from playwright.sync_api import sync_playwright
import contextlib, time

class MCPBrowser:
    def __init__(self, headless: bool = True):
        self._p = sync_playwright().start()
        self.browser = self._p.chromium.launch(headless=headless)
        self.page = self.browser.new_page(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/115.0.0.0 Safari/537.36"
            )
        )

    # ――― enhanced navigate with retries ―――
    def navigate(self, url):
        for attempt in range(3):
            try:
                print(f"🌍 Navigating to {url} (Attempt {attempt + 1}/3)")
                self.page.goto(url, timeout=60000, wait_until="domcontentloaded")
                print("✅ Page loaded successfully")
                return
            except Exception as e:
                print(f"⚠️ Attempt {attempt + 1} failed: {e}")
                if attempt == 2:
                    self.page.screenshot(path=f"error_screenshot_attempt_{attempt+1}.png")
                    raise e
                time.sleep(2)

    def fill(self, selector, text):
        self.page.fill(selector, text, timeout=30000)

    def click(self, selector):
        self.page.click(selector, timeout=30000)

    def select(self, selector, value):
        self.page.select_option(selector, value, timeout=30000)

    def wait(self, ms=3000):
        time.sleep(ms / 1000)

    def press(self, selector, key):
        self.page.locator(selector).press(key, timeout=30000)

    def text(self, selector):
        return self.page.inner_text(selector, timeout=30000)

    def screenshot(self, path):
        self.page.screenshot(path=path)

    def close(self):
        self.browser.close()
        self._p.stop()

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close()
