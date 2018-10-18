# get maoyanmovies

import requests
from bs4 import BeautifulSoup
import random
import time

# url = 'http://maoyan.com/board/4'

agentlist = []
with open('useragent.txt', 'r') as br:
    for i in range(36):
        agentlist.append(br.readline().lstrip('User-Agent:').rstrip('\n'))


def useragent():
    agent = agentlist[random.randint(1, 35)]
    return agent


def urllist():
    urlist = ['http://maoyan.com/board/4']
    for num in range(1, 10):
        url = 'http://maoyan.com/board/4?offset={}'.format(num*10)
        urlist.append(url)
    return urlist


def gethtml(link):
    namelist = []
    starlist = []
    scorelist = []
    head = {'User-Agent': useragent(),
            'Connection': 'keep-alive'
            }

    ht = requests.get(link, headers=head)
    ht.encoding = 'UTF-8'
    htx = ht.text
    hts = BeautifulSoup(htx, 'lxml')
    for n in hts.find_all('dd'):

        namelist.append(str(n.find_all('p', class_='name')[0].text).replace('\n', '').replace(' ', ''))
        starlist.append(str(n.find_all('p', class_='star')[0].text).replace('\n', '').replace(' ', '').replace(',', '-'))
        scorelist.append(str(n.find_all('p', class_='score')[0].text).replace('\n', '').replace(' ', ''))
    summ = [namelist, starlist, scorelist]
    return summ


def main():
    nalist = {}
    listofurl = urllist()
    count = 1
    for url in listofurl:
        print(count, end='\n')
        res = gethtml(url)
        for num in range(10):
            nalist[res[0][num]] = [res[1][num], res[2][num]]
        time.sleep(3)
        count += 1
    return nalist


if __name__ == '__main__':
    resu = main()
    for key in resu.keys():
        with open('result.csv', 'a', encoding='utf-8') as resultt:
            resultt.write('{0},{1},{2}\n'.format(key, str(resu[key][0]), resu[key][1]))
