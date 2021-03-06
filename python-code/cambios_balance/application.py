from pyhmy import account
from web3 import Web3
from datetime import datetime
from pycoingecko import CoinGeckoAPI
from eth_utils import to_checksum_address
from flask import Flask, request
from flask_cors import CORS
from collections import defaultdict
from math import ceil

from cambios_balance.utils import (
    convert_one_to_hex,
    queryAuctionStatus,
    queryPriceByDate,
    queryPriceLast,
    convertUSDtoEUR,
    getLastValueItemtoCurrency,
    getValueJeweltoCurrency,
    getValueOnetoCurrency,
    getBalanceChange,
    queryHeroLevel,
    queryHeroSummons,
    checkCostLevel,
    checkCostSummons,
    AVAX_get_transaction_history,
    queryPriceByDateJSON,
    get_transactions_count
)

import json
import logging
import requests
import warnings
warnings.filterwarnings("ignore")

app = Flask(__name__)
CORS(app)
cg = CoinGeckoAPI()

main_net = 'https://rpc.s0.t.hmny.io'
w3 = Web3(Web3.HTTPProvider(main_net))



MeditationCircleJson = open("abi/MeditationCircle.json")
MeditationCircleABI = json.load(MeditationCircleJson)

HeroSummoningUpgradeableJson = open("abi/HeroSummoningUpgradeable.json")
SummoningABI = json.load(HeroSummoningUpgradeableJson)

ERC721Json = open("abi/ERC721.json")
ERC721ABI = json.load(ERC721Json)

ERC20Json = open("abi/ERC20.json")
ERC20ABI = json.load(ERC20Json)

QuestCoreJson = open("abi/QuestCore.json")
QuestCoreABI = json.load(QuestCoreJson)

BankJson = open("abi/Bank.json")
BankABI = json.load(BankJson)

UniswapV2Router02Json = open("abi/UniswapV2Router02.json")
UniswapV2Router02ABI = json.load(UniswapV2Router02Json)

SaleAuctionJson = open("abi/SaleAuction.json")
SaleAuctionABI = json.load(SaleAuctionJson)

MasterGardenerJson = open("abi/MasterGardener.json")
MasterGardenerABI = json.load(MasterGardenerJson)

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
    "0xb12c13e66AdE1F72f71834f2FC5082Db8C091358" : "AVAX",
    "0xFbdd194376de19a88118e84E279b977f165d01b8" : "wMatic",
    "0x224e64ec1BDce3870a6a6c777eDd450454068FEC" : "wUST",
    "0x985458E523dB3d53125813eD68c274899e9DfAb4" : "USDC",
    "0x6983D1E6DEf3690C4d616b13597A09e6193EA013" : "ETH",
    "0x3095c7557bCb296ccc6e363DE01b760bA031F2d9" : "wBTC",
    "0x0aB43550A6915F9f67d0c454C2E90385E6497EaA" : "BUSD Token",
    "0x892D81221484F690C0a97d3DD18B9144A3ECDFB7" : "Magic",
    "0xCf1709Ad76A79d5a60210F23e81cE2460542A836" : "Tranquil",
    "0x0159ED2E06DDCD46a25E74eb8e159Ce666B28687" : "FarmersOnly Token2",
    "0xb1f6E61E1e113625593a22fa6aa94F8052bc39E0" : "BNB",
    "0x550D9923693998A6FE20801ABe3f1A78e0d75089" : "Immortl",
    "0x17fDEdda058d43fF1615cdb72a40Ce8704C2479A" : "SuperBid",
    "0x9b68BF4bF89c115c721105eaf6BD5164aFcc51E4" : "Freyala",
    "0x6008C8769BFACd92251bA838382e7e5637C7e74D" : "Cosmic Coin",
    "0x3C2B8Be99c50593081EAA2A724F0B8285F5aba8f" : "Tether USD",
    "0xd009b07B4a65CC769379875Edc279961D710362d" : "Rain Token",

    '0x66F5BfD910cd83d3766c4B39d13730C911b2D286' : "Shvas Rune",
    "0x24eA0D436d3c2602fbfEfBe6a16bBc304C963D04" : "Gaias Tears",
    "0x95d02C1Dc58F05A015275eB49E107137D9Ee81Dc" : "Grey Pet Egg",
    "0x9678518e04Fe02FB30b55e2D0e554E26306d0892" : "Blue Pet Egg",
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

dfk_contracts_abi = {
    "MeditationCircle"   : MeditationCircleABI,
    "Summoning"          : SummoningABI,
    "Quest"              : QuestCoreABI,
    "WishingWell"        : QuestCoreABI,
    "UniswapV2Router02"  : UniswapV2Router02ABI,
    "AuctionHouse"       : SaleAuctionABI,
    "MasterGardener"     : MasterGardenerABI,
    "xJEWEL"             : BankABI,
    "Banker"             : BankABI,
    "Hero"               : ERC721ABI,  
    "JewelToken"         : ERC20ABI,
    "Gaias Tears"        : ERC721ABI,
    "DFK Gold"           : ERC721ABI,
    "Ambertaffy"         : ERC721ABI,
    "Darkweed"           : ERC721ABI,
    "Goldvein"           : ERC721ABI,
    "Ragweed"            : ERC721ABI,
    "Redleaf"            : ERC721ABI,
    "Rockroot"           : ERC721ABI,
    "Swift-Thistle"      : ERC721ABI,
    "Bloater"            : ERC721ABI,
    "Ironscale"          : ERC721ABI,
    "Lanterneye"         : ERC721ABI,
    "Redgill"            : ERC721ABI,
    "Sailfish"           : ERC721ABI,
    "Shimmerskin"        : ERC721ABI,
    "Silverfin"          : ERC721ABI,
    "Shvas Rune"         : ERC721ABI,
    "Blue Pet Egg"       : ERC721ABI,
    "Grey Pet Egg"       : ERC721ABI,
    "Golden Egg"         : ERC721ABI
}

dfk_contracts_tokens = {
    "JewelToken"                  : "one1wt93p34l543ym5r77cyqyl3kd0tfqpy0eyd6n0",
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

Blacklist = [
    "Green Pet Egg",
    "Grey Pet Egg",
    "Blue Pet Egg",
    "Golden Egg",
    "Blue Stem",
    "Milkweed",
    "Spiderfruit"
]

def DFKContract(tx):
    for key,value in dfk_contracts.items():
        if tx["to"] == value or tx["from"] == value:
            return key

    return "Unknown Contract"

def gasPaid(gas, gasPrice):
    gas = int(gas, 16)
    gasPrice = int(gasPrice, 16)
    return (gas*gasPrice)/(10**18)

def getTxType(tx, contract_name, txData, address, currency):
    if contract_name in dfk_contracts_abi:
        contract = w3.eth.contract(address=convert_one_to_hex(dfk_contracts[contract_name]), abi=dfk_contracts_abi[contract_name])
        receipt = w3.eth.get_transaction_receipt(txData["hash"])
        try:
            contract_result = contract.decode_function_input(tx["input"])
        except:
            print("receipt error: ", contract_name)
            if contract_name == "Quest":
                return {"event": "Started New Quest"}
            elif contract_name == "WishingWell":
                return {"event": "Started Wishing Well Quest"}
            else:
                return {"event": "Failed Receipt"}
        if contract_name == "MeditationCircle":
            decode = decodeMeditationCircle(contract_result, tx)
            return decode
        elif contract_name == "Hero":
            decode = decodeHero(contract_result)
            return decode
        elif contract_name == "Quest" or contract_name == "WishingWell":
            decode = decodeQuest(contract_result, contract, receipt, txData, currency)
            return decode
        elif contract_name == "xJEWEL":
            decode = decodexJEWEL(contract_result)
            return decode
        elif contract_name == "UniswapV2Router02":
            decode = decodeUniswap(contract_result, txData)
            return decode
        elif contract_name == "AuctionHouse":
            decode = decodeAuctionHouse(contract_result, contract, receipt)
            return decode
        elif contract_name == "MasterGardener":
            decode = decodeMasterGardener(contract_result, contract, receipt)
            return decode 
        elif contract_name == "Summoning":
            decode = decodeSummoning(contract_result, tx, contract, receipt)
            return decode 
        elif contract_name == "JewelToken":
            decode = decodeJewel(contract_result)
            return decode
        elif contract_name in dfk_contracts_tokens:
            decode = decodeItem(contract_result, contract, receipt, contract_name)
            return decode
        else:
            result = contract_result
            print("Missing Contract decode", contract_name, result)
            return {"event": "Missing Contract decode"}
    elif contract_name == "Profiles":
        return {"event": "Create Profile"}
    else:
        return {"event": "Missing Contract ABI"}

def decodeItem(result, contract, receipt, name):
    decode = ""
    if str(result[0]) == "<Function approve(address,uint256)>":
        if result[1]["to"] == "0x0594D86b2923076a2316EaEA4E1Ca286dAA142C1":
            #receipt_result = contract.events.Approval().processReceipt(receipt)
            #print(receipt_result)
            decode = {
                "event" : "Approved for Meditation Circle",
                "item"  : name
            }
        elif result[1]["to"] == "0xe53BF78F8b99B6d356F93F41aFB9951168cca2c6":
            #Falta conseguir el oro obtenido al vender un item
            decode = {
                "event" : "Sold for Gold",
                "item"  : name
            }
        elif result[1]["to"] == "0x24ad62502d1C652Cc7684081169D04896aC20f30":
            decode = {
                "event" : "Approved for Trade",
                "item"  : name
            }
        elif result[1]["to"] == "0x65DEA93f7b886c33A78c10343267DD39727778c2":
            decode = {
                "event" : "Approved for Summoning",
                "item"  : name
            }
    if decode == "":
        print("decode Item", name, result)
        decode = {"event": "Transaction Failed"}
    return decode

def decodeJewel(result):
    decode = ""
    if str(result[0]) == "<Function approve(address,uint256)>":
        if result[1]["spender"] == "0x0594D86b2923076a2316EaEA4E1Ca286dAA142C1":
            #receipt_result = contract.events.Approval().processReceipt(receipt)
            #print(receipt_result)
            decode = {
                "event" : "Approved for Meditation Circle",
                "item"  : "Jewel"
            }
        elif result[1]["spender"] == "0xA9cE83507D872C5e1273E745aBcfDa849DAA654F":
            decode = {
                "event" : "Approved for Bank",
                "item"  : "Jewel"
            }
        elif result[1]["spender"] == "0x13a65B9F8039E2c032Bc022171Dc05B30c3f2892":
            decode = {
                "event" : "Approved for Auction House",
                "item"  : "Jewel"
            }
        elif result[1]["spender"] == "0x24ad62502d1C652Cc7684081169D04896aC20f30":
            decode = {
                "event" : "Approved for Trade",
                "item"  : "Jewel"
            }
        elif result[1]["spender"] == "0x65DEA93f7b886c33A78c10343267DD39727778c2":
            decode = {
                "event" : "Approved for Summoning",
                "item"  : "Jewel"
            }
    elif str(result[0]) == "<Function transfer(address,uint256)>":
        decode = {
            "event"    : "Transfer Jewel",
            "recipient": result[1]["recipient"],
            "amount"   : round(result[1]["amount"]/(10**18),3)
        }

    if decode == "":
        print("decode Jewel", result)
        decode = {"event": "Transaction Failed"}
    return decode

def decodeMasterGardener(result, contract, receipt):
    decode = ""
    if str(result[0]) == "<Function deposit(uint256,uint256,address)>":
        decode = ["Deposit: ", round(result[1]["_amount"]/(10**18),3), " LP"]
        decode = {
            "event" : "Deposit LP",
            "amount": round(result[1]["_amount"]/(10**18),3)
        }
    
    elif str(result[0]) == "<Function withdraw(uint256,uint256,address)>":
        decode = ["Deposit: ", round(result[1]["_amount"]/(10**18),3), " LP"]
        decode = {
            "event" : "Withdraw LP",
            "amount": round(result[1]["_amount"]/(10**18),3)
        }

    elif str(result[0]) == "<Function claimRewards(uint256[])>":
        receipt_result = contract.events.SendGovernanceTokenReward().processReceipt(receipt)
        for i in receipt_result:
            decode = {
                "event"          : "Claim LP rewards",
                "unlockedAmount" : round(i["args"]["amount"]/(10**18)-i["args"]["lockAmount"]/(10**18),3),
                "lockedAmount"   : round(i["args"]["lockAmount"]/(10**18),3)
            }
    if decode == "":
        print("decode MasterGardener", result)
        decode = {"event": "Transaction Failed"}
    return decode

def decodeMeditationCircle(result, tx):
    decode = ""
    if str(result[0]) == "<Function completeMeditation(uint256)>":
        decode = {
            "event" : "Complete Meditation",
            "heroId": result[1]['_heroId']
        }
    elif str(result[0]) == "<Function startMeditation(uint256,uint8,uint8,uint8,address)>":
        heroLevel = queryHeroLevel(result[1]["_heroId"], int(tx["blockNumber"],16)-1)
        if heroLevel == "Error":
            #Mejorar handling de este error
            cost = [0, "Shvas Rune", 0]
        else:
            cost = checkCostLevel(heroLevel)
        decode = {
            "event"      : "Start Meditation",
            "heroId"     : result[1]['_heroId'],
            "amountJewel": cost[0],
            "rune"       : cost[1],
            "amountRune" : cost[2],
        }
    if decode == "":
        print("decode MeditationCircle", result)
        decode = {"event": "Transaction Failed"}
    return decode

def decodeSummoning(result, tx, contract, receipt):
    decode = ""
    if str(result[0]) == "<Function cancelAuction(uint256)>":
        decode = {
            "event" : "Cancel Renting Auction",
            "heroId": result[1]["_tokenId"]
        }
    elif str(result[0]) == "<Function createAuction(uint256,uint128,uint128,uint64,address)>":
        decode = {
            "event" : "Create Renting Auction",
            "heroId": result[1]["_tokenId"],
            "price" : round(result[1]["_startingPrice"]/(10**18),3),
            "currency" : "Jewel"
        }
    elif str(result[0]) == "<Function open(uint256)>":
        receipt_result = contract.events.CrystalOpen().processReceipt(receipt)
        for i in receipt_result:
            decode = {
                "event"     : "Crystal Open",
                "crystalId" : result[1]["_crystalId"],
                "heroId"    : i["args"]["heroId"]
            }
    elif str(result[0]) == "<Function summonCrystal(uint256,uint256,uint16,uint16,address)>":
        receipt_result = contract.events.CrystalSummoned().processReceipt(receipt)
        heroInfo = queryHeroSummons(result[1]["_summonerId"], int(tx["blockNumber"],16)-1)
        if heroInfo == "Error":
            #Mejorar handling de este error
            cost = 0
        else:
            cost = checkCostSummons(heroInfo[0], heroInfo[1])
        for i in receipt_result:
            decode = {
                "event"         : "Summon Crystal",
                "crystalId"     : i["args"]["crystalId"],
                "summonerId"    : result[1]["_summonerId"],
                "assistantId"   : result[1]["_assistantId"],
                "summonerTears" : result[1]["_summonerTears"],
                "assistantTears": result[1]["_assistantTears"],
                "amountJewel"   : cost
            }

    if decode == "":
        print("decodeSummoning", result)
        decode = {"event": "Transaction Failed"}
    return decode

def decodeAuctionHouse(result, contract, receipt):
    decode = ""
    if str(result[0]) == "<Function bid(uint256,uint256)>":
        decode = {
            "event" : "Bought Hero",
            "heroId": result[1]["_tokenId"],
            "price" : round(result[1]["_bidAmount"]/(10**18), 3),
            "currency" : "Jewel"
        }
    elif str(result[0]) == "<Function createAuction(uint256,uint128,uint128,uint64,address)>":
        receipt_result = contract.events.AuctionCreated().processReceipt(receipt)
        for i in receipt_result:
            auctionStatus = queryAuctionStatus(i["args"]["auctionId"])
            decode = {
                "event"    : "Create Auction",
                "heroId"   : result[1]["_tokenId"],
                "price"    : round(result[1]["_startingPrice"]/(10**18),3),
                "currency" : "Jewel",
                "status"   : auctionStatus
            }
    elif str(result[0]) == "<Function cancelAuction(uint256)>":
        decode = {
            "event" : "Cancel Auction",
            "heroId": result[1]["_tokenId"]
        }

    if decode == "":
        print("decodeAuctionHouse", result)
        decode = {"event": "Transaction Failed"}
    return decode

def decodeHero(result):
    decode = ""
    if str(result[0]) == "<Function setApprovalForAll(address,bool)>":
        if str(result[1]["operator"]) == '0x13a65B9F8039E2c032Bc022171Dc05B30c3f2892':
            decode = {
                "event": "Approved for auction House"
            }
    elif str(result[0]) == "<Function transferFrom(address,address,uint256)>":
        decode = {
            "event": "Transfer Hero",
            "heroId": result[1]["tokenId"]
        }
    if decode == "":
        print("decodeHero", result)
        decode = {"event": "Transaction Failed"}
    return decode

def decodexJEWEL(result):
    decode = ""
    if str(result[0]) == "<Function enter(uint256)>":
        decode = {
            "event"    : "Add to Bank",
            "amount"   : round(result[1]["_amount"]/(10**18), 3),
            "currency" : "Jewel"
        }
    elif str(result[0]) == "<Function leave(uint256)>":
        decode = {
            "event"    : "Remove from Bank",
            "amount"   : round(result[1]["_share"]/(10**18), 3),
            "currency" : "xJewel"
        }
    if decode == "":
        print("xJewel", result)
        decode = {"event": "Transaction Failed"}
    return decode

def decodeQuest(result, contract, receipt, txData, currency):
    decode = ""
    heroes = []
    rewards = {}
    if str(result[0]) == "<Function completeQuest(uint256)>":
        receipt_result = contract.events.QuestReward().processReceipt(receipt)
        for i in receipt_result:
            if i["args"]["heroId"] not in heroes:
                heroes.append(i["args"]["heroId"])
            if i["args"]["rewardItem"] != "0x0000000000000000000000000000000000000000":
                item = dfk_contractsETH[i["args"]["rewardItem"]]
                if item == "Jewel":
                    quantity = round(i["args"]["itemQuantity"]/(10**18),5)
                else:
                    quantity = i["args"]["itemQuantity"]

                if item not in rewards:
                    rewards[item] = quantity
                else:
                    rewards[item] = rewards[item]+quantity
        decode = {
            "event"    : "Quest Completed", 
            "heroIds"  : heroes, 
            "rewards"  : rewards,
            }
    elif str(result[0]) == "<Function startQuest(uint256[],address,uint8)>" or str(result[0]) == "<Function startQuestWithData(uint256[],address,uint8,tuple)>":
        if str(result[1]["_questAddress"]) == '0x0548214A0760a897aF53656F4b69DbAD688D8f29':
            decode = {
            "event"    : "Start Wishing Well Quest", 
            "heroIds"  : result[1]['_heroIds'],
            }
        elif str(result[1]["_questAddress"]) == '0xE259e8386d38467f0E7fFEdB69c3c9C935dfaeFc':
            decode = {
            "event"    : "Start Fishing Quest", 
            "heroIds"  : result[1]['_heroIds'],
            }
        elif str(result[1]["_questAddress"]) == '0x3132c76acF2217646fB8391918D28a16bD8A8Ef4':
            decode = {
            "event"    : "Start Foraging Quest", 
            "heroIds"  : result[1]['_heroIds'],
            }
        elif str(result[1]["_questAddress"]) == '0x569E6a4c2e3aF31B337Be00657B4C040C828Dd73':
            decode = {
            "event"    : "Start Mining Quest", 
            "heroIds"  : result[1]['_heroIds'],
            }
        elif str(result[1]["_questAddress"]) == '0xe4154B6E5D240507F9699C730a496790A722DF19':
            decode = {
            "event"    : "Start Gardening Quest", 
            "heroIds"  : result[1]['_heroIds'],
            }


    elif str(result[0]) == "<Function cancelQuest(uint256)>":
        decode = {
            "event"    : "Cancel Quest", 
            "heroId"  : result[1]['_heroId'],
            }

    if decode == "":
        print("decodeQuest", result)
        decode = {"event": "Transaction Failed"}
    return decode

def decodeUniswap(result, txData):
    decode = ""
    if str(result[0]) == "<Function addLiquidityETH(address,uint256,uint256,uint256,address,uint256)>":
        if result[1]["token"] in dfk_contractsETH:
            token = dfk_contractsETH[result[1]["token"]]
        else:
            token = result[1]["token"]
        
        decode = {
            "event"    : "add Liquidity One",
            "token"    : token,
            "amount"   : round(result[1]['amountTokenDesired']/(10**18), 3),
            "amountOne": txData["valueOne"]
        }
        return decode

    elif str(result[0]) == "<Function addLiquidity(address,address,uint256,uint256,uint256,uint256,address,uint256)>":
        if result[1]["tokenA"] in dfk_contractsETH:
            tokenA = dfk_contractsETH[result[1]["tokenA"]]
        else:
            tokenA = result[1]["tokenA"]
        if result[1]["tokenB"] in dfk_contractsETH:
            tokenB = dfk_contractsETH[result[1]["tokenB"]]
        else:
            tokenB = result[1]["tokenB"]
        decode = {
            "event"  : "add Liquidity",
            "tokenA" : tokenA,
            "amountA": round(result[1]['amountADesired']/(10**18), 3),
            "tokenB" : tokenB,
            "amountB": round(result[1]['amountBDesired']/(10**18), 3),
        }
        return decode

    elif str(result[0]) == "<Function removeLiquidity(address,address,uint256,uint256,uint256,address,uint256)>":
        if result[1]["tokenA"] in dfk_contractsETH:
            tokenA = dfk_contractsETH[result[1]["tokenA"]]
        else:
            tokenA = result[1]["tokenA"]
        if result[1]["tokenB"] in dfk_contractsETH:
            tokenB = dfk_contractsETH[result[1]["tokenB"]]
        else:
            tokenB = result[1]["tokenB"]
        decode = {
            "event" : "Liquidity Removed",
            "tokenA" : tokenA,
            "amountA": round(result[1]['amountAMin']/(10**18), 3),
            "tokenB" : tokenB,
            "amountB": round(result[1]['amountBMin']/(10**18), 3),
        }
        return decode

    elif str(result[0]) == "<Function removeLiquidityETH(address,uint256,uint256,uint256,address,uint256)>" or str(result[0]) == "<Function removeLiquidityETHSupportingFeeOnTransferTokens(address,uint256,uint256,uint256,address,uint256)>":
        if result[1]["token"] in dfk_contractsETH:
            token = dfk_contractsETH[result[1]["token"]]
        else:
            token = result[1]["token"]

        decode = {
            "event" : "Liquidity One Removed",
            "amountOne": round(result[1]['amountETHMin']/(10**18), 3),
            "token" : token,
            "amountToken": round(result[1]['amountTokenMin']/(10**18), 3),
        }
        return decode
    
  
    if str(result[0]) == "<Function swapTokensForExactTokens(uint256,uint256,address[],address,uint256)>":
        if result[1]["amountOut"] > 10**12:
            amountOut = round(result[1]["amountOut"]/(10**18),3)
        else:
            amountOut = result[1]["amountOut"]
        if result[1]["amountInMax"] > 10**12:
            amountInMax = round(result[1]["amountInMax"]/(10**18),3)
        else:
            amountInMax = result[1]["amountInMax"]

        if result[1]["path"][-1] in dfk_contractsETH:
            tokenOut = dfk_contractsETH[result[1]["path"][-1]]
            if dfk_contractsETH[result[1]["path"][-1]] == "DFK Gold":
                amountOut = amountOut/1000
            elif dfk_contractsETH[result[1]["path"][-1]] == "USDC" or tokenOut == "Tether USD":
                amountOut = amountOut/1000000
            elif dfk_contractsETH[result[1]["path"][-1]] == "wBTC":
                amountOut = amountOut/100000000
        else:
            tokenOut = result[1]["path"][-1]

        if result[1]["path"][0] in dfk_contractsETH:
            tokenIn = dfk_contractsETH[result[1]["path"][0]]
            if tokenIn == "DFK Gold":
                amountInMax = amountInMax/1000
            elif tokenIn == "USDC" or tokenIn == "Tether USD":
                amountInMax = amountInMax/1000000

            elif tokenIn == "wBTC":
                amountInMax = amountInMax/100000000
        else:
            tokenIn = result[1]["path"][0]

        decode = {
            "event"        : "Trade",
            "bought"       : tokenOut,
            "boughtAmount" : amountOut,
            "sold"         : tokenIn,
            "soldAmount"   : amountInMax
        }
    elif str(result[0]) == "<Function swapExactTokensForTokens(uint256,uint256,address[],address,uint256)>":
        if result[1]["amountOutMin"] > 10**12:
            amountOutMin = round(result[1]["amountOutMin"]/(10**18),3)
        else:
            amountOutMin = result[1]["amountOutMin"]
        if result[1]["amountIn"] > 10**12:
            amountIn = round(result[1]["amountIn"]/(10**18),3)
        else:
            amountIn = result[1]["amountIn"]
        
        if result[1]["path"][-1] in dfk_contractsETH:
            tokenOut = dfk_contractsETH[result[1]["path"][-1]]
            if tokenOut == "DFK Gold":
                amountOutMin = amountOutMin/1000
            elif tokenOut == "wBTC":
                amountOutMin = amountOutMin/100000000
            elif tokenOut == "USDC" or dfk_contractsETH[result[1]["path"][-1]] == "Tether USD":
                amountOutMin = amountOutMin/1000000
        else:
            tokenOut = result[1]["path"][-1]

        if result[1]["path"][0] in dfk_contractsETH:
            tokenIn = dfk_contractsETH[result[1]["path"][0]]
            if tokenIn == "USDC" or tokenIn == "Tether USD":
                amountIn = amountIn/1000000
            elif tokenIn == "wBTC":
                amountIn = amountIn/100000000
            elif tokenIn == "DFK Gold":
                amountIn = amountIn/1000
        else:
            tokenIn = result[1]["path"][0]

        decode = {
            "event"        : "Trade",
            "bought"       : tokenOut,
            "boughtAmount" : amountOutMin,
            "sold"         : tokenIn,
            "soldAmount"   : amountIn
        }

    elif str(result[0]) == "<Function swapExactETHForTokens(uint256,address[],address,uint256)>" or str(result[0]) == "<Function swapExactETHForTokensSupportingFeeOnTransferTokens(uint256,address[],address,uint256)>":
        if result[1]["amountOutMin"] > 10**12:
            amountOutMin = round(result[1]["amountOutMin"]/(10**18), 3)
        else:
            amountOutMin = result[1]["amountOutMin"]

        if result[1]["path"][-1] in dfk_contractsETH:
            token = dfk_contractsETH[result[1]["path"][-1]]
            if token == "DFK Gold":
                amountOutMin = amountOutMin/1000
            elif token == "USDC" or token == "Tether USD":
                amountOutMin = amountOutMin/1000000
            elif token == "wBTC":
                amountOutMin = amountOutMin/100000000
        else:
            token = result[1]["path"][-1]

        decode = {
            "event"        : "Trade",
            "bought"       : token,
            "boughtAmount" : amountOutMin,
            "sold"         : dfk_contractsETH[result[1]["path"][0]],
            "soldAmount"   : round(txData["valueOne"], 3)
        }

    elif str(result[0]) == "<Function swapETHForExactTokens(uint256,address[],address,uint256)>":
        if result[1]["amountOut"] > 10**12:
            amountOut = round(result[1]["amountOut"]/(10**18), 3)
        else:
            amountOut = result[1]["amountOut"]
        
        if result[1]["path"][-1] in dfk_contractsETH:
            token = dfk_contractsETH[result[1]["path"][-1]]
            if token == "DFK Gold":
                amountOut = amountOut/1000
            elif token == "USDC" or token == "Tether USD":
                amountOut = amountOut/1000000
            elif token == "wBTC":
                amountOut = amountOut/100000000
        else:
            token = result[1]["path"][-1]

        decode = {
            "event"        : "Trade",
            "bought"       : token,
            "boughtAmount" : round(amountOut, 3),
            "sold"         : dfk_contractsETH[result[1]["path"][0]],
            "soldAmount"   : round(txData["valueOne"], 3)
        }

    elif str(result[0]) == "<Function swapExactTokensForETH(uint256,uint256,address[],address,uint256)>":
        if result[1]["amountIn"] > 10**12:
            amountIn = round(result[1]["amountIn"]/(10**18), 3)
        else:
            amountIn = result[1]["amountIn"]
        if result[1]["amountOutMin"] > 10**12:
            amountOutMin = round(result[1]["amountOutMin"]/(10**18), 3)
        else:
            amountOutMin = result[1]["amountOutMin"]
        
        if result[1]["path"][0] in dfk_contractsETH:
            token = dfk_contractsETH[result[1]["path"][0]]
            if token == "DFK Gold":
                amountIn = amountIn/1000
            elif token == "USDC" or token == "Tether USD":
                amountIn = amountIn/1000000
            elif token == "wBTC":
                amountIn = amountIn/100000000
        else:
            token = result[1]["path"][0]

        decode = {
            "event"        : "Trade",
            "bought"       : dfk_contractsETH[result[1]["path"][-1]],
            "boughtAmount" : amountOutMin,
            "sold"         : token,
            "soldAmount"   : amountIn
        }
    elif str(result[0]) == "<Function swapTokensForExactETH(uint256,uint256,address[],address,uint256)>":
        if result[1]["amountInMax"] > 10**12:
            amountInMax = round(result[1]["amountInMax"]/(10**18), 3)
        else:
            amountInMax = result[1]["amountInMax"]
        if result[1]["amountOut"] > 10**12:
            amountOut = round(result[1]["amountOut"]/(10**18), 3)
        else:
            amountOut = result[1]["amountOut"]
        
        if result[1]["path"][0] in dfk_contractsETH:
            token = dfk_contractsETH[result[1]["path"][0]]
            if token == "DFK Gold":
                amountInMax = amountInMax/1000
            elif token == "USDC" or dfk_contractsETH[result[1]["path"][0]] == "Tether USD":
                amountInMax = amountInMax/1000000
            elif token == "wBTC":
                amountInMax = amountInMax/100000000
        else:
            token = result[1]["path"][0]

        decode = {
            "event"        : "Trade",
            "bought"       : dfk_contractsETH[result[1]["path"][-1]],
            "boughtAmount" : amountOut,
            "sold"         : token,
            "soldAmount"   : amountInMax
        }

    if decode == "":
        print("decodeUniswap", result)
        decode = {"event": "Transaction Failed"}
    return decode

def generate_report(address, startTime, endTime, currency, page, hashes, balances):
    pageSize = 50
    txs_history = {}
    balanceSheet = {}
    txsProcessed = []
    status = "on"
    balanceSheet = defaultdict(int)

    if page == 1000:
        tx_count = get_transactions_count(address=address, tx_type="ALL", endpoint=main_net)
        page = ceil(tx_count/pageSize)

    c=len(hashes)+1
    txs = account.get_transaction_history(address, page=page, page_size=pageSize, include_full_tx=True, tx_type='ALL', order='DESC', endpoint=main_net)



    for tx in txs[::-1]:
        contract_name = DFKContract(tx)
        if int(tx["timestamp"], 16) < startTime:
            continue
        elif int(tx["timestamp"], 16) > endTime:
            status = "finished"
            break
        elif contract_name == "Unknown Contract":
            continue
        elif tx["hash"] in txsProcessed:
            continue
        elif tx["hash"] in hashes:
            continue
        else:
            txsProcessed.append(tx["hash"])

        txData = {"chain" : "Hmy"}
        txData["hash"] = tx["hash"]
        txData["from"] = tx["from"]
        txData["to"] = tx["to"]
        txData["gasPaid"] = round(gasPaid(tx["gas"], tx["gasPrice"]), 5)
        txData["contract"] = contract_name
        txData["valueOne"] = round(int(tx["value"], 16)/(10**18), 3)
        txData["timestamp"] = int(tx["timestamp"], 16)
        txData["txType"] = getTxType(tx, contract_name, txData, address, currency)
        txData["gasPaidCurrency"] = getValueOnetoCurrency(txData["gasPaid"], currency, txData["timestamp"])

        balanceChange = getBalanceChange(txData["txType"], txData["timestamp"], currency, balances)
        balanceChange["Gas"] = (-1*txData["gasPaid"], -1*txData["gasPaidCurrency"])

        txData["balanceChange"] = balanceChange
        txs_history[c] = txData
        c+=1

        for key, value in balanceChange.items():
            if key in balanceSheet:
                balanceSheet[key] = (round(balanceSheet[key][0]+value[0], 5), round(balanceSheet[key][1]+value[1], 5))
            else:
                balanceSheet[key] = (round(value[0], 5), round(value[1], 5))
    return {"txs": txs_history, "balanceSheet": balanceSheet, "status": status, "page": page}

def getBalances(address, currency):
    balances = {}
    oneBalance = round(w3.eth.get_balance(convert_one_to_hex(address))/(10**18),3)
    balances["One"] = (oneBalance, round(getValueOnetoCurrency(oneBalance, currency, "last"),3))
    for key, value in dfk_contracts_tokens.items():
        contract = w3.eth.contract(address=convert_one_to_hex(value), abi=dfk_contracts_abi[key])
        token_balance = contract.functions.balanceOf(convert_one_to_hex(address)).call()
        if token_balance == 0:
            continue
        if key == "JewelToken":
            jewelBalance = round(token_balance/(10**18), 3)
            balances[key] = (jewelBalance, round(getValueJeweltoCurrency(jewelBalance, currency, "last"),3))
        elif key == "DFK Gold":
            balances[key] = (token_balance/1000, getLastValueItemtoCurrency(convert_one_to_hex(value), currency)*(token_balance/1000))
        else:
            balances[key] = (token_balance, getLastValueItemtoCurrency(convert_one_to_hex(value), currency)*token_balance)
    return {"currentBalance": balances}

def updateData():
    onePriceUSD = cg.get_coin_market_chart_range_by_id("harmony", "usd", 1629518400, datetime.timestamp(datetime.now()))
    with open('cg/onePriceUSD.json', 'w', encoding='utf-8') as f:
        json.dump(onePriceUSD, f, ensure_ascii=False, indent=4)
    jewelPriceUSD = cg.get_coin_market_chart_range_by_id("defi-kingdoms", "usd", 1629518400, datetime.timestamp(datetime.now()))
    with open('cg/jewelPriceUSD.json', 'w', encoding='utf-8') as f:
        json.dump(jewelPriceUSD, f, ensure_ascii=False, indent=4)
    onePriceEUR = cg.get_coin_market_chart_range_by_id("harmony", "eur", 1629518400, datetime.timestamp(datetime.now()))
    with open('cg/onePriceEUR.json', 'w', encoding='utf-8') as f:
        json.dump(onePriceEUR, f, ensure_ascii=False, indent=4)
    jewelPriceEUR = cg.get_coin_market_chart_range_by_id("defi-kingdoms", "eur", 1629518400, datetime.timestamp(datetime.now()))
    with open('cg/jewelPriceEUR.json', 'w', encoding='utf-8') as f:
        json.dump(jewelPriceEUR, f, ensure_ascii=False, indent=4)

@app.route("/update", methods=['GET'])
async def priceUpdate():
    updateData()
    return {"Success": "Prices Updated"}

@app.route("/transactionReport", methods=['GET', "POST"])
async def transactionReport():
    data = request.json
    address = data["address"]
    start = data["startTime"]
    end = data["endTime"]
    currency = data["currency"]
    page = data["page"]
    hashes = data["hashes"]
    balances = data["balances"]
    #try:
    return generate_report(address, start, end, currency, page, hashes, balances)
    #except:
        #print("Error generating report")
        #return {"txs": {}, "balanceSheet": {}, "status": "error"}

@app.route("/currentBalance", methods=['GET', "POST"])
async def currentBalance():
    data = request.json
    address = data["address"]
    currency = data["currency"]
    return getBalances(address, currency)


updateData()
url = "http://graph3.defikingdoms.com/subgraphs/name/defikingdoms/dex"
urlAuctionHouse = "http://graph3.defikingdoms.com/subgraphs/name/defikingdoms/apiv5"
headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'User-Agent': 'Mozilla/5.0'
}
app.run(host='0.0.0.0')






    
