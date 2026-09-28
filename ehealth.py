import requests
import pandas as pd
import time

app_id = "1514742468"
reviews = []

for page in range(1, 8):  
    url = f"https://itunes.apple.com/hk/rss/customerreviews/id={app_id}/sortBy=mostRecent/page={page}/json"
    resp = requests.get(url)
    data = resp.json()
    entries = data.get("feed", {}).get("entry", [])
    for e in entries:
        if "im:rating" in e: 
            reviews.append({
                "rating": e["im:rating"]["label"],
                "title": e["title"]["label"],
                "content": e["content"]["label"],
                "date": e.get("updated", {}).get("label", "")
            })
    time.sleep(1)

df = pd.DataFrame(reviews).drop_duplicates(subset=["date", "title", "content"])
df.to_csv("ehealth_reviews.csv", index=False, encoding="utf-8-sig")
print(f"total: {len(df)} comments")