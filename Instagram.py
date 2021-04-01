import requests
from bs4 import BeautifulSoup
import urllib.request
import os
from mongoengine import *
import selenium.webdriver as webdriver
import Post_Insta

class Instagram_posts(object):
    
    def __init__(self,Posts_link):
        self.Posts_link = Posts_link
    Posts = {}

    def get_comment(self,soup):
        comments = soup.find_all("div", {"class":"EtaWk"})
        return comments[0].get_text()
    
    def get_image(self,soup,driver,filename='test'):
        photo = soup.find_all("img")[1]['src']
        if not os.path.exists('Photos_Insta'):
            os.makedirs('Photos_Insta')
        urllib.request.urlretrieve(photo,'./Photos_Insta/'+filename+'.png')
        
    def Scrap(self):
        for idx, link in self.Posts_link.items():
            driver = webdriver.Edge(executable_path=r'D:\Users\amine\Downloads\msedgedriver(1).exe')
            driver.get(link)
            soup = BeautifulSoup(driver.page_source)
            self.Posts[idx] = {}
            self.Posts[idx]['comments'] = self.get_comment(soup)
            self.get_image(soup,driver,str(idx))
    
    
    def Save(self):
        for idx,post in self.Posts.items():
            p = Post_Insta.Post_Insta(_id=str(idx))
            p.comments = post['comments']
            Photo = open('./Photos/'+str(idx)+'.png','rb')
            p.image.put(Photo,filename=str(idx)+'.png')
            p.save()