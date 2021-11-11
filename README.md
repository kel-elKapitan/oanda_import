## Retrieve data from oanda.com rest API v20
## Background
This repo imports currency pair prices for 7 instruments provided by oanda.com

It covers <b>retrieving data from an API</b> and <b>looping and control.</b>

it uses <i>pandas</i> for exporting to csv, <i>requests and datetime</i> for api manipulation. 

### Usage

1. choose a date __(line 14 in oanda_import.py)__ to start the import
1. This program is designed to Extract data from the OANDA Practice v20 APIyou need to your own access token, __(create a free OANDA account, paste token at line 16 of oanda_import.py)__ 
1. To execute the program: __python oanda_import.py__

__the output is 7 csv files__


Created because I sometimes need data in a rush

I hope this program is helpful, Enjoy.
