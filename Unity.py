"""
Created by hatim tachi.
Copyright © 2018 hatim tachi. All rights reserved.

"""
import beautifulSoupSC


class Unity(beautifulSoupSC.beautifulSoupSC):
    def __init__(self, url):
        beautifulSoupSC.beautifulSoupSC.__init__(self, url)
        self.url = url

    def getTopics(self, url):
        soup = self.readUrl(url)
        res = []
        for d in soup.find_all('div', class_="question-summary"):
            if d.find_all('div', class_="status answered-accepted"):
                for links in d.find_all('a', class_="question-hyperlink"):
                    res.append("https://stackoverflow.com/" + links['href'])
        return res

    def getPageNumbers(self, url):
        soup = self.readUrl(url)
        return int(soup.find_all("span", class_="page-numbers")[-2].getText())

    def getQuestionAndResponse(self, url):
        soup = self.readUrl(url)
        questionHeader = soup.find('a', class_="question-hyperlink")
        questionHeader = questionHeader.text
        postQ = soup.find_all('div', class_="question")
        _id = postQ[0]['data-questionid']
        question = self.extractTextAndCodeFromPost(postQ[0])
        postR = soup.find_all('div', class_="answer accepted-answer")
        response = self.extractTextAndCodeFromPost(postR[0])
        return [_id, questionHeader, question, response]

    @staticmethod
    def extractTextAndCodeFromPost(post):
        res = post.find('div', class_='post-text')
        resQ = []
        resCo = []
        for q in res.find_all('p'):
            resQ.append(q.text)
        for co in res.find_all('pre'):
            resCo.append(co.text)
        return {"text": resQ, "code": resCo}



