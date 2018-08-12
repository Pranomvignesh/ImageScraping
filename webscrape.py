from bs4 import BeautifulSoup
import requests
import re
import urllib2
import os
import cookielib
import json

def get_soup(url,header):
    return BeautifulSoup(urllib2.urlopen(urllib2.Request(url,headers=header)),'lxml')


query = raw_input("Enter the search query : ")# you can change the query for the image  here
imgCount = '100' # initialize the imgcount
imgCount = raw_input("Enter the no of images to be downloaded(< 100):")
image_name='_'.join(query.split())
#print image_name
query= query.split()
query='+'.join(query)
url="https://www.google.co.in/search?q="+query+"&source=lnms&tbm=isch"
#print url
#add the directory for your image here
DIR="Pictures"
header={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"
}
soup = get_soup(url,header)
#print(soup.find_all("div",{"class":"rg_meta"}))

ActualImages=[]# contains the link for Large original images, type of  image
for a in soup.find_all("div",{"class":"rg_meta"}):
    link , Type =json.loads(a.text)["ou"]  ,json.loads(a.text)["ity"]
    ActualImages.append((link,Type))
#print ActualImages[0]
#
#print  "there are total" , len(ActualImages),"images"
#
if not os.path.exists(DIR):
    os.mkdir(DIR)
DIR = os.path.join(DIR,image_name)

if not os.path.exists(DIR):
    os.mkdir(DIR)

####print images
for i , (img , Type) in enumerate( ActualImages):
    if(i+1 > int(imgCount) ):
        break
    try:
        req = urllib2.Request(img, headers={'User-Agent' : header})
        raw_img = urllib2.urlopen(req).read()

        cntr = len([i for i in os.listdir(DIR) if image_name in i]) + 1
        if len(Type)==0:
            f = open(os.path.join(DIR , image_name + "_"+ str(cntr)+".jpg"), 'wb')
        else :
            f = open(os.path.join(DIR , image_name + "_"+ str(cntr)+"."+Type), 'wb')

        f.write(raw_img)
        f.close()
#        print (str(cntr)+" downloaded...")
    except Exception as e:
        print "could not load : "+img
        print e
print ("Download Complete")
