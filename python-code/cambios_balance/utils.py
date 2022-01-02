import json
import requests
from eth_utils import to_checksum_address
from math import floor
from pyhmy import blockchain, transaction, account
from bech32 import (
    bech32_decode,
    convertbits
)

dfk_contracts = {
    "UniswapV2Factory"            : "one1jq2tjdcxnyvt6vvlsr5t8w629nm04f0hfepala",
    "UniswapV2Router02"           : "one1yjkky5pdr3jje3mggzq3d8gy394vyresl69pgt",
    "JewelToken"                  : "one1wt93p34l543ym5r77cyqyl3kd0tfqpy0eyd6n0",
    "xJEWEL"                      : "one1488gx5rasuk9uynnuaz6hn76sjw65e206pmljg",
    "Bank"                        : "one1488gx5rasuk9uynnuaz6hn76sjw65e206pmljg",
    "Banker"                      : "one1x6z7ca022v2zfwlx0kc3upcp82ltjhc7ucgz82",
    "MasterGardener"              : "one1mvcxg0r34j0zzgk2qdq76a7sn40en7fy7lytq4",
    "Airdrop"                     : "one15eudryl7e3nhuym6qrl0ksafenl62vsszleqj2",
    "Profiles"                    : "one14028gx2gxa937hw4m46entqlsk35etxaln7glh",
    "Hero"                        : "one1ta6nmn0ekxke427px3npf505w3hadnjuhlh7vv",
    "Gaias Tears"                 : "one1yn4q6smd8snq97l7l0n2z6auxpxfv0gyvfd7gr",
    "DFK Gold"                    : "one18f8deue39azw7qn6elvvyyuz55jejdh8xdfdw2",
    "Ambertaffy"                  : "one1dcduq8x995t9kdtuggzzeasgzkdzhqwpmxtseg",
    "Darkweed"                    : "one1dr4yvsx9eekvpjdp79ahhzpvk8974nxhfufs5f",
    "Goldvein"                    : "one1vqz5rttvuz5ttkhx3uyx633kz56dyr5qyqtqgu",
    "Ragweed"                     : "one1qslehkdmzl0ujr0r6styyf54mk86g3yxfg93ja",
    "Redleaf"                     : "one1p9py8hatlwe7daccz3sc4njn7pek92zvk4m3v9",
    "Rockroot"                    : "one1dvg26m3mnyysmcstl8u4l9s2mhp4aulzk6fll0",
    "Swift-Thistle"               : "one1ehl73x8xsl55rvfym7mayjvryejf9mcaedtayj",
    "Bloater"                     : "one10zhdvk3vcsx8mzcd7925mfst8zkn29pjag56j9",
    "Ironscale"                   : "one1un87uklstnhngxx6wn8m39e8mrj0a606xkqp8d",
    "Lanterneye"                  : "one13062pzyy28rt2sftetfank3aeawxefa7y4ma8u",
    "Redgill"                     : "one1cky3jyn33n8lejtn95v59nxe34vnfshpr8q9da",
    "Sailfish"                    : "one1hq9q0cfjgrp3a3kupdwh9tme63sa5wns3ffz33",
    "Shimmerskin"                 : "one1xuk276qn2d6clxz4j734yehhkvc29fzdpkuz7e",
    "Silverfin"                   : "one1yjfulkkvp7wqwfqttvwyhcyvv2uwalmf82k75p",
    "Shvas Rune"                  : "one1vm6mlkgsekpaxanvfvuazdeseygm955x5cx9pr",
    "Blue Pet Egg"                : "one1jeu9rrsylcp0kv94tcksu42wyccx6zyj7xfvzm",
    "Grey Pet Egg"                : "one1jhgzc8w93uz6q9f8t66fuyr3xlv7aqwufwkmqs",
    "Golden Egg"                  : "one1nmdnmgvtujcrs4ln6w0c8ewx4tt8hs2gangmff",
    "AVAX JEWEL"                  : "0x4f60a160D8C2DDdaAfe16FCC57566dB84D674BD6",
    "Foraging"                    : "one1xyevw6k0ygtkgmac8yv33552z67c4rh5x4rnap",
    "Fishing"                     : "one1ufv7swrd8pr87rnllmdkns7fey6althufxwzpy",
    "WishingWell"                 : "one17hlkna9vf2z3wvrx3wflcsytc8zfaaxw5rgfth",
    "AuctionHouse"                : "one1zwn9h8uq883vqv4uqgshrhq9kvxr72yjjjz9la",
    "Summoning"                   : "one1vh02j0mm3pkr8fuvzq6rye7a89e8w7xzvel70f",
    "MeditationCircle"            : "one1qk2ds6efyvrk5gckat4yu89zsmd2zskpwyytuq",
    "Quest"                       : "one12yqt6vdcygm3zz9q7c7uldjefwv3n6h5trltq4"
}

dfk_contractsETH = {
    "0xD74433B187Cf0ba998Ad9Be3486B929c76815215" : "Artemis",
    "0x72Cb10C6bfA5624dD07Ef608027E366bd690048F" : "Jewel",
    "0x95CE547D730519A90dEF30d647F37D9E5359B6Ae" : "wLuna",
    "0xcF664087a5bB0237a0BAd6742852ec6c8d69A27a" : "One",
    "0x735aBE48e8782948a37C7765ECb76b98CdE97B0F" : "Fantom",
    "0xE176EBE47d621b984a73036B9DA5d834411ef734" : "BUSD",
    "0x3a4EDcf3312f44EF027acfd8c21382a5259936e7" : "DFK Gold",

    '0x66F5BfD910cd83d3766c4B39d13730C911b2D286' : "Shvas Rune",
    "0x24eA0D436d3c2602fbfEfBe6a16bBc304C963D04" : "Gaias Tears",
    "0x95d02C1Dc58F05A015275eB49E107137D9Ee81Dc" : "Grey Pet Egg",
    "0x9678518e04fe02fb30b55e2d0e554e26306d0892" : "Blue Pet Egg",
    "0x6d605303e9Ac53C59A3Da1ecE36C9660c7A71da5" : "Green Pet Egg",

    "0x78aED65A2Cc40C7D8B0dF1554Da60b38AD351432" : "Bloater",
    "0xe4Cfee5bF05CeF3418DA74CFB89727D8E4fEE9FA" : "Ironscale",
    "0x8Bf4A0888451C6b5412bCaD3D9dA3DCf5c6CA7BE" : "Lanterneye",
    "0xc5891912718ccFFcC9732D1942cCD98d5934C2e1" : "Redgill",
    "0xb80A07e13240C31ec6dc0B5D72Af79d461dA3A70" : "Sailfish",
    "0x372CaF681353758f985597A35266f7b330a2A44D" : "Shimmerskin",
    "0x2493cfDAcc0f9c07240B5B1C4BE08c62b8eEff69" : "Silverfin",

    "0x6e1bC01Cc52D165B357c42042cF608159A2B81c1" : "Ambertaffy",
    "0x68EA4640C5ce6cC0c9A1F17B7b882cB1cBEACcd7" : "Darkweed",
    "0x600541aD6Ce0a8b5dae68f086D46361534D20E80" : "Goldvein",
    "0x043F9bd9Bb17dFc90dE3D416422695Dd8fa44486" : "Ragweed",
    "0x094243DfABfBB3E6F71814618ace53f07362a84c" : "Redleaf",
    "0x6B10Ad6E3b99090De20bF9f95F960addC35eF3E2" : "Rockroot",
    "0xCdfFe898E687E941b124dfB7d24983266492eF1d" : "Swift-Thistle",

    "0xAC5c49Ff7E813dE1947DC74bbb1720c353079ac9" : "Blue Stem",
    "0xc0214b37FCD01511E6283Af5423CF24C96BB9808" : "Milkweed",
    "0x19B9F05cdE7A61ab7aae5b0ed91aA62FF51CF881" : "Spiderfruit"
}

dfk_contracts_tokens = {
    "JewelToken"                  : "one1wt93p34l543ym5r77cyqyl3kd0tfqpy0eyd6n0",
    "Jewel"                       : "one1wt93p34l543ym5r77cyqyl3kd0tfqpy0eyd6n0",
    "One"                         : "one1eanyppa9hvpr0g966e6zs5hvdjxkngn6jtulua",
    "Gaias Tears"                 : "one1yn4q6smd8snq97l7l0n2z6auxpxfv0gyvfd7gr",
    "DFK Gold"                    : "one18f8deue39azw7qn6elvvyyuz55jejdh8xdfdw2",
    "Ambertaffy"                  : "one1dcduq8x995t9kdtuggzzeasgzkdzhqwpmxtseg",
    "Darkweed"                    : "one1dr4yvsx9eekvpjdp79ahhzpvk8974nxhfufs5f",
    "Goldvein"                    : "one1vqz5rttvuz5ttkhx3uyx633kz56dyr5qyqtqgu",
    "Ragweed"                     : "one1qslehkdmzl0ujr0r6styyf54mk86g3yxfg93ja",
    "Redleaf"                     : "one1p9py8hatlwe7daccz3sc4njn7pek92zvk4m3v9",
    "Rockroot"                    : "one1dvg26m3mnyysmcstl8u4l9s2mhp4aulzk6fll0",
    "Swift-Thistle"               : "one1ehl73x8xsl55rvfym7mayjvryejf9mcaedtayj",
    "Bloater"                     : "one10zhdvk3vcsx8mzcd7925mfst8zkn29pjag56j9",
    "Ironscale"                   : "one1un87uklstnhngxx6wn8m39e8mrj0a606xkqp8d",
    "Lanterneye"                  : "one13062pzyy28rt2sftetfank3aeawxefa7y4ma8u",
    "Redgill"                     : "one1cky3jyn33n8lejtn95v59nxe34vnfshpr8q9da",
    "Sailfish"                    : "one1hq9q0cfjgrp3a3kupdwh9tme63sa5wns3ffz33",
    "Shimmerskin"                 : "one1xuk276qn2d6clxz4j734yehhkvc29fzdpkuz7e",
    "Silverfin"                   : "one1yjfulkkvp7wqwfqttvwyhcyvv2uwalmf82k75p",
    "Shvas Rune"                  : "one1vm6mlkgsekpaxanvfvuazdeseygm955x5cx9pr",
    "Blue Pet Egg"                : "one1jeu9rrsylcp0kv94tcksu42wyccx6zyj7xfvzm",
    "Grey Pet Egg"                : "one1jhgzc8w93uz6q9f8t66fuyr3xlv7aqwufwkmqs",
    "Golden Egg"                  : "one1nmdnmgvtujcrs4ln6w0c8ewx4tt8hs2gangmff",
    "Hero"                        : "one1ta6nmn0ekxke427px3npf505w3hadnjuhlh7vv"
}

dfk_item_symbol = {
    "Jewel"        : "JEWEL",
    "Gaias Tears"  : "DFKTEARS",
    "DFK Gold"     : "DFKGOLD",
    "Ambertaffy"   : "DFKAMBRTFY",
    "Darkweed"     : "DFKDRKWD",
    "Goldvein"     : "DFKGLDVN",
    "Ragweed"      : "DFKRGWD",
    "Redleaf"      : "DFKRDLF",
    "Rockroot"     : "DFKRCKRT",
    "Swift-Thistle": "DFKSWFTHSL",
    "Bloater"      : "DFKBLOATER",
    "Ironscale"    : "DFKIRONSCALE",
    "Lanterneye"   : "DFKLANTERNEYE",
    "Redgill"      : "DFKREDGILL",
    "Sailfish"     : "DFKSAILFISH",
    "Shimmerskin"  : "DFKSHIMMERSKIN",
    "Silverfin"    : "DFKSILVERFIN",
    "Shvas Rune"   : "DFKSHVAS"
}

Blacklist = [
    "Green Pet Egg",
    "Grey Pet Egg",
    "Blue Pet Egg",
    "Blue Stem",
    "Milkweed",
    "Spiderfruit"
]

url = "http://graph3.defikingdoms.com/subgraphs/name/defikingdoms/dex"
urlAuctionHouse = "http://graph3.defikingdoms.com/subgraphs/name/defikingdoms/apiv5"
headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'User-Agent': 'Mozilla/5.0'
}
AVAXurl = "127.0.0.1:9650/ext/bc/X"

def AVAX_get_transaction_history(address, page, pageSize, assetID):
    method = "avm.getAddressTxs"
    params ={
      "address" : address,
      "cursor"  : page,
      "assetID" : assetID,
      "pageSize": pageSize
  }
    payload = json.dumps({"method": method, "params": params})
    r = requests.post(AVAXurl, data=payload, headers=headers)
    print(r)

def getValueOnetoCurrency(amount, currency, timestamp):
    if currency == "usd":
        oneUSD = open("cg/onePriceUSD.json")
        onePrice = json.load(oneUSD)
    elif currency == "eur":
        oneEUR = open("cg/onePriceEUR.json")
        onePrice = json.load(oneEUR)
    if timestamp == "last":
        value = onePrice["prices"][-1][1]*amount
        return round(value, 5)
    else:
        for i in onePrice["prices"]:
            if i[0] > timestamp*1000:
                value = i[1]*amount
                return round(value, 5)
    value = onePrice["prices"][-1][1]*amount
    return round(value, 5)
            
def getValueJeweltoCurrency(amount, currency, timestamp):
    if currency == "usd":
        jewelUSD = open("cg/jewelPriceUSD.json")
        jewelPrice = json.load(jewelUSD)
    elif currency == "eur":
        jewelEUR = open("cg/jewelPriceEUR.json")
        jewelPrice = json.load(jewelEUR)
    if timestamp == "last":
        value = jewelPrice["prices"][-1][1]*amount
        return round(value, 5)
    else:
        for i in jewelPrice["prices"]:
            if i[0] > timestamp*1000:
                value = i[1]*amount
                return round(value, 5)
    value = jewelPrice["prices"][-1][1]*amount
    return round(value, 5)

def getLastValueItemtoCurrency(token, currency):
    if currency == "usd":
        if token in dfk_contractsETH:
            if dfk_contractsETH[token] not in Blacklist:
                value = queryPriceByDateJSON(dfk_contractsETH[token], "last")
                #value = queryPriceLast(token.lower())
                return round(value, 3)
            else:
                return 0
        else:
            return 0
    elif currency == "eur":
        if token in dfk_contractsETH:
            if dfk_contractsETH[token] not in Blacklist:
                valueUSD = queryPriceByDateJSON(dfk_contractsETH[token], "last")
                #valueUSD = queryPriceLast(token.lower())
                value = convertUSDtoEUR(valueUSD)
                return round(value, 3)
            else:
                return 0
        else:
            return 0

def convertUSDtoEUR(valueUSD):
    #Mejorar para que utilize los precios USD/EUR del momento y no solo los mas actuales!
    oneUSD = open("cg/onePriceUSD.json")
    onePriceUSD = json.load(oneUSD)["prices"][-1][1]
    oneEUR = open("cg/onePriceEUR.json")
    onePriceEUR = json.load(oneEUR)["prices"][-1][1]
    value = (valueUSD/onePriceUSD)*onePriceEUR
    return value

def queryPriceLast(token):
    query = """
        query ($token: String, $date: Int) { 
            token (id: $token) {
            symbol
            tokenDayData (first: 1, orderBy: date, orderDirection: desc) {
                priceUSD
            }
        }  
    }"""
    variables = {
        "token": token, 
    }
    r = requests.post(url, json={'query': query, "variables": variables}, headers=headers)
    if str(r.json()["data"]["token"]["tokenDayData"]) == "[]":
        item_price = 0
    else:
        item_price = round(float(r.json()["data"]["token"]["tokenDayData"][0]["priceUSD"]), 5)
    return item_price

def queryPriceByDate(token, date):
    query = """
        query ($token: String, $date: Int) { 
            token (id: $token) {
            symbol
            tokenDayData(where: {date: $date}) {
                priceUSD
            }
        }  
    }"""
    variables = {
        "token": token, 
        "date" : date
    }
    r = requests.post(url, json={'query': query, "variables": variables}, headers=headers)
    if str(r.json()["data"]["token"]["tokenDayData"]) == "[]":
        item_price = 0
    else:
        item_price = round(float(r.json()["data"]["token"]["tokenDayData"][0]["priceUSD"]), 5)
    return item_price

def queryAuctionStatus(auctionId):
    query = """
        query ($id: Int) { 
            saleAuction (id: $id) {
                open
                purchasePrice
            }
        }  
    """
    variables = {
        "id": auctionId, 
    }
    r = requests.post(urlAuctionHouse, json={'query': query, "variables": variables}, headers=headers)
    if str(r.json()["data"]["saleAuction"]) == "None":
        status = "unknown"
    elif str(r.json()["data"]["saleAuction"]["open"]) == "True":
        status = "open"
    elif str(r.json()["data"]["saleAuction"]["purchasePrice"]) == "None":
        status = "cancelled"
    else:
        status = "sold"
    return status

def convert_one_to_hex(addr):
    """
    Given a one address, convert it to hex checksum address
    """
    if not account.is_valid_address(addr):
        return to_checksum_address(addr)
    hrp, data = bech32_decode(addr)
    buf = convertbits(data, 5, 8, False)
    address = '0x' + ''.join('{:02x}'.format(x) for x in buf)
    return to_checksum_address(address)

def getBalanceChange(transaction_info, timestamp, currency, balances):
    balanceChange = {}
    if transaction_info["event"] == "Quest Completed":
        balanceChange = {}
        for key, value in transaction_info["rewards"].items():
            if key not in Blacklist:
                    price = queryPriceByDateJSON(key, timestamp)
            else:
                price = 0
            if currency == "eur":
                price = convertUSDtoEUR(price)
            balanceChange[key] = [value, price*value]


    elif transaction_info["event"] == "Claim LP rewards":
        gainsJewel = getValueJeweltoCurrency(
            transaction_info["unlockedAmount"], 
            currency, 
            timestamp)
        balanceChange = {
            "Jewel": [transaction_info["unlockedAmount"], gainsJewel]
        }

    
    elif transaction_info["event"] == "Trade":
        bought = 0
        sold = 0

        if (transaction_info["bought"] == "One"):
            bought = getValueOnetoCurrency(
                transaction_info["boughtAmount"], 
                currency, 
                timestamp)
        elif (transaction_info["bought"] == "Jewel"):
            bought = getValueJeweltoCurrency(
                transaction_info["boughtAmount"], 
                currency, 
                timestamp)
        
        if transaction_info["sold"] in dfk_contracts_tokens:
            if transaction_info["sold"] in balances and balances[transaction_info["sold"]][0] > 0:
                if balances[transaction_info["sold"]][0] >= transaction_info["soldAmount"]:
                    sold = transaction_info["soldAmount"] * (balances[transaction_info["sold"]][1]/balances[transaction_info["sold"]][0])
                else:
                    value_bought = balances[transaction_info["sold"]][1]
                    token_to_buy = transaction_info["soldAmount"] - balances[transaction_info["sold"]][0]

                    if transaction_info["sold"] == "One":
                        value_to_buy = getValueOnetoCurrency(token_to_buy, currency, timestamp)
                    elif transaction_info["sold"] == "Jewel":
                        value_to_buy = getValueJeweltoCurrency(token_to_buy, currency, timestamp)
                    else:
                        value_to_buy = 0
                    sold = value_bought + value_to_buy

            else:
                if transaction_info["sold"] == "One":
                    sold = getValueOnetoCurrency(transaction_info["soldAmount"], currency, timestamp)
                elif transaction_info["sold"] == "Jewel":
                    sold = getValueJeweltoCurrency(transaction_info["soldAmount"], currency, timestamp) 
                else:
                    sold = bought
        else:
            sold = 0

        balanceChange = {
            transaction_info["sold"]: [-1*transaction_info["soldAmount"], -1*sold],
            transaction_info["bought"]: [transaction_info["boughtAmount"], bought]
        }
    
    elif transaction_info["event"] == "transfer Jewel":
        gainsJewel = getValueJeweltoCurrency(
            transaction_info["amount"], 
            currency, 
            timestamp)
        balanceChange = {
            "Jewel"   : [-1*transaction_info["amount"], -1*gainsJewel]
        }

    elif transaction_info["event"] == "Create Auction":
        if transaction_info["status"] != "sold":
            return { }
        

        if "Jewel" in balances and balances["Jewel"][0] > 0:
            if balances["Jewel"][0] >= transaction_info["price"]:
                gainsJewel = transaction_info["price"] * (balances["Jewel"][1]/balances["Jewel"][0])
            else:
                value_bought = balances["Jewel"][1]
                token_to_buy = transaction_info["price"] - balances["Jewel"][0]
                value_to_buy = getValueJeweltoCurrency(token_to_buy, currency, timestamp)
  
                gainsJewel = value_bought + value_to_buy
        else:
            gainsJewel = getValueJeweltoCurrency(transaction_info["price"], currency, timestamp) 

        balanceChange = {
            "Jewel": [transaction_info["price"], gainsJewel]
        }

    elif transaction_info["event"] == "Bought Hero":
        
        if "Jewel" in balances and balances["Jewel"][0] > 0:
            if balances["Jewel"][0] >= transaction_info["price"]:
                gainsJewel = transaction_info["price"] * (balances["Jewel"][1]/balances["Jewel"][0])
            else:
                value_bought = balances["Jewel"][1]
                token_to_buy = transaction_info["price"] - balances["Jewel"][0]
                value_to_buy = getValueJeweltoCurrency(token_to_buy, currency, timestamp)
  
                gainsJewel = value_bought + value_to_buy
        else:
            gainsJewel = getValueJeweltoCurrency(transaction_info["price"], currency, timestamp) 

        balanceChange = {
            "Jewel": [-1*transaction_info["price"], -1*gainsJewel]
        }

    elif transaction_info["event"] == "Summon Crystal":
        if "Jewel" in balances and balances["Jewel"][0] > 0:
            if balances["Jewel"][0] >= transaction_info["amountJewel"]:
                gainsJewel = transaction_info["amountJewel"] * (balances["Jewel"][1]/balances["Jewel"][0])
            else:
                value_bought = balances["Jewel"][1]
                token_to_buy = transaction_info["amountJewel"] - balances["Jewel"][0]
                value_to_buy = getValueJeweltoCurrency(token_to_buy, currency, timestamp)
  
                gainsJewel = value_bought + value_to_buy
        else:
            gainsJewel = getValueJeweltoCurrency(transaction_info["amountJewel"], currency, timestamp) 

        balanceChange = {
            "Jewel": [-1*transaction_info["amountJewel"], -1*gainsJewel]
        }
        
        gainsTears = queryPriceByDateJSON("Gaias Tears", timestamp)
        if currency == "eur":
            gainsTears = convertUSDtoEUR(gainsTears)
        
        
        tearAmount = transaction_info["summonerTears"] + transaction_info["assistantTears"]
        
        balanceChange = {
            "Gaias Tears": [-1*tearAmount, -1*gainsTears*tearAmount],
            "Jewel"      : [-1*transaction_info["amountJewel"], -1*gainsJewel]
        }
    
    elif transaction_info["event"] == "Start Meditation":
        if "Jewel" in balances and balances["Jewel"][0] > 0:
            if balances["Jewel"][0] >= transaction_info["price"]:
                gainsJewel = transaction_info["price"] * (balances["Jewel"][1]/balances["Jewel"][0])
            else:
                value_bought = balances["Jewel"][1]
                token_to_buy = transaction_info["price"] - balances["Jewel"][0]
                value_to_buy = getValueJeweltoCurrency(token_to_buy, currency, timestamp)
  
                gainsJewel = value_bought + value_to_buy
        else:
            gainsJewel = getValueJeweltoCurrency(transaction_info["price"], currency, timestamp) 

        balanceChange = {
            "Jewel": [-1*transaction_info["price"], -1*gainsJewel]
        }

        gainsRune = queryPriceByDateJSON(transaction_info["rune"], timestamp)
        if currency == "eur":
            gainsRune = convertUSDtoEUR(gainsRune)

        balanceChange = {
            transaction_info["rune"]   : [-1*transaction_info["amountRune"], -1*gainsRune*transaction_info["amountRune"]],
            "Jewel"                    : [-1*transaction_info["amountJewel"], -1*gainsJewel]
        }
    
    return balanceChange

def queryHeroLevel(id, block):
    query = """
        query ($id: Int $blockNumber: Int) { 
            hero (id: $id block: {number: $blockNumber}) {
                level
            }
        }  
    """
    variables = {
        "id": id, 
        "blockNumber": block
    }
    r = requests.post(urlAuctionHouse, json={'query': query, "variables": variables}, headers=headers)
    try:
        return r.json()["data"]["hero"]["level"]
    except:
        return "Error"

def queryHeroSummons(id, block):
    query = """
        query ($id: Int $blockNumber: Int) { 
            hero (id: $id block: {number: $blockNumber}) {
                generation
                summons
            }
        }  
    """
    variables = {
        "id": id, 
        "blockNumber": block
    }
    r = requests.post(urlAuctionHouse, json={'query': query, "variables": variables}, headers=headers)
    try:
        return (r.json()["data"]["hero"]["generation"], r.json()["data"]["hero"]["summons"])
    except: 
        return "Error"

def checkCostLevel(level):
    if level > 0 and level < 10:
        return [0.1*level, "Shvas Rune", floor(level/2)+1]
    else:
        return [0,"No Rune",0]

def checkCostSummons(generation, summons):
    if generation == 0:
        baseCost = 6
    else:
        baseCost = 10*generation
    return baseCost+summons*2

def queryPriceByDateJSON(item, date):
    item_price = 0
    symbol = dfk_item_symbol[item]
    priceJSON = open(f"items/{symbol}.json")
    priceData = json.load(priceJSON)
    if date == "last":
        return float(priceData["1640660400"])
    for key, value in priceData.items():
        if date>int(key):
            item_price = float(value)
            break
    if item_price == 0:
        return float(priceData["1640660400"])
    return round(item_price, 5)

def get_transactions_count(address, tx_type, endpoint):
    method = 'hmyv2_getTransactionsCount'
    params = [
        address,
        tx_type
    ]
    payload = {
        "id": "1",
        "jsonrpc": "2.0",
        "method": method,
        "params": params
    }
    headers = {
        'Content-Type': 'application/json'
    }

    resp = requests.request('POST', endpoint, headers=headers, data=json.dumps(payload), allow_redirects=True)
    return int(resp.json()["result"])
