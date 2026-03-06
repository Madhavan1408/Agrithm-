"""
test_news_api.py
----------------
Quick test for the Farmer News Scraper.
Run: python test_news_api.py
"""

from news_api import get_farmer_news

TEST_CASES = [
    {"city": "Ongole",   "crop": "rice",   "state": "Andhra Pradesh"},
    {"city": "Nashik",   "crop": "grapes", "state": "Maharashtra"},
    {"city": "Ludhiana", "crop": "wheat",  "state": "Punjab"},
]

PASS_ICON = "✅"
FAIL_ICON = "❌"

def run_tests():
    all_passed = True
    for tc in TEST_CASES:
        city, crop, state = tc["city"], tc["crop"], tc["state"]
        print(f"\n{'─'*60}")
        print(f"  Testing: city={city!r}, crop={crop!r}, state={state!r}")
        print(f"{'─'*60}")
        try:
            articles = get_farmer_news(city=city, crop=crop, state=state, limit=5)
            assert isinstance(articles, list), "Result is not a list"
            assert len(articles) > 0,          "No articles returned"
            for a in articles:
                assert "title"     in a, "Missing 'title'"
                assert "url"       in a, "Missing 'url'"
                assert "source"    in a, "Missing 'source'"
                assert "published" in a, "Missing 'published'"
                assert "score"     in a, "Missing 'score'"

            print(f"  {PASS_ICON}  Got {len(articles)} articles")
            for i, a in enumerate(articles, 1):
                print(f"  [{i}] score={a['score']:>2}  {a['title'][:80]}")
                print(f"       {a['source']} | {a['published']}")
        except Exception as e:
            print(f"  {FAIL_ICON}  FAILED: {e}")
            all_passed = False

    print(f"\n{'═'*60}")
    if all_passed:
        print(f"  {PASS_ICON}  All tests passed!")
    else:
        print(f"  {FAIL_ICON}  Some tests failed. Check output above.")
    print(f"{'═'*60}")

if __name__ == "__main__":
    run_tests()
