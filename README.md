# Crypto_analysis
Discription:
simple streamlit app to make MMA and OSC analysis for cyrpto-currenices, and gives resaults for which coins are best to buy or sell depending on the interval you using.


        Stage 0: get a list of lastest active coins in the market
        Stage 1: MA analysis that they have been > 0 the last 1 hour , 24 hours and 7 days and output:
            strong_buy
            buy
            sell
            strong_sel
        Stage 2: OSC analysis on the "strong_buy list" that we got from the analysis in earlier stage and generate: 
            recommanded_list
        
        stage 1,2 can be done on different intervel of times:
            1 minute
            5 minutes
            15 minutes
            1 hour
            4 hours
            1 day
            1 week
            1 month
        Stage 3: save the generated Coin_list

setup:
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
        'X-CMC_PRO_API_KEY': 'add your key in here',   
        }

3- run the program
streamlit run main.py

![image](https://user-images.githubusercontent.com/17545900/116814244-2c155780-ab58-11eb-8b80-6d2b73bd27d8.png)
