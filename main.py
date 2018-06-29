import Unity
import tools
import os
import threading
import queue


def main(url, numbreOfThreads):
    unityBT = Unity.Unity(url)
    dataDirName = "data"
    print("1 - getAllLinks")
    if not os.path.exists("./" + dataDirName):
        os.makedirs("./" + dataDirName)
    listLinks = tools.getQueueLinks(unityBT, url)
    queueLock = threading.Lock()
    workQueue = queue.Queue(len(listLinks))
    tools.startScrapingLinks(listLinks, numbreOfThreads, queueLock, workQueue, unityBT, dataDirName)
    print("Exiting Main Thread")


if __name__ == '__main__':
    main(url='https://stackoverflow.com/questions', numbreOfThreads=120)
