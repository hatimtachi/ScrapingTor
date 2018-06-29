"""
Created by hatim tachi.
Copyright © 2018 hatim tachi. All rights reserved.

"""

import bs4
import requests
from stem.control import Controller
from stem import Signal
from fake_useragent import UserAgent


class beautifulSoupSC:
    def __init__(self, url):
        self.url = url
        self.ui = UserAgent()

    def readUrl(self, url):
        session = self.get_tor_session()
        html = session.get(url)
        soup = bs4.BeautifulSoup(html.text, 'html.parser')
        if soup.find("div", class_="msg") is not None:
            print(soup.find("div", class_="msg"))
            self.renewAndCheckIpChange()
            session = self.get_tor_session()
            html = session.get(url)
            soup = bs4.BeautifulSoup(html.text, 'html.parser')
        return soup

    @staticmethod
    def get_tor_session():
        session = requests.session()
        # Tor uses the 9050 port as the default socks port
        session.proxies = {'http': 'socks5://127.0.0.1:9050',
                           'https': 'socks5://127.0.0.1:9050'}
        return session

    @staticmethod
    def renew_connection():
        with Controller.from_port(port=9051) as controller:
            controller.authenticate()
            controller.signal(Signal.NEWNYM)

    def renewAndCheckIpChange(self):
        session = self.get_tor_session()
        print(session.get("http://httpbin.org/ip").json()['origin'], "last_ip")
        last_Ip = session.get("http://httpbin.org/ip").json()['origin']
        new_Ip = last_Ip
        while last_Ip == new_Ip:
            self.renew_connection()
            session = self.get_tor_session()
            new_Ip = session.get("http://httpbin.org/ip").json()['origin']
        print(session.get("http://httpbin.org/ip").json()['origin'], "new_ip")


