import config as CFG
import vk

class VKUser:
    def __init__(self, acces_token):
        self.acces_token = acces_token
        self.session = vk.AuthSession(access_token=self.acces_token)
        self.api = vk.API(self.session)

    def GetUserGroups(self,userId):
        counter = 0
        errorCounter = 0
        while True:
            try:
                if (errorCounter >= 20):
                    print("skipped")
                    return []

                result = api.users.getSubscriptions(user_id=userId)['groups']['items']
                return result
            except:
                errorCounter += 1
                pass


    def GetGroupUserIds(self,groupId , count = -1):
        loadCount = 100
        first={}
        while True:
            try:
                first = self.api.groups.getMembers(group_id = groupId,offset = 0, count = loadCount)
                break
            except:
                pass
        userIds = first['users']

        maxCount = first['count']
        if(count >= 0):
            maxCount = min(maxCount, count)

        loadedUsers = 0

        while loadedUsers < maxCount:
            print(str(loadedUsers)+" / "+str(maxCount))
            try:
                loadedUsers = len(userIds)
                userIds = userIds + self.api.groups.getMembers(group_id = groupId,offset = loadedUsers, count = loadCount)['users']
            except:
                pass

        return userIds

    def textUserGroups(self,groups):
        text =""
        for g in groups:
            text = text + str(g) +" "
        return text

    def GetMostPopularGroups(self,userIds ,isGood, maxCount = 5000):

        groupCount = 0
        groups = {}

        getted = 0
        print((userIds))
        for id in userIds:
            print(id)
            while True:
                try:
                    a = self.GetUserGroups(id)
                    print((a))
                    for group in a:

                        if group in groups:
                            #print(groups)
                            groups[group] += 1
                        else:
                            if(groupCount < maxCount):
                                groups[group] = 1
                            else:
                                pass
                    break
                except:
                    pass
            getted +=1

            #print("get: " + str(getted))
        return [a for a in groups]

    def SaveUser(self,isGood, userId ,fileName):
        a=[]
        while True:
            try:
                a = self.GetUserGroups(userId)
                break
            except:
                pass
        text = self.textUserGroups(a)

        path = 'Data/'
        if(isGood):
            path = path + 'White/'
        else:
            path = path + 'Black/'
        path = path + fileName +'.txt'
        with open(path, 'w') as f:
            f.write(text)

    def SaveUsers(self,isGood, userIds):
        import time

        startName = time.time()
        counter = 0

        for idn in userIds:
            self.SaveUser(isGood,idn,str(startName + counter))
            counter +=1

    def GetUserById(self,id):
        errorCount = 0
        while True:
            try:
                if(errorCount > 20):
                    return [{'uid': 91304376, 'first_name': 'Алексей', 'last_name': 'Филин'}]
                return (self.api.users.get(user_ids = id))
            except:
                errorCount+=1

    def GetDialogs(self):
        return (self.api.messages.getDialogs(version = 5.73))

    #messages.getHistory

    def GetHistory(self,userId):
        return (self.api.messages.getHistory(user_id = userId, version = 5.73))

    #messages.markAsRead
    def MarkAsReaded(self,userId):
        return (self.api.messages.markAsRead(peer_id = userId, version = 5.73))


    def SendMessageToGroup(self,groupId,message):
        self.api.messages.send(peer_id = (2000000000 + groupId), message = message,v = 5.73)
        pass

    def SendMessageToUser(self,userId,message):
        try:
            self.api.messages.send(user_id = userId, peer_id = (userId), message = message,v = 5.73)
            return True
        except:
            print("error")
            return False

    # 78752776 106
    # 477883548
#print(GetUserById("alekseifilin"))
#print(GetUserGroups(0))

    def AddFriend(self,id):
        self.api.friends.add(user_id = id,v = 5.73)

    def AreFriends(self,id):
        return self.api.friends.areFriends(user_ids=id, v=5.73)[0]["friend_status"]
