from flask import Flask, request, render_template
import config
import os



#bot = telebot.TeleBot(config.TOKEN)
server = Flask(__name__)



#server handlers

@server.route("/")
def webhook():
    return render_template('hello.html')

@server.route("/wakeup")
def wakeup():
    #print("pinged")
    return "Never sleeps", 200

@server.route('/startQuest/<int:usedId>')
def show_post(usedId):
    # show the post with the given id, the id is an integer

    print(usedId)
    return 'Post %d' % usedId

import NotSleeping
server.run(host="0.0.0.0", port=os.environ.get('PORT', 5000))
server = Flask(__name__)

