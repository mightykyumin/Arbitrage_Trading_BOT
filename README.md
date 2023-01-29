Arbitrage Trading Bot
===================

Overview
------------------
![arb1](https://user-images.githubusercontent.com/86776597/215308005-edb34a89-2bee-4ddb-9ce4-fdad4ab6d8e9.PNG)

![arb2](https://user-images.githubusercontent.com/86776597/215319059-7b92aa1b-ec1a-4d7e-9f7b-af8b3d2e4438.PNG)


Required
---------------
* pyupbit API
* python 
* binance API

Usage
-------------
* pip install pyupbit
* pip install pybinance

Used QThread

How to Use
---------------
1. Insert upbit Access key and secret key in the Upbit box
2. Insert binance Access key and secret key in the binance box
3. Press Start Trading

How it works
-----------------
* Calculate the price difference between upbit and binance in BTC price
* If the difference is great enough(0.5%) purchase the coin that has lowest premium in korea upbit market
* Transfer to binance and purchase the highest premium and transfer back to korea upbit market.

Future Plan
--------------
* Update UI with better graphic
* Use websocket to calculate faster
* Add other market and more coin available
* Improve performance
