# FB-Altcoin-Stock-Chatbot
A slightly lengthy bot to get Stocks and Altcoin prices. Uses fbchat and python. #CURRENT COMPATIBLE WITH ONLY FBCHAT < 1.0

## Getting Started
Really simple, just copy app.py to whereever you want to run it, add two environment variables Email and Password, then run it using `python app.py`. That or just git push it to openshift. Whatever floats your boat.

### Prerequisites

* Some version of Python
* fbchat `pip install fbchat`
* Facebook login of some sort, whether this is your actual account or one just for this purpose




## Using the bot

#### Instructions

1. Run the command `rhc env set Email=<Your Email> Password=<Your Password> -a <App Name>` in CMD for Openshift. Heroku is slightly different.
2. Run `python app.py` (or if you're using Openshift, just do a `git push` and it will autostart)
3. Find the name of the account you used and start a conversation
4. Wait for the bot's reply
 
#### Commands
* `!stock <stockcode>` - Gets the current price and change for the specified stock `e.g. !stock anz.ax`
* `!<altcoin>` - Gets the current price for the altcode in USD and BTC `e.g. !eth`
* `!btcaud` - Gets the current price for 1 bitcoin in AUD `e.g. !btcaud`
* `!decide <option 1>,<option 2>,<option n>` - Make a decision for you 'e.g. !decide Pancakes, Cereal`

## Screenshot
![](http://i.imgur.com/T0YVCQn.png)


## Authors

* Tim Chan - https://twitter.com/TimLChan


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## Acknowledgments

* Thanks to [fbchat](https://github.com/carpedm20/fbchat) for the great Facebook Chat implementation
* Uses the [Yahoo! Query Language](https://developer.yahoo.com/yql/)
* Utilises the [CryptoCompare API](https://www.cryptocompare.com/api/)
* Thanks [Weidi Zhang](https://github.com/weidizhang/) for providing the YQL url and arguments
