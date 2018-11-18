DM = None

def set_DM(bot, update):
    global DM
    if DM == None:
        DM = update.message.from_user.first_name
        bot.sendMessage(chat_id=update.message.chat_id,
                        text=DM + " has been set as Dungeon Master")
    else:
        bot.sendMessage(chat_id=update.message.chat_id,
                        text="DM " + DM + " has already been set!")
