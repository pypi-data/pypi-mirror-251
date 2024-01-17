import json
import requests
from bs4 import BeautifulSoup
import pandas as pd
from newspaper import Article 

def scrape_ag(query, path):
    query = query.replace(" ", "+")
    headers = {
        "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36"
    }
    response = requests.get(
        "https://www.google.com/search?q={0}&gl=us&tbm=nws&num=100".format(query), headers=headers
    )
    soup = BeautifulSoup(response.content, "html.parser")
    res = []
 
    for el in soup.select("div.SoaBEf"):
        res.append(
            {
                "link": el.find("a")["href"],
                "title": el.select_one("div.MBeuO").get_text(),
                "content" : ""
            }
        )
  
    df = pd.read_json(json.dumps(res, indent = 2))
    df.to_csv(path)
    print(res)

def parse_ag(df_path):
    df = pd.read_csv(df_path)
    for index, row in df.iterrows():
        try:
            article = Article(row.link)
            article.download()
            article.parse()
            df.loc[index, 'content'] = article.text
        except:
            pass
    df.to_csv(df_path)
