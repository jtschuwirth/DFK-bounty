from web3 import Web3
import json

main_net = 'https://rpc.s0.t.hmny.io'
w3 = Web3(Web3.HTTPProvider(main_net))

UniswapFactory = "0x9014B937069918bd319f80e8B3BB4A2cf6FAA5F7"
wLuna = "0x95CE547D730519A90dEF30d647F37D9E5359B6Ae"
Jewel = "0x72Cb10C6bfA5624dD07Ef608027E366bd690048F"

UniswapFactoryJson = open("abi/UniswapFactory.json")
UniswapFactoryABI = json.load(UniswapFactoryJson)

contract = w3.eth.contract(address=UniswapFactory, abi=UniswapFactoryABI)
result = contract.functions.getPair(Jewel, wLuna).call()
print(result)
