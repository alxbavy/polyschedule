from vkbottle import Bot

from config import api
from polyschedule.handlers import labelers


if __name__ == "__main__":
    bot = Bot(api=api)

    for labeler in labelers:
        bot.labeler.load(labeler)

    bot.run_forever()
