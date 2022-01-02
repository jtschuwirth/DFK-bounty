import requests
import json

url = "http://graph3.defikingdoms.com/subgraphs/name/defikingdoms/dex"
query = """
    query ($token: String) { 
        token (id: $token) {
            id
            symbol
            tokenDayData (first: 150, orderBy: date, orderDirection: desc) {
                priceUSD
      			date
            }
        }  
    }"""
headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'User-Agent': 'Mozilla/5.0'
}
variables = {
    "token":"0x19b9f05cde7a61ab7aae5b0ed91aa62ff51cf881"
}
r = requests.post(url, json={'query': query, "variables": variables}, headers=headers)
tokenDayData = r.json()["data"]["token"]["tokenDayData"]
data = {}
symbol =r.json()["data"]["token"]["symbol"]
print(symbol)
for i in tokenDayData:
    data[i["date"]] = i["priceUSD"]

with open(f'items/{symbol}.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)