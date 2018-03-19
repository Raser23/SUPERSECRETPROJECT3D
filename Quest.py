import time
import threading
import config as CFG
from VK import VKUser as vkUser
import json

users = {}

personagePhrases = {}

userRybkin1 = vkUser(CFG.VKTOKENR1)
userRybkin2 = vkUser(CFG.VKTOKENR2)

states ={}


def StartQuestFor(id):
    obj = {"userId": id, "questEnded": False, "currentState": "-1", "currentAct": 1, "currentRybkin": 1,
           "sendedMessage": False}

    users[id] = obj



def NextAct(id):
    if(users[id]["currentAct"] == 1):
        users[id]["currentRybkin"] = 2
        users[id]["currentState"] = "2.1"
        users[id]["sendedMessage"] = True
        users[id]["questEnded"] = True

    if(users[id]["currentAct"] == 2):
        users[id]["currentRybkin"] = 1
        users[id]["currentState"] = "3.1"
        users[id]["sendedMessage"] = True
    if(users[id]["currentAct"] == 3):
        users[id]["questEnded"] = True
    users[id]["currentAct"] +=1
    pass



def LoadStates():

    #addQuestState("1.1")
    #addQuestState("2.1")
    addQuestState("3.1")

    print(states)

def LoadPersonages():
    global personagePhrases
    for personage in [1,2]:
        f = open('Personages/' + str(personage), 'r')
        phrases = json.loads(f.read())
        personagePhrases[personage] = phrases
    print(personagePhrases)
    pass


def addQuestState(fileName):
    # 0 - default 1 - skip 2 - need to read 3 - pohui na otvet 4-strong 5 - lite
    global states
    f = open('textes/'+fileName, 'r')

    print(fileName)
    state = json.loads(f.read())
    name = state["StateName"]
    states[name] = {}
    states[name]["text"] = state["text"]
    states[name]["variants"] = state["variants"]
    states[name]["type"] = state["type"]
    states[name]["lastInAct"] = state["lastInAct"]

    if(not state["lastInAct"]):
        for variant in state["variants"]:
            if (variant[1] not in states):
                addQuestState(variant[1])

    pass

def SendMessage(user, text , id):
    return user.SendMessageToUser(users[id]["userId"], text)

def SendStateMessage(currentPresonage,user,id):
    state = states[users[id]["currentState"]]
    text = state["text"]

    if(state["type"] == 0):#если есть варианты ответов
        a = 1
        text = text + "\n\n"+ personagePhrases[currentPresonage]["ChooseAnswerVariants"] +"\n["
        for variant in states[users[id]["currentState"]]["variants"]:
            text = text +str(a)+": " + variant[0] +" "
            a+=1
        text = text + "]"
    return SendMessage(user,text,id)


def GetMessage(user,currentPersonage,message,id):
    #global sendedMessage,currentState,states

    state = users[id]["currentState"]

    originalMessage = message
    message = message.replace(" ","")

    variantsCount = len(states[users[id]["currentState"]]["variants"])

    if(states[users[id]["currentState"]]["type"] == 3):
        message = "1"

    if (states[state]["type"] == 3):
        message = int(message)
        users[id]["currentState"] = states[state]["variants"][message - 1][1]
        users[id]["sendedMessage"] = False

    if(states[state]["type"] == 0):
        if(message.isdigit()):
            message = int(message)
            if(message <= variantsCount ):
                users[id]["currentState"] = states[state]["variants"][message - 1][1]
                users[id]["sendedMessage"] = False
            else:
                SendMessage(user,personagePhrases[currentPersonage]["IncorrestAnswerT0"],id)
        else:
            SendMessage(user,personagePhrases[currentPersonage]["IncorrestAnswerT0"],id)

    message = originalMessage
    if(states[state]["type"] == 4):
        givenRightAnswer = False
        for variant in states[state]["variants"]:
            if(variant[0] == message):
                users[id]["currentState"] = variant[1]
                users[id]["sendedMessage"] = False
                givenRightAnswer = True
        if(not givenRightAnswer):
            SendMessage(user,personagePhrases[currentPersonage]["IncorrestAnswerT4"],id)

    if (states[state]["type"] == 5):
        givenRightAnswer = False
        messageWords = message.split(" ")
        for variant in states[state]["variants"]:
            answerWords = variant[0].split(" ")
            for word in messageWords:
                if (word in answerWords and not givenRightAnswer):
                    users[id]["currentState"] = variant[1]
                    users[id]["sendedMessage"] = False
                    givenRightAnswer = True
        if (not givenRightAnswer):
            SendMessage(user, personagePhrases[currentPersonage]["IncorrestAnswerT5"], id)


def Rybkin(user,number,id):
    #global sendedMessage, currentState
    myTurn = (users[id]["currentRybkin"] == number)
    if (myTurn and not users[id]["sendedMessage"]):
        print("Отправил сообщение")
        users[id]["sendedMessage"] = SendStateMessage(number,user,id)
        if (states[users[id]["currentState"]]["lastInAct"]  and users[id]["sendedMessage"]):
            NextAct(id)
            return
        if (users[id]["sendedMessage"] and states[users[id]["currentState"]]["type"] == 1):
            users[id]["currentState"] = states[users[id]["currentState"]]["variants"][0][1]
            users[id]["sendedMessage"] = False

    else:
        print("Ожидаю сообщения")
        messages = user.GetHistory(users[id]["userId"])[1:]
        if (len(messages) == 0):
            return
        lastMessage = messages[0]
        if lastMessage['out'] == 0 and lastMessage['read_state'] == 0:
            if(myTurn):
                GetMessage(user,number,lastMessage['body'],id)
            else:
                SendMessage(user,personagePhrases[number]["NotMyTurn"],id)
        else:
            print("Ничего интересного")

def Quester():

    while(True):
        #print("here")
        print(users)
        delete = []
        for user in users:
            if(users[user]["questEnded"]):
                print("Квест закончен для "+str(user))
                delete.append(user)
                continue

            if(users[user]["currentState"] == "-1"):
                af = userRybkin1.AreFriends(user)
                if(af == 0):
                    userRybkin1.AddFriend(user)
                else:
                    users[user]["currentState"] = "1.1"
            else:
                Rybkin(userRybkin1, 1, user)
                Rybkin(userRybkin2, 2, user)
        for d in delete:
            del users[d]
        time.sleep(7)



LoadStates()
LoadPersonages()
t1 = threading.Thread(target=Quester)
t1.start()