# FB Altcoin Stock Chatbot
Random FB Altcoin/Stock/Trigger chatbot. Probably does what it's supposed to do.

~~CURRENTLY COMPATIBLE WITH ONLY FBCHAT < 1.0. This will be fixed shortly with a new update.~~

Compatible with the latest FBChat

## Todo
- ~~Move main app.py from urllib3 to requests~~ Done
- Add Currency Conversion
- Add Heroku instructions
- Fix Math function
- Make admin access configurable for adding commands


## Getting Started
### Prerequisites

* Some version of Python3
* fbchat, requests, urllib3 `pip install -r requirements.txt`
* Facebook login of some sort, whether this is your actual account or one just for this purpose

### Usage
1. `git clone` this repo
2. Rename `settings/settings_template.py` to `settings/settings.py` and fill in blank information
3. `pip install -r requirements.txt` to get requirements
4. Run with `python app.py`


Note: I suggest not using your main Facebook account, but have a separate account set up for this purpose. If you are planning to run this on a service without a fixed IP (such as Heroku), Please log in first, copy the useragent of your browser and the relevant cookies for facebook.com to avoid getting checkpointed.



## Using the bot

#### Admin ID Setup
The ability to delete commands are only available for admins of the this chatbot. To set admins, find the user's facebook ID and add them as comma separated values in `adminfbids` variable in `settings/settings.py`


#### Functionality
* Get stocks (via Alphavantage)
* Get Bitcoin/Altcoins (via CoinMarketCap)
* Get time from a timezone
* Check 2captcha credits
* Respond to triggers set by users


#### Commands
* `!commands` - Return the command list
* `!addcmd <command> <response>` - to add a basic text/emoji response
* `!delcmd <command>` - to delete a command

## Screenshot
![](http://i.imgur.com/T0YVCQn.png)


## Authors

* Tim Chan - https://twitter.com/TimLChan


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## Changelog

#### 16 March 2020 - Version 2.0
* Update `shitcoins.py` to use new Coinmarketcap API
* Remove use of `urllib3` for app.py

## Acknowledgments

* Thanks to [fbchat](https://github.com/carpedm20/fbchat) for the great Facebook Chat implementation
* Utilises the [CryptoCompare API](https://www.cryptocompare.com/api/)
* Thanks [Weidi Zhang](https://github.com/weidizhang/) for providing the YQL url and arguments