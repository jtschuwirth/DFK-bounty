import React, { useState } from "react";
import ReactDOM from "react-dom";
import DayPicker from "react-day-picker";
import DayPickerInput from "react-day-picker/DayPickerInput";

const BN = require('bn.js');
const Web3 = require("web3");

const HMY_RPC_URL = "https://api.s0.t.hmny.io/"
const web3 = new Web3(HMY_RPC_URL);

window.onload = async function initialize() {
    ReactDOM.render(
        <App />,
        document.getElementById('app'));
}

function App() {
    const [currentMenu, setMenu] = useState("mainmenu");
    const [currentAddress, setAddress] = useState("");
    const[currentStartDay, setStartDay] = useState("");
    const[currentEndDay, setEndDay] = useState("");

    return (
        <div>
            <NavBar setMenu={setMenu} 
            currentAddress={currentAddress}
            currentStartDay={currentStartDay}
            currentEndDay={currentEndDay}
            />
            <Menu currentMenu={currentMenu} 
            currentAddress={currentAddress} 
            setAddress={setAddress} 
            setStartDay={setStartDay}
            setEndDay={setEndDay}
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
            <NavTitle id = {"mainmenu"} text={"DFK Transaction History"} setMenu={props.setMenu}/>
            <NavButton id = {"address"} text={`current address: ${props.currentAddress}`} setMenu={props.setMenu}/>
            <NavButton id = {"address"} text={`From: ${props.currentStartDay}`} setMenu={props.setMenu}/>
            <NavButton id = {"address"} text={`To: ${props.currentEndDay}`} setMenu={props.setMenu}/>
        </div>
    )

}

function Menu(props) {
    const[currentValue, setValue] = useState("");


    function handleChange(event) {
      setValue(event.target.value);
    }

    async function handleSubmit(event) {
      setTransaction([])
      event.preventDefault();
      props.setAddress(currentValue);
    }
    function startInput(event) {
      let unixTime = new Date(event).getTime() / 1000
      props.setStartDay(unixTime)

    }
    function endInput(event) {
      let unixTime = new Date(event).getTime() / 1000
      props.setEndDay(unixTime)
    }

    if (props.currentMenu == "mainmenu") {
        return (
            <div className = "menu">
                <ul >
                    <div className="center"><h2>Transaction History</h2></div>
                    <br></br>
                    <div className="center">From:</div>
                    <div className="center"><DayPickerInput placeholder="DD/MM/YYYY" format="DD/MM/YYYY" onDayChange={startInput} /></div>
                    <div className="center">To:</div>
                    <div className="center"><DayPickerInput placeholder="DD/MM/YYYY" format="DD/MM/YYYY" onDayChange={endInput}/></div>
                    <br></br>
                    <div className="center">
                    <form onSubmit={handleSubmit}>
                      <label>
                        Address: <input type="text" value={currentValue} onChange={handleChange} />
                      </label>
                      <input type="submit" value="Submit"/>
                    </form>
                    </div>
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







