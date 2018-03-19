from flask import Flask, request, render_template
import config
import os
import Quest as q

server = Flask(__name__)

#server handlers

@server.route("/")
def webhook():
    return render_template('hello.html')

@server.route("/wakeup")
def wakeup():
    #print("pinged")
    return "Never sleeps", 200

@server.route('/startQuest/<int:userId>')
def show_post(userId):
    print("Starting quest for %d"% userId )

    q.StartQuestFor(userId)
    return 'Post %d' % userId


import NotSleeping
server.run(host="0.0.0.0", port=os.environ.get('PORT', 5000))
server = Flask(__name__)

