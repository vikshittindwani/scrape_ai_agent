from .base import BaseScraper  # Inherit from base class

class AmazonScraper(BaseScraper):
    SITE = "amazon"

    def run(self, keywords: str, max_price: int | None = None, **_):
        b = self.browser
        b.navigate("https://www.amazon.in")
        b.fill("input#twotabsearchtextbox", keywords)
        b.press("input#twotabsearchtextbox", "Enter")
        b.wait(5000)

        # Wait for search results
        b.page.wait_for_selector("div[data-component-type='s-search-result']", timeout=15000)
        b.page.mouse.wheel(0, 5000)
        b.wait(4000)

        cards = b.page.locator("div[data-component-type='s-search-result']")
        total = cards.count()
        print(f"🔍 Amazon cards found: {total}")

        for i in range(min(25, total)):
            item = cards.nth(i)

            # ⚠️ Skip Sponsored
            try:
                if item.locator("span:has-text('Sponsored')").count() > 0:
                    print(f"⚠️ Skipped sponsored item #{i}")
                    continue
            except:
                pass

            try:
                # 🏷️ Title
                try:
                    title = item.locator("h2 span").first.inner_text(timeout=7000)
                except:
                    print(f"⚠️ No title for item #{i}")
                    continue

                # 💰 Price
                try:
                    price_str = item.locator("span.a-price-whole").first.inner_text(timeout=7000)
                    price = int(price_str.replace(",", "").replace("₹", "").strip())
                except:
                    print(f"⚠️ No price for item #{i}")
                    continue

                # 🔗 URL
                url = None
                try:
                    url = item.locator("h2 a").get_attribute("href", timeout=3000)
                except:
                    anchors = item.locator("a")
                    for j in range(anchors.count()):
                        try:
                            href = anchors.nth(j).get_attribute("href", timeout=1000)
                            if href and "/dp/" in href:
                                url = href
                                break
                        except:
                            continue

                if not url:
                    print(f"⚠️ No product URL for item #{i}")
                    continue

                # 🎯 Price Filter
                if not max_price or price <= max_price:
                    self.data.append({
                        "title": title.strip(),
                        "price": price,
                        "url": "https://amazon.in" + url
                    })
                    print(f"🛒 {title.strip()} — ₹{price}")

            except Exception as e:
                print(f"⚠️ Skipped item #{i} due to error: {e}")
                continue
