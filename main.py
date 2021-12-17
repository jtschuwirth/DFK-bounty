from pyhmy import blockchain, transaction, account
from datetime import datetime
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from pycoingecko import CoinGeckoAPI
from eth_utils import to_checksum_address
from bech32 import (
    bech32_decode,
    convertbits
)

from web3 import Web3
import json

#uvicorn main:app --reload

app = FastAPI()
cg = CoinGeckoAPI()

origins = ["*", "http://localhost:3000/"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

main_net = 'https://rpc.s0.t.hmny.io'
w3 = Web3(Web3.HTTPProvider(main_net))
#test_address = one1se7lv0g7athe8xzz2rmckj7c83cx2twwks52kj
#test_address = 0xa8c5115c8e44351b2bc2d401a1f033bb45129dc5
#{'id': 'defi-kingdoms', 'symbol': 'jewel', 'name': 'DeFi Kingdoms'}
#{'id': 'harmony', 'symbol': 'one', 'name': 'Harmony'}
#1629518400

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
    "Foraging"                    : "one1xyevw6k0ygtkgmac8yv33552z67c4rh5x4rnap",
    "Fishing"                     : "one1ufv7swrd8pr87rnllmdkns7fey6althufxwzpy",
    "WishingWell"                 : "one17hlkna9vf2z3wvrx3wflcsytc8zfaaxw5rgfth",
    "AuctionHouse"                : "one1zwn9h8uq883vqv4uqgshrhq9kvxr72yjjjz9la",
    "Summoning"                   : "one1vh02j0mm3pkr8fuvzq6rye7a89e8w7xzvel70f",
    "MeditationCircle"            : "one1qk2ds6efyvrk5gckat4yu89zsmd2zskpwyytuq",
    "Quest"                   : "one12yqt6vdcygm3zz9q7c7uldjefwv3n6h5trltq4"
}

MeditationCircleJson = open("MeditationCircle.json")
MeditationCircleABI = json.load(MeditationCircleJson)

HeroSummoningUpgradeableJson = open("HeroSummoningUpgradeable.json")
SummoningABI = json.load(HeroSummoningUpgradeableJson)

ERC721Json = open("ERC721.json")
ERC721ABI = json.load(ERC721Json)

QuestCoreJson = open("QuestCoreV2.json")
QuestCoreABI = json.load(QuestCoreJson)

dfk_contracts_abi = {
    "MeditationCircle" : MeditationCircleABI,
    "Summoning"        : SummoningABI,
    "Hero"             : ERC721ABI,
    "Quest"            : QuestCoreABI
}

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

def DFKContract(tx):
    for key,value in dfk_contracts.items():
        if tx["to"] == value or tx["from"] == value:
            return key

    return False

def gasPaid(gas, gasPrice):
    gas = int(gas, 16)
    gasPrice = int(gasPrice, 16)
    return (gas*gasPrice)/(10**18)

def getTxType(tx, contract_name):
    for key, value in dfk_contracts_abi.items():
        if contract_name == key:
            contract = w3.eth.contract(address=convert_one_to_hex(dfk_contracts[contract_name]), abi=dfk_contracts_abi[contract_name])
            contract_result = contract.decode_function_input(tx["input"])
            if contract_name == "MeditationCircle":
                decode = decodeMeditationCircle(contract_result)
                return decode
            elif contract_name == "Hero":
                decode = decodeHero(contract_result)
                return decode
            elif contract_name == "Quest":
                decode = decodeQuest(contract_result)
                return decode
            else:
                result = contract_result
                print(contract_name, result)
                #return result
    return ""


def decodeMeditationCircle(result):
    decode = ""
    if str(result[0]) == "<Function completeMeditation(uint256)>":
        decode = f"Complete Meditation with Hero: {result[1]['_heroId']}"
    elif str(result[0]) == "<Function startMeditation(uint256,uint8,uint8,uint8,address)>":
        decode = f"Start Meditation with Hero: {result[1]['_heroId']}"
    return decode

def decodeSummoning(result):
    pass

def decodeHero(result):
    decode = ""
    if str(result[0]) == "<Function setApprovalForAll(address,bool)>":
        if str(result[1]["operator"]) == '0x13a65B9F8039E2c032Bc022171Dc05B30c3f2892':
            decode = f"Approval for auction House"
    return decode

def decodeQuest(result):
    decode = ""
    if str(result[0]) == "<Function completeQuest(uint256)>":
        decode = f"Quest Completed with Hero: {result[1]['_heroId']}"
    elif str(result[0]) == "<Function startQuest(uint256[],address,uint8)>":
        if str(result[1]["_questAddress"]) == '0x0548214A0760a897aF53656F4b69DbAD688D8f29':
            decode = f"Quest ? Started with Heroes: {result[1]['_heroIds']}"
        elif str(result[1]["_questAddress"]) == '0xE259e8386d38467f0E7fFEdB69c3c9C935dfaeFc':
            decode = f"Quest Fishing Started with Heroes: {result[1]['_heroIds']}"
    return decode


def getValueJewel(tx):
    return 0

def convertCurrency(valueOne, valueJewel, onePrice, jewelPrice, timestamp, gasPaid):
    #Arreglar que si el i nunca es mayor al timestamp se utilize el ultimo dato
    value = 0
    gas = 0
    for i in onePrice["prices"]:
        if i[0]>timestamp*1000:
            value = value + i[1]*valueOne
            gas = i[1]*gasPaid
            break
    for i in jewelPrice["prices"]:
        if i[0]>timestamp*1000:
            value = value + i[1]*valueJewel
            break
    return [round(value, 3), round(gas, 5)]


def getDelta(tx):
    return ""

def totalGasPaid(txs_history):
    gasPaid = 0
    for value in txs_history.items():
        gasPaid = gasPaid + value[1]["gasPaid"]
    return round(gasPaid, 5)

def totalGasPaidCurrency(txs_history):
    gasPaid = 0
    for value in txs_history.items():
        gasPaid = gasPaid + value[1]["gasPaidCurrency"]
    return round(gasPaid, 5)

def generate_metadata(txs_history):
    GasPaidOne = totalGasPaid(txs_history)
    GasPaidCurrency = totalGasPaidCurrency(txs_history)

    metadata = {
        "totalBalanceOne" : "",
        "totalBalanceCurrency" : "", 
        "totalGasPaidOne" : GasPaidOne,
        "totalGasPaidCurrency" : GasPaidCurrency
    }
    return metadata

def generate_report(address, startTime, endTime, currency):
    onePrice = cg.get_coin_market_chart_range_by_id("harmony", currency, startTime, datetime.timestamp(datetime.now()))
    jewelPrice = cg.get_coin_market_chart_range_by_id("defi-kingdoms", currency, startTime, datetime.timestamp(datetime.now()))
    txs_history = {}
    txs = account.get_transaction_history(address, page=0, page_size=100, include_full_tx=False, tx_type='ALL', order='DESC', endpoint=main_net)
    c=0
    for tx_hash in txs:

        tx = transaction.get_transaction_by_hash(tx_hash, main_net)
        #First check if it is a contract that we care of 
        contract_name = DFKContract(tx)
        if int(tx["timestamp"], 16) < startTime:
            continue
        elif int(tx["timestamp"], 16) > endTime:
            break
        elif contract_name == False:
            continue
        txData = {
            "chain" : "Harmony"
        }
        txData["hash"] = tx["hash"]
        txData["from"] = tx["from"]
        txData["to"] = tx["to"]
        txData["gasPaid"] = round(gasPaid(tx["gas"], tx["gasPrice"]), 5)
        txData["contract"] = contract_name
        txData["txType"] = getTxType(tx, contract_name)
        txData["valueOne"] = round(int(tx["value"], 16)/(10**18), 3)
        txData["valueJewel"] = getValueJewel(tx)
        txData["timestamp"] = int(tx["timestamp"], 16)
        CurrencyValues = convertCurrency(txData["valueOne"], txData["valueJewel"], onePrice, jewelPrice, txData["timestamp"], txData["gasPaid"])
        txData["valueCurrency"] = CurrencyValues[0]
        txData["gasPaidCurrency"] = CurrencyValues[1]
        txData["delta"] = getDelta(tx)
        txs_history[c] = txData
        c+=1
    metadata = generate_metadata(txs_history)
    return {"txs": txs_history, "metadata" : metadata}

class Data(BaseModel):
    address: str
    startTime: int
    endTime: int
    currency: str


@app.post("/")
async def main(data: Data):
    return generate_report(data.address, data.startTime, data.endTime, data.currency)




    
