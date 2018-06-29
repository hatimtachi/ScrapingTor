"""
Created by hatim tachi.
Copyright © 2018 hatim tachi. All rights reserved.

"""
import threading
import time
import ThreadQueue
import os
import tools


class SingleThread(threading.Thread):
    exitFlag = 0
    listOfDeadThreads = 0

    def __init__(self, threadID, link, unityBT, dirName):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.link = link
        self.unityBT = unityBT
        self.dirName = dirName

    def run(self):
        print("Starting " + self.name)
        listOfLinks = tools.getAllLinksSujet(self.name, self.link, self.unityBT)
        self.saveLinks(listOfLinks, self.dirName)
        listOfLinks.clear()
        SingleThread.listOfDeadThreads += 1
        print("Exiting " + self.name)

    @staticmethod
    def saveLinks(listL, dirName):
        if not os.path.exists("./" + dirName):
            os.makedirs("./" + dirName)
        file = open("./" + dirName + "/links.txt", "a")

        for link in listL:
            file.write(str(link) + "\n")
