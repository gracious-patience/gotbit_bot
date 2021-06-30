import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os
import requests
import urllib.request
import json




def get_soup(url):

    f = urllib.request.urlopen(url)
    nyb = f.read()
    mystr = nyb.decode("utf8")
    f.close()
    soup = json.loads(mystr)

    return soup

coins = [
    'pawtocol',
    'safemooncash',
    'g999',
    'bitswift',
    'intexcoin',
    'horizondollar',
    'skillchain',
    'exchangecoin',
    'buzzshow',
    'ime-lab',
    'didcoin',
    'phoenix-defi-finance',
    'merchdao',
    'dehive',
    'xsigma'
        ]

exchanges = [
    'xt',
    'probit',
    'hitbtc',
    'bitforex',
    'bitmart',
    'hotbit',
    'bibox',
    'ibank',
    'gate',
    'coinsuper',
    'exmarkets',
    'stex',
    'bittrex'
    ]

def send_stats():
    # volumes
    vols =[]
    #time = datetime.datetime.today().strftime("%Y_%m_%d_%H:%M:%S")
    text =  '\nVolumes for the last 24h, :\n\n'
    for coin in coins:
        url = 'https://api.coingecko.com/api/v3/coins/'+ coin
        s = get_soup(url)

        client_vols = {'name':'',
                      'volume':''}

        client_vols['name'] = coin
        client_vols['volume'] = s['market_data']['total_volume']['usd']
        vols.append(client_vols)

        text += coin + ' :\n'

        tickers = s['tickers']
        for ticker in tickers:
            if ticker['market']['identifier'] in exchanges:
                text += '\t' + ticker['market']['name'] + ': ' + ticker['base'] + ' - ' + ticker['target'] + ': ' + str(ticker['converted_volume']['usd']) + '\n' 

        text += '\n'
       # print(coin, ' price in usd = ', s['market_data']['current_price']['usd'])

        #print(coin, s['market_data']['total_volume']['usd'])

    text += '\n Current prices in USD :\n\n'
    for coin in coins:
        url = 'https://api.coingecko.com/api/v3/coins/'+ coin
        s = get_soup(url)

        client_prices = {'name':'',
                      'price':''}

        client_prices['name'] = coin
        client_prices['volume'] = s['market_data']['current_price']['usd']
        vols.append(client_vols)
       # print(coin, ' price in usd = ', s['market_data']['current_price']['usd'])
        text += coin + ' - '+str(s['market_data']['current_price']['usd']) + '\n'
        print(coin, s['market_data']['total_volume']['usd'])    

    #time = datetime.datetime.today().strftime("%Y_%m_%d_%H:%M:%S")
    #filename= 'Clients_vols'+ time + '.csv'
    #df = pd.DataFrame.from_records(vols)
    #df.to_csv(filename)


    return text
    







#PORT = int(os.environ.get('PORT', 8443))

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
TOKEN = '1880188697:AAHzKOFN3HqgU5b4672z2RORjT8br9gU0js'

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')

def help(update, context):
    """Send a message when the command /help is issued."""
    


    text = send_stats()
    update.message.reply_text(text)

def echo(update, context):
    """Echo the user message."""
    if (update.message.text == 'hi' or update.message.text == 'Hi' or update.message.text == 'HI') and (update.message.from_user['id']==666165975):
        update.message.reply_text('Ты себя видел?')
    elif (update.message.text == 'hi' or update.message.text == 'Hi' or update.message.text == 'HI') and (update.message.from_user['id']==553439580):
        update.message.reply_text('Здорово, отец!')
    elif (update.message.text == 'hi' or update.message.text == 'Hi' or update.message.text == 'HI') and (update.message.from_user['id']==858240517):
        update.message.reply_text('Привет, Саша!')
    elif (update.message.text == 'hi' or update.message.text == 'Hi' or update.message.text == 'HI'):
        update.message.reply_text(update.message.text)
    
    print(update.message.from_user)

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    
        
    # updater.start_webhook(listen="0.0.0.0",
    #                           port=int(PORT),
    #                           url_path=TOKEN)
    # updater.bot.setWebhook('https://fierce-badlands-07220.herokuapp.com/ ' + TOKEN)

        # Run the bot until you press Ctrl-C or the process receives SIGINT,
        # SIGTERM or SIGABRT. This should be used most of the time, since
        # start_polling() is non-blocking and will stop the bot gracefully.

    updater.start_polling()
    updater.idle()
    
    

if __name__ == '__main__':
    main()