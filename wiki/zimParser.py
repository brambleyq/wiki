import time
from libzim.reader import Archive,Item,Entry
from libzim.search import Query,Searcher
from bs4 import BeautifulSoup
import os
import random
import pyttsx3


class ZimReader:
    def __init__(self,path:str):
        self.path = path
        self.file = Archive(path)
        self.n = self.file.all_entry_count
        self.name = path.split('_')[-3]
    
    def getRandomItem(self) -> Item:
        entry = self.file.get_random_entry()
        item = entry.get_item()
        self.last_item = item
        return item
    
class WikiReader:
    def __init__(self,path:str='data'):
        self.folder = path
        self.zims:list[ZimReader] = [ZimReader(path+'/'+file) for file in os.listdir(path)]

    def getRandomPage(self) -> BeautifulSoup:
        zim = random.choices(self.zims,[zim.n for zim in self.zims])[0]
        self.last_zim = zim
        html = zim.getRandomItem().content.tobytes().decode("utf-8")
        return BeautifulSoup(html,features='html.parser')
    
    def lineSimplifier(self,page:str) -> list[str]:
        lines = [[word for  word in line.split()] for line in page.splitlines()]


    def readAloud(self):
        fulltext:str = self.getRandomPage().text
        lines = [line.strip() for line in fulltext.splitlines() if line.strip()]
        fulltext = '\n'.join(lines)
        for line in lines:
            if line == 'References':
                break
            print(line)
            engine = pyttsx3.init()
            engine.say(line)
            time.sleep(.5)
            engine.runAndWait()
            time.sleep(.5)
            engine.stop()
            del(engine)



        
if __name__ == '__main__':
    zim = WikiReader('data/zims')
    while True:
        print(zim.readAloud())
        result = input(':')
        if result:
            break