from datetime import datetime
from .base import BaseScraper

class CleartripScraper(BaseScraper):
    SITE = "cleartrip"

    def run(self, origin: str, destination: str, date: str, **_):
        b = self.browser
        page = b.page

        # Convert YYYY-MM-DD → DD/MM/YYYY
        try:
            formatted_date = datetime.strptime(date, "%Y-%m-%d").strftime("%d/%m/%Y")
        except:
            print(f"⚠️ Invalid date format: {date}")
            return

        # Build URL
        url = (
            f"https://www.cleartrip.com/flights/results?"
            f"adults=1&childs=0&infants=0&class=Economy"
            f"&depart_date={formatted_date}"
            f"&from={origin}&to={destination}&intl=n"
        )

        print("🌐 Navigating:", url)
        b.navigate(url)

        try:
            page.wait_for_selector("div.sc-aXZVg.dAqxAC", timeout=20000)
        except:
            print("⚠️ Flights not loaded.")
            return

        cards = page.locator("div.sc-aXZVg.dAqxAC")
        total = cards.count()
        print(f"🔍 Found {total} flights")

        for i in range(total):
            try:
                card = cards.nth(i)
                airline = card.locator("p.sc-eqUAAy.giMTRs").inner_text()
                flight_no = card.locator("p.sc-eqUAAy.fkahrI").inner_text()
                times = card.locator("p.sc-eqUAAy.kZeIiG").all_inner_texts()
                price = card.locator("h2.sc-eqUAAy.kXeydX").inner_text()

                dep_time, arr_time = times[0], times[-1] if len(times) >= 2 else ("", "")

                self.data.append({
                    "airline": airline,
                    "flight_no": flight_no,
                    "departure": dep_time,
                    "arrival": arr_time,
                    "price": price
                })

                print(f"🛫 {airline} {flight_no} | {dep_time} → {arr_time} | {price}")

            except Exception as e:
                print(f"⚠️ Skipped flight {i}: {e}")
                continue
