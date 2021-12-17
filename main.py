from pyhmy import blockchain, transaction, account
from datetime import datetime
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
#uvicorn main:app --reload

app = FastAPI()

origins = ["*", "http://localhost:3000/"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

main_net = 'https://rpc.s0.t.hmny.io'
#test_address = "one1se7lv0g7athe8xzz2rmckj7c83cx2twwks52kj"

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
    "Gaia's Tears"                : "one1yn4q6smd8snq97l7l0n2z6auxpxfv0gyvfd7gr",
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
    "Serendale_Foraging"          : "one1xyevw6k0ygtkgmac8yv33552z67c4rh5x4rnap",
    "Serendale_Fishing"           : "one1ufv7swrd8pr87rnllmdkns7fey6althufxwzpy",
    "Serendale_WishingWell"       : "one17hlkna9vf2z3wvrx3wflcsytc8zfaaxw5rgfth",
    "Serendale_AuctionHouse"      : "one1zwn9h8uq883vqv4uqgshrhq9kvxr72yjjjz9la",
    "Serendale_summoning"         : "one1vh02j0mm3pkr8fuvzq6rye7a89e8w7xzvel70f",
    "Serendale_MeditationCircle"  : "one1qk2ds6efyvrk5gckat4yu89zsmd2zskpwyytuq"
}

def DFKContract(tx):
    for key,value in dfk_contracts.items():
        if tx["to"] == value or tx["from"] == value:
            return key

    return False

def gasPaid(gas, gasPrice):
    gas = int(gas, 16)
    gasPrice = int(gasPrice, 16)
    return (gas*gasPrice)/(10**18)

def getTxType(tx):
    return ""

def getValueJewel(tx):
    return ""

def getValueUSD(tx):
    return ""

def getDelta(tx):
    return ""

def totalGasPaid(txs_history):
    gasPaid = 0
    for value in txs_history.items():
        gasPaid = gasPaid + value[1]["gasPaid"]
    return round(gasPaid, 5)

def generate_metadata(txs_history):
    totalGasPaidOne = totalGasPaid(txs_history)

    metadata = {
        "totalBalanceOne" : "",
        "totalBalanceUSD" : "", 
        "totalGasPaidOne" : totalGasPaidOne,
        "totalGasPaidUSD" : ""
    }
    return metadata

def generate_report(address, startTime, endTime):
    txs_history = {}
    txs = account.get_transaction_history(address, page=0, page_size=10, include_full_tx=False, tx_type='ALL', order='DESC', endpoint=main_net)
    c=0
    for tx_hash in txs:

        tx = transaction.get_transaction_by_hash(tx_hash, main_net)
        #First check if it is a contract that we care of 
        contract = DFKContract(tx)
        if int(tx["timestamp"], 16) < startTime:
            continue
        elif int(tx["timestamp"], 16) > endTime:
            break
        elif contract == False:
            continue
        txData = {
            "chain" : "Harmony"
        }
        txData["hash"] = tx["hash"]
        txData["from"] = tx["from"]
        txData["to"] = tx["to"]
        txData["gasPaid"] = round(gasPaid(tx["gas"], tx["gasPrice"]), 5)
        txData["contract"] = contract
        txData["txType"] = getTxType(tx)
        txData["valueOne"] = round(int(tx["value"], 16)/(10**18), 3)
        txData["valueJewel"] = getValueJewel(tx)
        txData["valueUSD"] = getValueUSD(tx)
        txData["delta"] = getDelta(tx)
        txData["timestamp"] = int(tx["timestamp"], 16)
        txs_history[c] = txData
        c+=1
    metadata = generate_metadata(txs_history)
    return {"txs": txs_history, "metadata" : metadata}

class Data(BaseModel):
    address: str
    startTime: int
    endTime: int

@app.post("/")
async def main(data: Data):
    return generate_report(data.address, data.startTime, data.endTime)




    
