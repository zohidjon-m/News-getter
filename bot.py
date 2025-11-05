import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

API_KEY = '9b971b608357433da36b30d62a61f4ed'
URL = 'https://newsapi.org/v2/top-headlines?'

def get_articles_by_category(update: Update, context: CallbackContext):
    category = context.args[0]  # Extract category from the command
    query_parameters = {
        "category": category,
        "sortBy": "top",
        "country": "gb",
        "apiKey": API_KEY
    }
    articles = _get_articles(query_parameters)

    for article in articles:
        update.message.reply_text(f"{article['title']}\n{article['url']}\n")

def get_articles_by_query(update: Update, context: CallbackContext):
    query = ' '.join(context.args)  # Extract query from the command
    query_parameters = {
        "q": query,
        "sortBy": "top",
        "country": "us",
        "apiKey": API_KEY
    }
    articles = _get_articles(query_parameters)

    for article in articles:
        update.message.reply_text(f"{article['title']}\n{article['url']}\n")

def _get_articles(params):
    response = requests.get(URL, params=params)
    articles = response.json().get('articles', [])
    return [{"title": article["title"], "url": article["url"]} for article in articles]

def get_sources_by_category(update: Update, context: CallbackContext):
    category = context.args[0]  # Extract category from the command
    url = 'https://newsapi.org/v2/top-headlines/sources'
    query_parameters = {
        "category": category,
        "language": "en",
        "apiKey": API_KEY
    }

    response = requests.get(url, params=query_parameters)
    sources = response.json().get('sources', [])

    for source in sources:
        update.message.reply_text(f"{source['name']}\n{source['url']}\n")

def main():
    updater = Updater(token='6340071159:AAFaqx2YxZFW3itlVR9erbVf_UhtiYRxODk', use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("get_articles_by_category", get_articles_by_category))
    dp.add_handler(CommandHandler("get_articles_by_query", get_articles_by_query))
    dp.add_handler(CommandHandler("get_sources_by_category", get_sources_by_category))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
