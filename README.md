# Crypto_analysis
simple streamlit app to make MMA and OSC analysis for cyrpto-currenices, and gives resaults for which coins are best to buy or sell depending on the interval you using.

steps:
1- install requierments:
pip install -r requirements.txt

2- coinmarketcap API-key
 def get_marketCap(self):
        url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
        parameters = {
        'start':'1',
        'limit':'100',
        'convert':'USDT'
        }
        headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': 'add you key in here',   
        }
3- run the program
streamlit run main.py
