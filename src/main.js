import React, { useState, useEffect } from "react";
import ReactDOM from "react-dom";
import DayPickerInput from "react-day-picker/DayPickerInput";
import { Table, Dropdown } from 'react-bootstrap';
import axios from "axios";
const bootstrap = require('bootstrap')
const { getAddress } = require('@harmony-js/crypto');

window.onload = async function initialize() {
    ReactDOM.render(
        <App />,
        document.getElementById('app'));
}

//const API_URL = "http://192.168.0.30:5000/"
//const API_URL = "http://localhost:5000/"
const API_URL = "https://jtschuwirth.xyz/"

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
    const[currentCurrency, setCurrency] = useState("usd");
    const[displayCurrency, setDisplayCurrency] = useState("usd");
    const[currentContract, setContract] = useState("ALL");
    const[currentBalance, setCurrentBalance] = useState([]);
    const[currentSheet, setSheet] = useState([]);
    const[loading, setLoading] = useState(false);
    const[query, setQuery] = useState("");

    function handleChange(event) {
        setValue(event.target.value);
    }
    function handleSubmit(event) {
        event.preventDefault();
        let harmonyAddress = getAddress(currentValue).bech32;
        //let harmonyAddress = getAddress("one1se7lv0g7athe8xzz2rmckj7c83cx2twwks52kj").bech32;
        //let harmonyAddress = getAddress("0xa8c5115c8e44351b2bc2d401a1f033bb45129dc5").bech32;
        props.setAddress(harmonyAddress);
        setQuery([harmonyAddress, props.currentStartDay, props.CurrentEndDay, currentCurrency])
        setDisplayCurrency(currentCurrency)
        setData([]);
        setCurrentBalance([]);
        setSheet([]);
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
            let txs = [];
            let balance = [];
            let balanceSheet = [];
            let hashes = [];
            if (props.currentAddress == "") {
                txs = [];
                balance = [];
                balanceSheet = [];
                hashes = [];
            }
            else {
                setLoading(true);
                const result = await axios.post(API_URL+"currentBalance", {
                    address   : address,
                    currency  : currency
                })
                for (let i = 0; i<Object.keys(result.data.currentBalance).length; i++) {
                    if (Object.values(result.data.currentBalance)[i] != 0 ) {
                        balance.push([Object.keys(result.data.currentBalance)[i], Object.values(result.data.currentBalance)[i]]);
                    }
                }
                setCurrentBalance(balance)
                for (let i = 0; i<1000; i++) {
                    const result = await axios.post(API_URL+"transactionReport", {
                        address   : address,
                        startTime : start,
                        endTime   : end,
                        currency  : currency,
                        page      : i,
                        hashes    : hashes
                    })
                    if (result.data.status == "finished") {
                        break
                    } else if (result.data.status == "error") {
                        break
                    }
                    txs = result.data.txs;
                    for (let i=0; i<Object.values(txs).length; i++) {
                        if (hashes.includes(Object.values(txs)[i].hash) == false) {
                            hashes.push(Object.values(txs)[i].hash)
                        } 
                    }
                    setData(currentData => [...currentData, txs]);
                    for (let i = 0; i<Object.keys(result.data.balanceSheet).length; i++) {
                        let logrado = false;
                        let name = Object.keys(result.data.balanceSheet)[i];
                        let value = Object.values(result.data.balanceSheet)[i];
                        currentSheet.map((_) => balanceSheet.push(_));
                        for (let j in balanceSheet) {
                            if (balanceSheet[j][0].toString() == name.toString()) {
                                balanceSheet[j] = [name, balanceSheet[j][1]+value];
                                logrado = true;
                                break
                            }
                        }
                        if (logrado == false) {
                            balanceSheet.push([name, value]);
                        }
                    }
                    setSheet([...balanceSheet])
                }
                setLoading(false);
            }
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
                    <div className="center">{loading == true && <h2>Fetching Transactions, please wait</h2>}</div>
                    <div className="center"><h2>Current Balance</h2></div>
                    <Table striped bordered hover size="sm" variant="dark" responsive>
                        <thead>
                        <tr>
                            <td> #</td>
                            {currentBalance.map((_, index) => renderCurrentBalanceTitle(_, index))}
                        </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td> Quantity</td>
                                {currentBalance.map((_, index) => renderCurrentBalanceQuantity(_, index))}
                            </tr>
                            <tr>
                                <td> Value in {displayCurrency}</td>
                                {currentBalance.map((_, index) => renderCurrentBalanceValue(_, index))}
                            </tr>
                        </tbody>
                    </Table>
                    <div className="center"><h2>Current Balance value ({displayCurrency}): {currentBalance.reduce((a, b) => a + b[1][1], 0)}</h2></div>

                    <br></br>
                    <div className="center"><h2>Gains/Losses in Timeframe</h2></div>
                    <div className="center">Currency values in USD/EUR are calculated from the day that the transaction was made, not with the current values</div>
                    <div className="center">This Table updates when more transactions are fetched</div>
                    <Table striped bordered hover size="sm" variant="dark" responsive>
                        <thead>
                        <tr>
                            <th>#</th>
                            {currentSheet.map((_, index) => renderCurrentSheetTitle(_, index))}
                        </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td> Change in timeframe</td>
                                {currentSheet.map((_, index) => renderCurrentSheetValue(_, index))}
                            </tr>
                        </tbody>
                    </Table>
                    <br></br>
                    <div className="center"><h2>Transaction History</h2></div>
                    <div className="center">Transactions are fetched in batches of 5, it takes a while to make the full report, please be patient</div>
                    <Dropdown>
                        <Dropdown.Toggle variant="success" id="dropdown-basic">
                            Contract Display ({currentContract})
                        </Dropdown.Toggle>

                        <Dropdown.Menu>
                            <Dropdown.Item onClick={() => setContract("ALL")}>ALL</Dropdown.Item>
                            <Dropdown.Item onClick={() => setContract("UniswapV2Router02")}>Marketplace Trader</Dropdown.Item>
                            <Dropdown.Item onClick={() => setContract("Quest")}>Quest</Dropdown.Item>
                            <Dropdown.Item onClick={() => setContract("MeditationCircle")}>Meditation Circle</Dropdown.Item>
                            <Dropdown.Item onClick={() => setContract("MasterGardener")}>Master Gardener</Dropdown.Item>
                            <Dropdown.Item onClick={() => setContract("xJEWEL")}>Bank</Dropdown.Item>
                            <Dropdown.Item onClick={() => setContract("AuctionHouse")}>Auction House</Dropdown.Item>
                            <Dropdown.Item onClick={() => setContract("Summoning")}>Summoning</Dropdown.Item>
                        </Dropdown.Menu>
                    </Dropdown>
                    <Table striped bordered hover size="sm" variant="dark">
                        <thead>
                        <tr>
                            <th>#</th>
                            <th>Chain</th>
                            <th>Contract Name</th>
                            <th>Transaction Type</th>
                            <th>Change (One)</th>
                            <th>Change (Jewel)</th>
                            <th>Change ({displayCurrency})</th>
                            <th>Gas (One)</th>
                            <th>Gas ({displayCurrency})</th>
                            <th>Date</th>
                        </tr>
                        </thead>
                        <tbody>
                            {currentData.map((txs) => Object.values(txs).map((_, index) => renderData(_, Object.keys(txs)[index], currentContract)))}
                        </tbody>
                    </Table>
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
function renderCurrentSheetTitle(tupla, index, currency) {
    if (tupla[0] == "Currency") {
        return (
            <th>gains/losses</th>
        )
    } else {
        return (
            <th>{tupla[0]}</th>
        )
    }
}

function renderCurrentSheetValue(tupla, index) {
    return (
        <th>{tupla[1]}</th>
    )
}

function renderCurrentBalanceTitle(tupla, index) {
    return (
        <th>{tupla[0]}</th>
    )
}
function renderCurrentBalanceValue(tupla, index) {
    return (
        <th>{tupla[1][1]}</th>
    )
}

function renderCurrentBalanceQuantity(tupla, index) {
    return (
        <th>{tupla[1][0]}</th>
    )
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
        <tr key={index}>
            <td>{index}</td>
            <td>{tx.chain}</td>
            <td>{tx.contract}</td>
            <td>{DecodeTxInfo(tx.txType)}</td>
            <td>{tx.balanceChange.One}</td>
            <td>{tx.balanceChange.Jewel}</td>
            <td>{tx.balanceChange.Currency}</td>
            <td>{tx.gasPaid}</td>
            <td>{tx.gasPaidCurrency}</td>
            <td>{new Date(tx.timestamp * 1000).toLocaleDateString("en-US")}</td>
        </tr>
        )
    } else { return "" }
}

function renderItems(item, quantity) {
    return (
        <div><img 
        src={`src/images/${item.toLowerCase().replace(/\ /g,"_")}.png`} width="30" height="30" ></img>{[item,": ",quantity]}</div>
    )
}

function DecodeTxInfo(info) {
    if (info.event == "Quest Completed") {
        return(
            <div>
                <div>{[info.event, " with heroes: ", info.heroIds.map((id) => [id, " "])," rewards: "]}</div>
                {Object.keys(info.rewards).map((_, index) => renderItems(_, Object.values(info.rewards)[index]))}
            </div>
        )
    } else if (info.event == "Start Fishing Quest" || info.event == "Start Foraging Quest" || info.event == "Start Wishing Well Quest") {
        return [info.event, " with heroes: ", info.heroIds.map((id) => [id, " "])]
    } else if (info.event == "Trade") {
        return [info.event, ": Bought ", info.boughtAmount, " ",info.bought, " for ", info.soldAmount, " ", info.sold]
    } else if (info.event == "Sold for Gold") {
        return [info.item, " ",info.event]
    } else if (info.event == "Deposit LP" || info.event == "Withdraw LP") {
        return [info.event, ": ",info.amount]
    } else if (info.event == "Cancel Auction") {
        return [info.event, " of hero: ",info.heroId]
    } else if (info.event == "Add to Bank" || info.event == "Remove from Bank") {
        return [info.event, ": ",info.amount, " ",info.currency]
    } else if (info.event == "Approved for Bank" || info.event == "Approved for Meditation Circle" || info.event == "Approved for Auction House" || info.event == "Transaction Failed" || info.event == "Started New Quest" || info.event == "Approved for Trade" || info.event == "Started Wishing Well Quest" || info.event == "Approved for auction House" || info.event == "Approved for Summoning") {
        return [info.event]
    } else if (info.event == "Create Renting Auction") {
        return [info.event, " for hero: ",info.heroId, " for ",info.price," ",info.currency]
    } else if (info.event == "Cancel Renting Auction" || info.event == "Cancel Quest") {
        return [info.event, " for hero: ", info.heroId]
    } else if (info.event == "Complete Meditation") {
        return [info.event, " with hero: ", info.heroId]
    } else if (info.event == "add Liquidity" || info.event == "Liquidity Removed") {
        return [info.event, ": ", info.amountA, " ",info.tokenA, " and ", info.amountB, " ", info.tokenB]
    } else if (info.event == "add Liquidity One") {
        return [info.event, ": ", info.amountOne, " One and ", info.amount, " ", info.token]
    } else if (info.event == "Claim LP rewards") {
        return [info.event, ": ", info.unlockedAmount, " Unlocked Amount and ", info.lockedAmount, " Locked Amount"]
    } else if (info.event == "Create Auction") {
        return [info.event, " for hero: ",info.heroId, ", Selling price: ", info.price, " ", info.currency, ", Status: ", info.status]
    } else if (info.event == "Bought Hero") {
        return [info.event, ": ",info.heroId, " for ", info.price, " ", info.currency]
    } else if (info.event == "Summon Crystal") {
        return [info.event, ": with hero ", info.summonerId, " and assistant: ", info.assistantId, " cost: ",info.summonerTears+info.assistantTears, " Tears and ", info.amountJewel, " Jewels"]
    } else if (info.event == "Crystal Open") {
        return [info.event, ", received hero: ",info.heroId]
    } else if (info.event == "Liquidity One Removed") {
        return [info.event, ": ", info.amountOne, " One and ", info.amountToken, " ", info.token]
    } else if (info.event == "Start Meditation") {
        return [info.event, " with hero: ", info.heroId, " cost: ", info.amountJewel, " Jewels and ", info.amountRune, " ", info.rune]
    } else if (info.event == "Transfer Hero") {
        return [info.event, ": ",info.heroId]
    }else {
        return JSON.stringify(info)
    }
}







