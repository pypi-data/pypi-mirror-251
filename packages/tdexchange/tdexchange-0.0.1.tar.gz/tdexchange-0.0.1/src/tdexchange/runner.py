import time

from src.tdexchange.bot import RegularBot, MarketPrice, PairPrice


def typical():
    bots = []
    price = MarketPrice()
    pair = PairPrice(price)
    for i in range(1, 5):
        name = f'bot-0{i}'
        bot = RegularBot(name, name, price, pair)
        bot.run()
        bots.append(bot)

    try:
        while True:
            time.sleep(1 / 25)
    except KeyboardInterrupt:
        print('ctrl-c encountered, exiting')
    finally:
        for bot in bots:
            bot.stop()

        exit()
