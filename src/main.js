import React, { useState, useEffect } from "react";
import ReactDOM from "react-dom";
import DayPickerInput from "react-day-picker/DayPickerInput";
import { Table, Dropdown } from 'react-bootstrap';
import axios from "axios";
const bootstrap = require('bootstrap')
const { getAddress } = require('@harmony-js/crypto');
//const api = require("./api.js")

window.onload = async function initialize() {
    ReactDOM.render(
        <App />,
        document.getElementById('app'));
}

//const API_URL = "http://192.168.0.30:5000/"
//const API_URL = "http://localhost:5000"
const API_URL = "http://dfkflaskapi-env.eba-akm5qgmp.us-east-1.elasticbeanstalk.com/"

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
        //let harmonyAddress = getAddress(currentValue).bech32;
        let harmonyAddress = getAddress("one1se7lv0g7athe8xzz2rmckj7c83cx2twwks52kj").bech32;
        props.setAddress(harmonyAddress);
        setQuery([harmonyAddress, props.currentStartDay, props.CurrentEndDay, currentCurrency])
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
            let txs;
            let metadata;
            if (props.currentAddress == "") {
                txs = [];
                metadata = [];
            }
            else {
                const result = await axios.post(API_URL, {
                    address   : address,
                    startTime : start,
                    endTime   : end,
                    currency  : currency
                })
            txs = result.data.txs;
            metadata = result.data.metadata;
            }
            //else {
            //    const result = await api.Api(address, start, end, currency);
            //    txs = result.txs;
            //    metadata = result.metadata;
            //}
            setMetadata(metadata);
            setData(txs);
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
                            <Dropdown.Item onClick={() => setContract("UniswapV2Router02")}>UniswapV2Router02</Dropdown.Item>
                            <Dropdown.Item onClick={() => setContract("Quest")}>Quest</Dropdown.Item>
                            <Dropdown.Item onClick={() => setContract("MeditationCircle")}>MeditationCircle</Dropdown.Item>
                            <Dropdown.Item onClick={() => setContract("xJEWEL")}>Bank</Dropdown.Item>
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







