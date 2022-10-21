from gettext import find
import sys
from game_links import *
from logger_base import log
from telegram.ext import Updater, MessageHandler, CommandHandler, Filters
import requests
from bs4 import BeautifulSoup
import signal
import time

# Declarando variables globales
updater = Updater(TOKEN, use_context=True)
dispatcher = updater.dispatcher
best_price_game = {
    reTriplePack_url: 10.00,
    redDeadREdemption_url: 20.00,
    nierAutomata_url: 10.00,
    doomEternal: 10.00,
    GOF: 15.00,
    RE2: 10.00,
    RE3: 10.00,
    detroid: 10.00,
}

# Funcion que obtiene los precios parseando la pagina web
def get_price(game_url):
    url = requests.get(game_url)
    characters = "$€" # Eliminamos estos caracteres para que se nos retorno un valor decimal y no un string
    soup = BeautifulSoup(url.content, "html.parser")
    stock = soup.find("div", {"class": "stock"})
    nostock = soup.find("div", {"class": "nostock"})

    if stock: 
        result = soup.find("div", {"class": "total"})
        first_price_text = result.text
        first_price = float("".join(x for x in first_price_text if x not in characters))
        return first_price

    elif nostock: # Si no hay stock se nos retornara un valor de 0
        return 0


def current_games(games, bot, chatID):
    price_game = get_price(games) # Obtenemos los precios mediante una funcion. El parametro de la funcion inicial es la url
    try:
        if price_game != 0:
            bot.sendMessage(
                chat_id=chatID,
                text="¡Alerta mamaguevo hay tremendo oferton de: {}€! \n"
                      "Aqui tenes el enlace papuh: {}".format(price_game, games)
                )
        else:
            bot.sendMessage(
                    chat_id=chatID,
                    text="Fuera de stock papuh :C: Este es el juego fuera de stock \n"
                         "El juego es: \n {}".format(games)
                    )            
    except Exception as e:
        log.error(e)


def all_games(bot, chatID): # Llamando a todos los juegos dentro del diccionario
    for game in best_price_game.keys():
        current_games(game, bot, chatID)


def alert_games(bot, chatID): # Bucle con intervalo de tiempo para poder apreciar el cambio de precio del juego
    messag = True
    while messag:
        log.info("Empenzando ciclo")
        find_game = None
        for game, price in best_price_game.items():
            price_game = get_price(game)
            if price_game <= price and price_game > 0: 
                bot.sendMessage(
                chat_id=chatID,
                text="Alerta mmguevo porfin hay tremenda oferta, El precio es: {} \n" 
                "aqui tienes el link papuh: {}".format(price_game, game)
                )
                messag = False
                find_game = game
        log.info("Variable de while: {}".format(messag))
        if find_game:
            del best_price_game[find_game]
            log.info(best_price_game)

def start(update, context): # Creando funcion de comienzo
    bot = context.bot
    chatID = update.message.chat_id
    bot.sendMessage(
        chat_id=chatID,
        text="Hola soy Pepot Ofertones y te vendo a traer las mejores ofertas puto pobre OwO\n"
             "Estos son los comandos:\n\n"
             "/getGames: Lista de juegos en oferta.\n\n"
             "Digite 'comenzar' para analizar los precios constantemente. Una vez que se encuentre un precio deseado"
             "tendra que digitar nuevamente 'comenzar' ya que una vez encontrado un solo precio se dejara de hacer el reconocimiento."
    )

def get_games(update, context): # Listar todos los juegos que va analizar los bots
    bot = context.bot
    chatID = update.message.chat_id
    all_games(bot, chatID)


def message_on(update, context): # Comenzar el analisis recursivo hasta encontrar el precio
    bot = context.bot
    chatID = update.message.chat_id
    text = update.message.text
    text_lower = text.lower()
    if text_lower == "comenzar":
        messa = True
        alert_games(bot, chatID)

def main():
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('getGames', get_games))
    dispatcher.add_handler(MessageHandler(Filters.text, message_on))
    updater.start_polling()
    updater.idle()
        
if __name__ == "__main__":
    main()   