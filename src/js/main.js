import React, { useState } from "react";
import ReactDOM from "react-dom";
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

    return (
        <div>
            <NavBar setMenu={setMenu} />
            <Menu currentMenu={currentMenu}/>
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
            <NavButton id = {"menu1"} text={"menu 1"} setMenu={props.setMenu}/>
        </div>
    )

}


function Menu(props) {
    if (props.currentMenu == "mainmenu") {
        return (
            <div className = "menu">
                <ul >
                    <div className="center"><h2>Transaction History</h2></div>
                    <br></br>
                </ul>
            </div>
        )
    } else if (props.currentMenu == "menu2") {
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





