from .base import BaseScraper

class FlipkartScraper(BaseScraper):
    SITE = "flipkart"

    def run(self, keywords: str, max_price: int | None = None, **_):
        b = self.browser
        b.navigate("https://www.flipkart.com")
        b.wait(3000)

        # Close popup if appears
        try:
            b.page.locator("button._2KpZ6l._2doB4z").click(timeout=3000)
        except:
            pass

        b.fill("input[name='q']", keywords)
        b.press("input[name='q']", "Enter")
        b.wait(5000)
        b.page.mouse.wheel(0, 8000)
        b.wait(3000)

        cards = b.page.locator("div.tUxRFH")
        total = cards.count()
        print(f"🔍 Flipkart cards found: {total}")

        for i in range(min(25, total)):
            item = cards.nth(i)
            try:
                title = item.locator("div.KzDlHZ").inner_text(timeout=2000)
                price = item.locator("div.Nx9bqj._4b5DiR").inner_text(timeout=2000)
                price = int(price.replace("₹", "").replace(",", "").strip())
                url = item.locator("a.CGtC98").get_attribute("href")

                if not max_price or price <= max_price:
                    self.data.append({
                        "title": title,
                        "price": price,
                        "url": "https://www.flipkart.com" + url
                    })
                    print(f"🛒 {title} — ₹{price}")

            except Exception as e:
                print(f"⚠️ Skipped item #{i}: {e}")
