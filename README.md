# DFK-bounty

Transaction Generator Report for Defi Kingdoms

fetch the current balance of all contracts related to defi kingdoms and their current value in usd/eur

fetch all transactions between a selected frametime for a selected address.
calculate the gains/losses on the given timeframe, takes into consideration the price which each item has when obtain/bought and the price when sold. 
considers gains/losses for appreciation and depreciation of each currency.
gains/losses calculations improve when feed better historical data and doesn't include all HRC20 tokens so it might not be 100% accurate.
Harmony api gives some transactions out of order so those might affect gains/losses calculations.