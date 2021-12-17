import React, { useState, useEffect } from "react";
import ReactDOM from "react-dom";
import DayPickerInput from "react-day-picker/DayPickerInput";
import { Table, Dropdown } from 'react-bootstrap';
import axios from 'axios';
const bootstrap = require('bootstrap')
const { getAddress } = require('@harmony-js/crypto');


const BN = require('bn.js');
const Web3 = require("web3");
const API_URL = "http://127.0.0.1:8000/"

const HMY_RPC_URL = "https://api.s0.t.hmny.io/"
const web3 = new Web3(HMY_RPC_URL);

const DUMMY_DATA = [
{blockHash: '0x85b8aeb7ac7fe749c39f0a9d01925a4d97967d46274d066b9d7a3d331fab4ea3', blockNumber: '0x138a61f', ethHash: '0xf8f25c8c7fd376a6ad8e60bce52aa53d995db2b4591756d19ccf80660051704b', from: 'one1se7lv0g7athe8xzz2rmckj7c83cx2twwks52kj', gas: '0x5208', gasPrice: '0x2540be400', hash: '0x775a2d098197824197d0e023fd5a086818e152367afe36e539b22b559cac79ae', input: '0x', nonce: '0x74', r: '0x1c93d5839962b711852d08e773731ad21f7952b1354bd1436b334c206e0321c9', s: '0x2f7bcb72ef112fa40c4c88bb5b6e96cde3b8e584a899d3132e56c62df29f3885', shardID: 0, timestamp: '0x61b8fb28', to: 'one103gdq8rm5rk7sd4a5mdv3z549ue9w4hrewyhu6', toShardID: 0, transactionIndex: '0x15', v: '0xc6ac98a3', value: '0x429d069189e0000'},
{blockHash: '0x2c66987bc3cb4e5281f04f7dcc2c2468ae4152a725f70679c89386be86f7ac5d', blockNumber: '0x137e96c', ethHash: '0xcd5a9c8ba2c7058e67797cf33b4e1af3459b26ad01553f921fbf3b159ecc299e', from: 'one1se7lv0g7athe8xzz2rmckj7c83cx2twwks52kj', gas: '0x7eacf', gasPrice: '0x2540be400', hash: '0x689dd4b9d1fbe5904c83ea1560d0baf8bae09aaedfda95a08b3392d83d656ac6', input: '0x8dbdbe6d0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000054f5e288bf391da0000000000000000000000000000000000000000000000000000000000000000', nonce: '0x73', r: '0xa5c9c7327b1a0f8992d1cbbbe84cc6daf5696aa22c07df4df3b639ea6c282e4d', s: '0x715bd3db807feb4c54af4bc29512e3c76bd6cda3e24aada4dd33e63d2c2c3b0e', shardID: 0, timestamp: '0x61b76320', to: 'one1mvcxg0r34j0zzgk2qdq76a7sn40en7fy7lytq4', toShardID: 0, transactionIndex: '0x12', v: '0xc6ac98a3', value: '0x0'},
{blockHash: '0xf651c42de469b9b37e4843db23e98cf7cf0e164b4da8179b3fd6d0250238c7f2', blockNumber: '0x137e95e', ethHash: '0xc99051cc3084656a3fbe2817857ec5b95df8213609b34282faa2ecb43d4c03e1', from: 'one1se7lv0g7athe8xzz2rmckj7c83cx2twwks52kj', gas: '0x38149', gasPrice: '0x2540be400', hash: '0x0ec057adb9c365d2aa7f4b6187a69be7f7ea66542832e9ec52545ac333c8d87a', input: '0xf305d71900000000000000000000000072cb10c6bfa5624dd07ef608027e366bd690048f00000000000000000000000000000000000000000000000000e5d399591077d100000000000000000000000000000000000000000000000000e4ad6bc7faa02d0000000000000000000000000000000000000000000000002285601216c8c000000000000000000000000000867df63d1eeaef93984250f78b4bd83c70652dce0000000000000000000000000000000000000000000000000000000061b767a2', nonce: '0x72', r: '0x429f12954b400fa0513321b9a4f3b1ac63af531f3bdf5989dc76ed7784ef293a', s: '0x3ed334e84d10091dfe7922dc3cdaeb8db4c549939b22d04c1737eaa506b1e5cb', shardID: 0, timestamp: '0x61b76302', to: 'one1yjkky5pdr3jje3mggzq3d8gy394vyresl69pgt', toShardID: 0, transactionIndex: '0xb', v: '0xc6ac98a4', value: '0x22b1c8c1227a0000'},
{blockHash: '0xd66c59af7428eb2d1eacf73c23265b39c5150cf5d6e37e785bef8523a9e9390b', blockNumber: '0x137e94a', ethHash: '0x80b5d70df3fe94e35df85dbb67591bc0d17e4ca1864fa09b97121aa1de855c7d', from: 'one1se7lv0g7athe8xzz2rmckj7c83cx2twwks52kj', gas: '0x2afdd', gasPrice: '0x2540be400', hash: '0xd29fa8b21a27c9da797f980b556038f6e8346f98a8054f79b3c88ffd30ed63c6', input: '0x18cbafe500000000000000000000000000000000000000000000000000e6ed27d6668000000000000000000000000000000000000000000000000000229586cd940c7aa200000000000000000000000000000000000000000000000000000000000000a0000000000000000000000000867df63d1eeaef93984250f78b4bd83c70652dce0000000000000000000000000000000000000000000000000000000061b76749000000000000000000000000000000000000000000000000000000000000000200000000000000000000000072cb10c6bfa5624dd07ef608027e366bd690048f000000000000000000000000cf664087a5bb0237a0bad6742852ec6c8d69a27a', nonce: '0x71', r: '0x604d549def1b33f3847bc1caa8a4e7406c326fa81152a9f47412abef52a8ce20', s: '0x49f9530b969a7cbc826e2bf72a70d8fc3fc5e41acc1c7ef4d70103d0d09deece', shardID: 0, timestamp: '0x61b762d6', to: 'one1yjkky5pdr3jje3mggzq3d8gy394vyresl69pgt', toShardID: 0, transactionIndex: '0x8', v: '0xc6ac98a3', value: '0x0'},
{blockHash: '0xf4b6f4e04f2cb7f1c94919c9bf88999e7194d727519de8c879c464b3a5a78f03', blockNumber: '0x137e922', ethHash: '0x7cb41b3f2ea4b3b6d3a6bdd6224d87e65676fc419d5caa1b0d6abc66bf5c97b2', from: 'one1se7lv0g7athe8xzz2rmckj7c83cx2twwks52kj', gas: '0x6a953', gasPrice: '0x2540be400', hash: '0xfc5968390bfb2736b2fb30b2e8225600a66d39f198b9a7428a14a8c274106d69', input: '0x5eac6239000000000000000000000000000000000000000000000000000000000000002000000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000000', nonce: '0x70', r: '0x8045dccd77028914c5f945989441b0d2d960719dcb3b34d03793f6de2012cb25', s: '0x2f2b619d82c607449ee7ebcd73a72c3696cf0eced42751139133681919753324', shardID: 0, timestamp: '0x61b7627f', to: 'one1mvcxg0r34j0zzgk2qdq76a7sn40en7fy7lytq4', toShardID: 0, transactionIndex: '0x8', v: '0xc6ac98a3', value: '0x0'},
{blockHash: '0x2aa8875ff95c7663c1222c5cb21640b7c0506b95eb903c0c1628187d0e4bc0b1', blockNumber: '0x137e908', ethHash: '0xb3d256e0e71ec0d9606dfaf36a233eaf707b2be03667919f1ab5b8625f0fdee6', from: 'one1se7lv0g7athe8xzz2rmckj7c83cx2twwks52kj', gas: '0x2a858', gasPrice: '0x2540be400', hash: '0x38aa847ee9bfa6d277099d7dc0cffa5b08782c4d1c6e1ab38348c43ec5ee7a64', input: '0x5eac6239000000000000000000000000000000000000000000000000000000000000002000000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000000', nonce: '0x6f', r: '0xecbc831e04b6078bbf7c73d2319930bc0ea1a3a7d60c9329168e9d4b922c9a48', s: '0x34ff52ef68b78fa7c944ac51f71cafc4b8e3780e102bbee8a1a29ee8971b2bb4', shardID: 0, timestamp: '0x61b76246', to: 'one1mvcxg0r34j0zzgk2qdq76a7sn40en7fy7lytq4', toShardID: 0, transactionIndex: '0x4', v: '0xc6ac98a4', value: '0x0'},
{blockHash: '0x88483f523c6fb0675b7dd273662bd3a9e7c583c2afdba144e37145a2882b5124', blockNumber: '0x1374ee4', ethHash: '0xfffce0128ab2d029679a8250d7f0d87b3165b0f3656cf2e92f3d62a2e1d49175', from: 'one1se7lv0g7athe8xzz2rmckj7c83cx2twwks52kj', gas: '0x82b43', gasPrice: '0x2540be400', hash: '0xe674b32a405916a4d282c99789e39f3e588c49c4eb54294d15db9e553f7de7a8', input: '0x8dbdbe6d00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000ecd60d677a27ccf0000000000000000000000000000000000000000000000000000000000000000', nonce: '0x6e', r: '0xe0e55cbe3eb7a3ddd59f53e7e1e9f4c0449792c02e8c633ecefadb588b3aeea4', s: '0x1135624ca413c08d5aa70ff6869fa3d5277c6cf5eb7cd9cf26434cf657d0e021', shardID: 0, timestamp: '0x61b61774', to: 'one1mvcxg0r34j0zzgk2qdq76a7sn40en7fy7lytq4', toShardID: 0, transactionIndex: '0x7', v: '0xc6ac98a3', value: '0x0'},
{blockHash: '0xbd5dcf7d2f12726e3dc353352485cb292a377c9ffcad2a56a2750acb7b572824', blockNumber: '0x1374ec1', ethHash: '0x3974bb87962071c74ad093c05025f991a93323415ffbeae89d55553ae5f29820', from: 'one1se7lv0g7athe8xzz2rmckj7c83cx2twwks52kj', gas: '0x39ec8', gasPrice: '0x2540be400', hash: '0xcd5caffbb1d287c084bf5ffefb83380f92800b6995c590ce3973519d92292e60', input: '0xf305d71900000000000000000000000072cb10c6bfa5624dd07ef608027e366bd690048f00000000000000000000000000000000000000000000000002887c6bb93c963900000000000000000000000000000000000000000000000002853e5bd330c38d0000000000000000000000000000000000000000000000005f0c3bf50707b216000000000000000000000000867df63d1eeaef93984250f78b4bd83c70652dce0000000000000000000000000000000000000000000000000000000061b61bb6', nonce: '0x6d', r: '0x2320795e04ab5cc250f65077b95d6050b7317deacacddae99bd01059c6f9eb1f', 's': '0x6c95bbd87466732a8fe068ad2de0b62a1e657b33f11b5af8442fc537870529d4', shardID: 0, timestamp: '0x61b6172b', to: 'one1yjkky5pdr3jje3mggzq3d8gy394vyresl69pgt', toShardID: 0, transactionIndex: '0x6', v: '0xc6ac98a4', value: '0x5f8681b9cbe3b6d8'},
{blockHash: '0x715093d229fdf6aa04b5fc77b6f2d4d3be42819f77e4523990098a10d035c576', blockNumber: '0x1374eaf', ethHash: '0x5ba82b27e69459e28bb5f0120ba5955e6921a93a3988007fef56bd4595c1dfb6', from: 'one1se7lv0g7athe8xzz2rmckj7c83cx2twwks52kj', gas: '0x25de2', gasPrice: '0x2540be400', hash: '0x197933bf848e202071e83ca216e67311ef245a18e450ac485815b2f2d3c77c15', input: '0x7ff36ab5000000000000000000000000000000000000000000000000008c1f71ac62d34f0000000000000000000000000000000000000000000000000000000000000080000000000000000000000000867df63d1eeaef93984250f78b4bd83c70652dce0000000000000000000000000000000000000000000000000000000061b61b8b0000000000000000000000000000000000000000000000000000000000000002000000000000000000000000cf664087a5bb0237a0bad6742852ec6c8d69a27a00000000000000000000000072cb10c6bfa5624dd07ef608027e366bd690048f', nonce: '0x6c', r: '0x849a22b3132d2a5d4fdd5eeed502e60e52fb68a9685d6a789ec376b7fa047ad6', s: '0x5b38cd655741b47568a50bc21103adeff5fc19217edf1f8464b22374268e0130', shardID: 0, timestamp: '0x61b61704', to: 'one1yjkky5pdr3jje3mggzq3d8gy394vyresl69pgt', toShardID: 0, transactionIndex: '0x8', v: '0xc6ac98a3', value: '0x14d1120d7b160000'},
]

window.onload = async function initialize() {
    ReactDOM.render(
        <App />,
        document.getElementById('app'));
}

function App() {
    const [currentMenu, setMenu] = useState("mainmenu");
    const [currentAddress, setAddress] = useState("");
    const[currentStartDay, setStartDay] = useState(1629518400);
    const[currentEndDay, setEndDay] = useState(1000000000000);

    return (
        <div>
            <NavBar setMenu={setMenu} 
            currentAddress={currentAddress}
            />
            <Menu currentMenu={currentMenu} 
            currentAddress={currentAddress} 
            setAddress={setAddress} 
            setStartDay={setStartDay}
            setEndDay={setEndDay}
            currentStartDay={currentStartDay}
            currentEndDay={currentEndDay}
            />
        </div>
    );

}

function NavBar(props) {
    function NavButton(props) {
        return <button className = "navbtn" id="btnMenu" onClick={ () => props.setMenu(props.id)}>{props.text}</button>
    }
    
    function NavTitle(props) {
        return <button className = "navtitle" id="btnMenu" onClick={ () => props.setMenu(props.id)}>{props.text}</button>
    }


    return (
        <div className = "navbar">
            <NavTitle id = {"mainmenu"} text={"Defi Kingdoms"} setMenu={props.setMenu}/>
            <NavButton id = {"mainmenu"} text={`current address: ${props.currentAddress}`} setMenu={props.setMenu}/>
        </div>
    )

}

function Menu(props) {
    const[currentValue, setValue] = useState("");
    const[currentData, setData] = useState([]);
    const[currentMetadata, setMetadata] = useState({
        totalBalanceOne: "",
        totalBalanceCurrency: "",
        totalGasPaidOne: "",
        totalGasPaidCurrency: "",
    });
    const[currentCurrency, setCurrency] = useState("usd");
    const[displayCurrency, setDisplayCurrency] = useState("usd");
    const[currentContract, setContract] = useState("ALL");
    
    const[query, setQuery] = useState("");

    function handleChange(event) {
        setValue(event.target.value);
    }
    function handleSubmit(event) {
        event.preventDefault();
        let harmonyAddress = getAddress(currentValue).bech32;
        props.setAddress(harmonyAddress);
        setQuery([harmonyAddress, props.currentStartDay, props.CurrentEndDay])
        setDisplayCurrency(currentCurrency)
    }
    function startInput(event) {
        let unixTime = new Date(event).getTime() / 1000
        props.setStartDay(unixTime)

    }
    function endInput(event) {
        let unixTime = new Date(event).getTime() / 1000
        props.setEndDay(unixTime)
    }

    useEffect(() => {
        const fetchData = async (address, start, end, currency) => {
            let txs
            let metadata
            if (props.currentAddress == "") {
                txs = []
                metadata = []
            } else {
                const result = await axios({
                    method: 'post',
                    url: API_URL,
                    data: {
                      address: address,
                      startTime: start,
                      endTime: end,
                      currency: currency
                    }
                });
                txs = result.data.txs
                metadata = result.data.metadata
            }
            setMetadata(metadata)
            setData(txs)
        }
        fetchData(props.currentAddress, props.currentStartDay, props.currentEndDay, currentCurrency);

    },[query]);

    if (props.currentMenu == "mainmenu") {
        return (
            <div className = "menu">
                <ul >
                    <div className="center"><h2>Defi Kingdoms Transactions Report Generator</h2></div>
                    <br></br>
                    <div className="center">From:</div>
                    <div className="center"><DayPickerInput placeholder="DD/MM/YYYY" format="DD/MM/YYYY" onDayChange={startInput} /></div>
                    <div className="center">To:</div>
                    <div className="center"><DayPickerInput placeholder="DD/MM/YYYY" format="DD/MM/YYYY" onDayChange={endInput}/></div>
                    <br></br>
                    <div className="center">
                    <Dropdown>
                        <Dropdown.Toggle variant="success" id="dropdown-basic">
                            Currency ({currentCurrency})
                        </Dropdown.Toggle>

                        <Dropdown.Menu>
                            <Dropdown.Item onClick={() => setCurrency("usd")}>USD</Dropdown.Item>
                            <Dropdown.Item onClick={() => setCurrency("eur")}>EUR</Dropdown.Item>
                        </Dropdown.Menu>
                    </Dropdown>
                    </div>
                    <div className="center">
                    <form onSubmit={handleSubmit}>
                      <label>
                        <div className="center">Address:</div>
                        <input type="text" value={currentValue} onChange={handleChange} />
                      </label>
                      <input type="submit" value="Submit"/>
                    </form>
                    </div>


                    <br></br>
                    <div className="center"><h2>Information</h2></div>
                    <div className="center">Currency values in USD/EUR are calculated from the day that the transaction was made, not with the current values</div>
                    <Table striped bordered hover size="sm" variant="dark" >
                        <thead>
                        <tr>
                            <th>#</th>
                            <th>Value in One</th>
                            <th>Value in {displayCurrency}</th>
                        </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td> Gains/Losses</td>
                                <td>{currentMetadata.totalBalanceOne}</td>
                                <td>{currentMetadata.totalBalanceCurrency}</td>
                            </tr>
                            <tr>
                                <td>Total Gas Paid</td>
                                <td>{currentMetadata.totalGasPaidOne}</td>
                                <td>{currentMetadata.totalGasPaidCurrency}</td>
                            </tr>
                        </tbody>
                    </Table>
                    <br></br>
                    <div className="center"><h2>Transaction History</h2></div>
                    <div className="center">it takes a while to make the full report, please be patient</div>
                    <Dropdown>
                        <Dropdown.Toggle variant="success" id="dropdown-basic">
                            Contract Display ({currentContract})
                        </Dropdown.Toggle>

                        <Dropdown.Menu>
                            <Dropdown.Item onClick={() => setContract("ALL")}>ALL</Dropdown.Item>
                            <Dropdown.Item onClick={() => setContract("MasterGardener")}>MasterGardener</Dropdown.Item>
                            <Dropdown.Item onClick={() => setContract("UniswapV2Router02")}>UniswapV2Router02</Dropdown.Item>
                            <Dropdown.Item onClick={() => setContract("Quest")}>Quest</Dropdown.Item>
                            <Dropdown.Item onClick={() => setContract("MeditationCircle")}>MeditationCircle</Dropdown.Item>
                        </Dropdown.Menu>
                    </Dropdown>
                    <Table striped bordered hover size="sm" variant="dark">
                        <thead>
                        <tr>
                            <th>#</th>
                            <th>Blockchain</th>
                            <th>Contract Name</th>
                            <th>Transaction Type</th>
                            <th>One</th>
                            <th>Jewel</th>
                            <th>{displayCurrency} (Conversion)</th>
                            <th>Balance (in {displayCurrency})</th>
                            <th>Gas (in One)</th>
                            <th>Gas (in {displayCurrency})</th>
                            <th>Date</th>
                        </tr>
                        </thead>
                        <tbody>
                            {Object.values(currentData).map((_, index) => renderData(_, index, currentContract))}
                        </tbody>
                    </Table>
                    <br></br>
                    <br></br>
                    <br></br>
                    <br></br>
                    <br></br>
                    <br></br>
                    <br></br>
                    <br></br>
                    <br></br>
                    <br></br>
                    <br></br>
                    <br></br>
                    <br></br>
                    <br></br>
                </ul>
            </div>
        )
    } else if (props.currentMenu == "address") {
        return (
            <div className = "menu">
                <ul >
                    <div className="center">

                    </div>
                </ul>
            </div>
        )
    }
}

function renderData(tx, index, contract) {
    let render
    if (contract == "ALL") {
        render = true
    } else if (contract == tx.contract) {
        render = true
    } else {
        render = false
    }
    if (render == true) {
        return (
        <tr key={index+1}>
            <td>{index+1}</td>
            <td>{tx.chain}</td>
            <td>{tx.contract}</td>
            <td>{tx.txType}</td>
            <td>{tx.valueOne}</td>
            <td>{tx.valueJewel}</td>
            <td>{tx.valueCurrency}</td>
            <td>{tx.delta}</td>
            <td>{tx.gasPaid}</td>
            <td>{tx.gasPaidCurrency}</td>
            <td>{new Date(tx.timestamp * 1000).toISOString()}</td>
        </tr>
        )
    } else { return "" }
}







