from flask import Flask, request
import config
import os



#bot = telebot.TeleBot(config.TOKEN)
server = Flask(__name__)



#server handlers

@server.route("/")
def webhook():

    return "ok", 200

@server.route("/wakeup")
def wakeup():
    #print("pinged")
    return "Never sleeps", 200



import NotSleeping
server.run(host="0.0.0.0", port=os.environ.get('PORT', 5000))
server = Flask(__name__)

