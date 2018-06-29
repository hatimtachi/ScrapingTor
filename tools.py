import ThreadQueue
import SingleThread
import os
import json


def process_data(threadId, unityBT, q, queueLock, workQueue, dataDirName):
    while not ThreadQueue.Thread.exitFlag:
        try:
            queueLock.acquire()
            if not workQueue.empty():
                link = q.get()
                queueLock.release()
                res = unityBT.getTopics(link)
                for li in res:
                    dataParse = unityBT.getQuestionAndResponse(li)
                    data = createJson(dataParse, li)
                    with open(dataDirName + "/" + str(dataParse[0]) + '.json', 'w') as outfile:
                        json.dump(data, outfile)
                print(threadId, "--", link)
            else:
                queueLock.release()
        except Exception as e:
            raise str(e)
            pass

def createJson(dataParse, url):
    array = []
    isResponse = False
    key = "question"
    array.append({"url": url})
    array.append({"questionHeader": dataParse[1]})
    print(len(dataParse), url)
    for i in range(2, len(dataParse)):
        data = {}
        if isResponse:
            key = "response"
        for re in dataParse[i]:
            if re is "text":
                if type(dataParse[i][re]) == list:
                    data["text"] = "\n".join(str(x) for x in dataParse[i][re])
                else:
                    data["text"] = dataParse[i][re]
            else:
                if type(dataParse[i][re]) == list:
                    data["code"] = "".join(str(x) for x in dataParse[i][re])
                else:
                    data["code"] = dataParse[i][re]
        rest = {key: data}
        array.append(rest)
        isResponse = True
    return array


def getAllLinksSujet(threadId, url, unityBTSC):
    listOfLinks = []
    listOfLinks.extend(unityBTSC.getAllSujet(url))
    linkNext = unityBTSC.hasNextPage(url)
    while linkNext is not None:
        if SingleThread.SingleThread.exitFlag:
            threadId.exit()
        listOfLinks.extend(unityBTSC.getAllSujet(linkNext))
        linkNext = unityBTSC.hasNextPage(linkNext)
    return listOfLinks


# create SignleThreads to get all links from url
def startCrowlingAllLinks(links, unityBT, dirName):
    threads = []
    for link in range(len(links)):
        threads.append(SingleThread.SingleThread(link, links[link], unityBT, dirName))
    for i in range(len(threads)):
        threads[i].start()
    for i in range(len(threads)):
        threads[i].join()


def getQueueLinks(unityBT, url):
    res = []
    print("in get Queue Links")
    for i in range(41200, unityBT.getPageNumbers(url)):
        res.append(url + "?page=" + str(i) + "&sort=newest&pagesize=50")
    return res


def getAllDiscussion(url, unityBT):
    listDisc = []
    listDisc.extend(unityBT.getDiscussions(url))
    nextLink = unityBT.hasNextPage(url)
    while nextLink is not None:
        listDisc.extend(unityBT.getDiscussions(nextLink))
        nextLink = unityBT.hasNextPage(nextLink)
    return listDisc


def writeDiscussionJson(nameDir, unityBT, url, listDiscussion, idLink):
    if not os.path.exists('./' + nameDir):
        os.makedirs("./" + nameDir)
    file = open("./" + nameDir + "/" + idLink + ".json", "w")
    title = unityBT.getTitleComments(url)
    jsonArrayTitle = []
    jsonArrayDisc = []
    for ti in title:
        jsonTitle = {'path': ti}
        jsonArrayTitle.append(jsonTitle)
    for disc in listDiscussion:
        jsonDisc = {"text": disc}
        jsonArrayDisc.append(jsonDisc)
    dic = {"title ": jsonArrayTitle, "Discussion": jsonArrayDisc}
    file.write(json.dumps(dic, ensure_ascii=False))


def startScrapingLinks(listLinks, nbThread, queueLock, workQueue, unityBT, dataDirName):
    threadList = [str(thread) for thread in range(nbThread)]
    ThreadQueue.Thread.exitFlag = 0
    nameList = listLinks
    threads = []
    for tId in threadList:
        thread = ThreadQueue.Thread(tId, workQueue, queueLock, workQueue, unityBT, dataDirName)
        thread.start()
        threads.append(thread)

    queueLock.acquire()
    for data in nameList:
        workQueue.put(data)
    queueLock.release()

    while not workQueue.empty():
        pass

    ThreadQueue.Thread.exitFlag = 1

    for t in threads:
        t.join(timeout=1)
