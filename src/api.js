const BN = require('bn.js');
const Web3 = require("web3");

const { Harmony } = require('@harmony-js/core');
const { getAddress, HarmonyAddress } = require('@harmony-js/crypto');
var simple_jsonrpc = require('simple-jsonrpc-js');

const BankABI = require('../abi/Bank.json');
const ERC20ABI = require('../abi/ERC20.json');
const ERC721ABI = require('../abi/ERC721.json');
const SummoningABI = require('../abi/HeroSummoningUpgradeable.json');
const MeditationCircleABI = require('../abi/MeditationCircle.json');
const QuestCoreABI = require('../abi/QuestCoreV2.json');
const SaleAuctionABI = require('../abi/SaleAuction.json');
const UniswapV2Router02ABI = require('../abi/UniswapV2Router02.json');
const MasterGardenerABI = require('../abi/MasterGardener.json');

const HMY_RPC_URL = "https://api.s0.t.hmny.io/"
const web3 = new Web3(HMY_RPC_URL);
var jrpc = simple_jsonrpc.connect_xhr(HMY_RPC_URL);


const dfk_contracts = {
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
    "Quest"                       : "one12yqt6vdcygm3zz9q7c7uldjefwv3n6h5trltq4"
}

const dfk_contracts_abi = {
    "MeditationCircle"   : MeditationCircleABI,
    "Summoning"          : SummoningABI,
    "Hero"               : ERC721ABI,
    "Quest"              : QuestCoreABI,
    "UniswapV2Router02"  : UniswapV2Router02ABI,
    "AuctionHouse"       : SaleAuctionABI,
    "xJEWEL"             : BankABI,
    "JewelToken"         : ERC20ABI,
    "MasterGardener"     : MasterGardenerABI
}

async function Api(address, start, end , currency) {
    let transactions = {};
    let metadata = {
        totalBalanceOne: "",
        totalBalanceCurrency: "",
        totalGasPaidOne: "",
        totalGasPaidCurrency: "",
    };
    
    let txs_history = await jrpc.call("hmyv2_getTransactionsHistory", [{
        address: address, 
        fullTx: true, 
        pageSize: 10, 
        pageIndex: 0, 
        txType: 'ALL', 
        order: 'DESC'
    }])
    let txs = txs_history.transactions
    for (let i=0; i<txs.length; i++) {
        let contract = getContractName(txs[i]);
        if (contract.name == "unknown") {
            continue
        }
        let contract_info = contractInfo(txs[i], contract);
        transactions[i] = {
            chain     : "Harmony",
            hash      : txs[i].hash,
            from      : txs[i].from,
            to        : txs[i].to,
            gasPaid   : getGasPaid(txs[i].gas, txs[i].gasPrice),
            contract  : contract.name,
            valueOne  : getValueOne(txs[i].value),
            txType    : contract_info.txType,
            valueJewel: contract_info.valueJewel,
            timestamp : txs[i].timestamp
        }
    }
    return {txs: transactions, metadata: metadata}
}

function getGasPaid(gas, gasPrice) {
    gas = Number(gas);
    gasPrice = Number(gasPrice);
    return ((gas*gasPrice)/(10**18)).toFixed(5);
}

function getContractName(txs) {
    let contract_name = "unknown";
    let address = "";
    for (let i = 0; i<Object.keys(dfk_contracts).length; i++) {
        if (txs.from == Object.values(dfk_contracts)[i] || txs.to == Object.values(dfk_contracts)[i]) {
            contract_name = Object.keys(dfk_contracts)[i];
            address = Object.values(dfk_contracts)[i];
            break
        }
    }
    return {name: contract_name, address: address}
}

function getValueOne(value) {
    return (Number(value)/(10**18)).toFixed(3);
}

function contractInfo(tx, contract) {
    let address = new HarmonyAddress(contract.address)
    let contract_data = new web3.eth.Contract(dfk_contracts_abi[contract.name], address.basicHex)
    let json_interface = contract_data.options.jsonInterface;
    let contract_result = web3.eth.abi.decodeLog(json_interface, tx.input);
    console.log(contract.name, contract_result)
    return {txType: "", valueJewel: 0}
}


module.exports.Api = Api;