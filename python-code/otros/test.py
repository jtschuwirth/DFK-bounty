from pyhmy import account
from web3 import Web3
import json
main_net = 'https://rpc.s0.t.hmny.io'
w3 = Web3(Web3.HTTPProvider(main_net))

page = 55
pageSize = 10
address = "one16eqvyu8fq7qsd0wncmant9vuhdvlng4n69xv63"

txs = account.get_transaction_history(address, page=page, page_size=pageSize, include_full_tx=True, tx_type='ALL', order='DESC', endpoint=main_net)
c=1
ERC20Json = open("abi/ERC20.json")
ERC20ABI = json.load(ERC20Json)

for tx in txs:
    #print(c, tx)
    print(c, int(tx["timestamp"], 16))
    if tx["to"] == "one1wt93p34l543ym5r77cyqyl3kd0tfqpy0eyd6n0":
        contract = w3.eth.contract(address="0x72Cb10C6bfA5624dD07Ef608027E366bd690048F", abi=ERC20ABI)
        contract_result = contract.decode_function_input(tx["input"])
        print(c, contract_result)
    if tx["to"] == "one14028gx2gxa937hw4m46entqlsk35etxaln7glh":
        print("Profile!")
    c+=1