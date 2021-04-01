import requests
from bs4 import BeautifulSoup
import urllib.request
import os
from mongoengine import *
import selenium.webdriver as webdriver
import Post_Facebook

class Facebook_posts(object):
    
    def __init__(self,Posts_link):
        self.Posts_link = Posts_link
    Posts = {}
    connect(db="Facebook",host="localhost",port=27017)
    
    def get_content(self,soup):
        content = soup.find_all("p")
        cnts=[]
        for cnt in content:
            cnts.append(cnt.get_text())
        return ' '.join(cnts)
    
    def get_comment(self,soup):
        comment = soup.find_all("div", {"class": "ct"})
        comments = []
        for cmnt in comment:
            comments.append(cmnt.get_text())
        return ';'.join(comments)
    
    def get_image(self,soup,filename='test'):
        photo = soup.find_all("img")[1]['src']
        if not os.path.exists('Photos'):
            os.makedirs('Photos')
        urllib.request.urlretrieve(photo,'./Photos/'+filename+'.png')
    
    def parse_html(self,request_url):
        with requests.Session() as session:
            #post = session.post(login_basic_url, data=payload)
            parsed_html = session.get(request_url)
        return parsed_html
    
    def Scrap(self):
        for idx, link in self.Posts_link.items():
            soup = BeautifulSoup(self.parse_html(link).content, "html.parser")
            self.Posts[idx] = {}
            self.Posts[idx]['content'] = self.get_content(soup)
            self.Posts[idx]['comments'] = self.get_comment(soup)
            self.get_image(soup,str(idx))
    
    def Save(self):
        for idx,post in self.Posts.items():
            p = Post_Facebook.Post(_id=str(idx))
            p.content = post['content']
            p.comments = post['comments']
            Photo = open('./Photos/'+str(idx)+'.png','rb')
            p.image.put(Photo,filename=str(idx)+'.png')
            p.save()