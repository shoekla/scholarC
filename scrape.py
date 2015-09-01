import urllib2
import re
import nltk
import csv
import time
import requests
from bs4 import BeautifulSoup
from urllib2 import urlopen
import os
def refresh():
	os.remove("static/SearchLinks.txt","w")
	os.remove("static/Social-Media-Links.txt","w")
	os.remove("static/Contacts.txt","w")
	os.remove("static/Data.txt","w")
	os.remove("static/All.txt","w")
	os.remove("static/AllButSocial.txt","w")
	os.remove("test.txt","w")
countS=0
def is_in_arr(lis,s):
	result=False
	for item in lis:
		if item==s:
			result=True
	return result
def deleteDuplicates(lis):
	newLis=[]
	for item in lis:
		if item not in newLis:
			print "Delteing Dupes"
			newLis.append(item)
	return newLis
def getScore(url,eth,grade,major,gender,loc):
	try:
		htmlfile=urllib2.urlopen(str(url))
		hText=htmlfile.read()
		data=hText.lower()
		score=data.count(str(eth))
		if grade=="high school students in":
			score=data.count("high school")+score
		else:
			score=data.count("college")+score
		score=data.count(str(major))+score
		if gender=="male":
			score=data.count("male")+score
		else:
			score=data.count("female")+score
		score=data.count(str(loc))+score
		return score
	except:
		return 0

def getData(url):
	try:

		regex='<p>(.+?)</p>'
		headers='Info In Paragrapgh'

		pattern = re.compile(regex);
		htmlfile=urllib2.urlopen(str(url))
		htmltext=htmlfile.read()
		title=re.findall(pattern,htmltext)
		return title
	except:
		print "Data Error At "+str(url)

def getName(url):
	try:
		regex='<title>(.+?)</title>'
		headers='Title:'
		pattern = re.compile(regex);
		htmlfile=urllib2.urlopen(url)
		htmltext=htmlfile.read()
		title=re.findall(pattern,htmltext)
		return title[0]
	except:
		return str(url)

def getGoodLink(url):
	k = url.rfind("/")
	return url[:k+1]
def getHTML(url):
	try:
		htmlfile=urllib2.urlopen(str(url))
		htmltext=htmlfile.read()
		htmltext.replace("<!Doctype html>","")
		htmltext.replace("<html","")
		htmltext.replace("</html>","")
		tokens = nltk.word_tokenize(htmltext)
		return tokens
	except:
		return "Error Occured"
#nltk.download()
def getPhone(url):
	try:
		tokens=getHTML(url)
		nums=[1,2,3,4,5,6,7,8,9,0]
		contacts=[]
		string=""

		for i in range(0,len(tokens)):
			item=tokens[i]
			if len(item)==10:
				number=True

				if item.isalpha():
					number=False

				if item[3:6]=="555":
					number=False

				if str(item[0])!="1" or str(item[0])!="2" or str(item[0])!="3" or str(item[0])!="4" or str(item[0])!="5" or str(item[0])!="6" or str(item[0])!="7" or str(item[0])!="8" or str(item[0])!="9" or str(item[0])!="0":
					number=False
				if number==True and item not in contacts:
					contacts.append(item)
			if len(item)==12:
				number=True
				"""
				if item[3]!= "-" or item[7]!="-":
					if item[3]!="." or item[7]!=".":
						number=False
				"""
				if str(item[0]).isalpha() or str(item[1]).isalpha() or str(item[2]).isalpha() or str(item[3]).isalpha() or str(item[4]).isalpha() or str(item[5]).isalpha() or str(item[6]).isalpha() or str(item[7]).isalpha() or str(item[8]).isalpha() or str(item[9]).isalpha() or str(item[10]).isalpha() or str(item[11]).isalpha():
					number=False
				if item[4:7]=="555":
					number=False

				if number==True and item not in contacts:
					if "Fax" in tokens[i-2]:
						contacts.append("Fax: "+item)
					else:
						contacts.append("Phone: "+item)
		return contacts
	except:
		return "Error Occured"

def getEmail(url):
	try:
		tokens=getHTML(url)
		contacts=[]
		for i in range(0,len(tokens)):
			if "@" in tokens[i]:
				string= str(tokens[i-1])
				if string[0].isalpha():
					string = string +str(tokens[i])
					string = string +str(tokens[i+1])
					endA=str(tokens[i+1])
					if endA.find(".")>=0:
						if is_in_arr(contacts,tokens[i])==False:
							if string.endswith(".")==False:
								contacts.append(string)
			if "at"==tokens[i]:
				if tokens[i-1]=="[" and tokens[i+1]=="]":
					string=str(tokens[i-2])+"@"+str(tokens[i+2])
					contacts.append(string)
			if len(tokens[i])==3:
				if tokens[i].isalpha==False:
					if (tokens[i+1].isalpha==False and len(tokens[i+1])==3) and (tokens[i+2].isalpha()==False and len(tokens[i+2])==3) and item not in contacts:
						string = str(tokens[i]) +str(tokens[i+1])+str(tokens[i+2])
						contacts.append(string)
		new = deleteDuplicates(contacts)
		return new
	except:
		return "Error Occured"

def crawl(url,pages):
	try:
		arr=[]
		source_code=requests.get(url)
		plain_text=source_code.text
		soup=BeautifulSoup(plain_text)
		for link in soup.findAll('a'):

			href=link.get('href')
			href_test=str(href)
			#if href_test[0]!='/' and href_test[0]!='j' and href_test!='none' and href_test[0]!='#':
			if is_in_arr(pages,str(href))==False:
				if "microsoft" not in href_test and "facebook" not in href_test and "twitter" not in href_test and "google" not in href_test:
					if href_test.startswith("http"):
						pages.append(str(href))
					else:
						lin=getGoodLink(url)
						pages.append(lin+str(href))

	except:
		print "Error at: "+str(url)




def crawlLink(ina):
	links=[]
	finds=[]
	item=ina

	crawl(item,links)

	for link in links:
		crawl(link, finds)
	new=deleteDuplicates(finds)
	for link in new:
		linkText.write(link)
		linkText.write("\n")
	allFile.write("Crawled Links: \n")
	allSocial.write("Crawled Links \n")
	for link in new:
		allFile.write(str(link))
		allFile.write("\n")
		allSocial.write(str(link))
		allSocial.write("\n")

def crawlLinkScoial(url):
	try:
		pages=[]
		arr=[]
		source_code=requests.get(url)
		plain_text=source_code.text
		soup=BeautifulSoup(plain_text)
		for link in soup.findAll('a'):

			href=link.get('href')
			href_test=str(href)
			#if href_test[0]!='/' and href_test[0]!='j' and href_test!='none' and href_test[0]!='#':
			if is_in_arr(pages,str(href))==False:
				if "facebook" in href_test or "twitter" in href_test or "google" in href_test:

					lin=getGoodLink(url)
					pages.append(lin+str(href))
		newArr=deleteDuplicates(pages)
		for page in newArr:
			socialFile.write(page)
			socialFile.write("\n")
		allFile.write("Social-Media-Links: \n")
		for page in newArr:
			allFile.write(page)
			allFile.write("\n")



	except:
		print "Error at: "+str(url)
def contact(url):
	phone=getPhone(url)
	email=getEmail(url)
	second=[]
	for item in phone:
		second.append(str(item))
	for item in email:
		second.append(str(item))
	new=deleteDuplicates(second)
	for item in new:
		contactFile.write(item)
		contactFile.write("\n")
	allFile.write("Contact Info: \n")
	allSocial.write("Contact Info: \n")
	for page in new:
		allFile.write(page)
		allFile.write("\n")
		allFile.write(str(link))
		allFile.write("\n")
		allSocial.write(page)
		allSocial.write("\n")
		allSocial.write(str(link))
		allSocial.write("\n")		
	if len(new)>=1:
		contactFile.write("No contacts on "+str(url))
		allFile.write("No contacts on "+str(url))
		allSocial.write("No contacts on "+str(url))

def contactSearch(urls):
	second=[]
	for url in urls:
		print str(url)
		phone=getPhone(url)
		email=getEmail(url)
		third=[]
		for item in phone:
			third.append(str(item))
		for item in email:
			third.append("Email: "+str(item))
		if len(second)==0:
			third.append("No Contacts Found")
		second.append(third)
	new=deleteDuplicates(second)
	for i in range(0,len(urls)):
		contactFile.write("      Link: "+str(urls[i])+"\n \n")
		contactFile.write(new[i])
		contactFile.write("\n")
			
	if len(new)>=1:
		contactFile.write("No contacts on "+str(url))
		allFile.write("No contacts on "+str(url))
		allSocial.write("No contacts on "+str(url))


def link(url):
	crawlLink(url)
	crawlLinkScoial(url)
	contact(url)
	data=getData(url)
	dataFile.write(str(data))
	allFile.write("Data Aggregated: \n")
	allFile.write(str(data))
	allSocial.write("Data Aggregated: \n")
	allSocial.write(str(data))
def isLink(url):
	if str(url).startswith("http"):
		return True
	return False
def turnToSearch(text):
	search=text.replace(" ","%20")
	link="http://www.bing.com/search?q="+str(search)+"&qs=n&form=QBRE&pq="+str(search)+"&sc=9-6&sp=-1&sk=&cvid=6585c559beef41f3b942271b982e674a"
	return link
def crawlSearch(url,pages):
	try:
		arr=[]
		source_code=requests.get(url)
		plain_text=source_code.text
		soup=BeautifulSoup(plain_text)
		for link in soup.findAll('a'):

			href=link.get('href')
			href_test=str(href)
			#if href_test[0]!='/' and href_test[0]!='j' and href_test!='none' and href_test[0]!='#':
			if is_in_arr(pages,str(href))==False:
				if "microsoft" not in href_test and "facebook" not in href_test and "twitter" not in href_test and "google" not in href_test:
					if href_test.startswith("http"):
						if "bing" not in href_test:
							if "scholarships.com" not in href_test:
								pages.append(href)
								print str(href)
							else:
								if countS<2:
									crawl(href,pages)
									print "Crawling "+str(href)
									countS=countS+1
								else:
									print "Skiping "+str(href)
					else:
						pass


	except:
		print "Error at: "+str(url)
def getMoreSearch(url):
	try:
		pages=[]
		arr=[]
		source_code=requests.get(url)
		plain_text=source_code.text
		soup=BeautifulSoup(plain_text)
		pages.append(str(url))
		for link in soup.findAll('a'):

			href=link.get('href')
			href_test=str(href)
			#if href_test[0]!='/' and href_test[0]!='j' and href_test!='none' and href_test[0]!='#':
			if href_test.startswith("/search"):
				if "microsoft" not in str(url) and "microsoft" not in href_test:
					pages.append(str(url+href))

		return pages
	except:
		return []

def takeOutBing(arr):
	new=[]
	for ite in arr:
		item=str(ite)
		if "bing" not in item:
			new.append(ite)
	return new



def getLinksFromS(url):
	link=turnToSearch(str(url))
	a=getMoreSearch(link)
	b=[]
	for item in a:
		crawlSearch(item,b)
		print item
	for item in b:
		linkText.write(item)
		linkText.write("\n")

def findnth(haystack, needle, n):
    parts= haystack.split(needle, n+1)
    if len(parts)<=n+1:
        return -1
    return len(haystack)-len(parts[-1])-len(needle)
def findWhatToScrape(arr):
	new=[]
	testArr=[]
	for s in arr:
		begin=findnth(s,"/",1)
		end=findnth(s,"/",2)
		item=s[begin+1:end]
		if item not in testArr:
			testArr.append(item)
			new.append(s)
	return new

def searchQ(link):
	url=turnToSearch(str(link))
	b=getMoreSearch(url)
	a=[]
	for item in b:
		crawlSearch(item,a)
	for item in a:
		print item
		linkText.write(str(item))
		linkText.write("\n")	
	scrapes=findWhatToScrape(a)
	for item in scrapes:
		print item
		contactFile.write(str(item)+"\n")
		contact(item)
	allSocial.write("Data Aggregated: \n")
	allFile.write("Data Aggregated: \n")
	for item in scrapes:
		print item
		data=getData(item)
		dataFile.write(str(item))
		allFile.write("\n \n")
		dataFile.write(str(data))
		allFile.write("\n \n")
		allFile.write(item+"\n")
		allFile.write(str(data))
		allFile.write("\n \n")
		allSocial.write(item+"\n")
		allSocial.write(str(data))
		allSocial.write("\n \n")

def getScholar(eth,grade,loc,gender,major):
	text=str("Scholarships for "+eth+" "+gender+" "+grade+" "+loc+" interested in "+major)
	search=turnToSearch(text)
	more=getMoreSearch(search)
	res=[]
	for item in more:
		crawlSearch(str(item),res)
	new = deleteDuplicates(res)
	return res
"""
print getScore("https://hsf.net/","hispanic","high school students in","art","male","houston")
print getScore("http://scholarships.fastweb.com/y-high-school-seniors","hispanic","high school students in","art","male","houston")
print getScore("http://www.aisd.net/aisd/scholarships/Home/tabid/4724/Default.aspx","hispanic","high school students in","art","male","houston")
"""
def sort(my_list,eth,grade,major,gender,loc):
    size = len(my_list)
    for i in range(size):
        for j in range(size-i-1):
            if(getScore(my_list[j],eth,grade,major,gender,loc) < getScore(my_list[j+1],eth,grade,major,gender,loc)):
                tmp = my_list[j]
                my_list[j] = my_list[j+1]
                my_list[j+1] = tmp
                print "Sorting "+str(my_list[j])
    return my_list
"""arr=['https://hsf.net/','http://www.aisd.net/aisd/scholarships/Home/tabid/4724/Default.aspx','http://scholarships.fastweb.com/y-high-school-seniors']
b=sort(arr,"hispanic","high school students in","art","male","houston")
for item in b:
	print item

print getName("http://lamarwebtsa.org/")

print getScholar("Indian","high school students in","Houston","male","Computer Science")


arrA=getScholar("Indian","high school students in","Houston")
for item in arrA:
	print item
userIn=raw_input("Enter A Search: ")
searchQ(userIn)
url=turnToSearch(str(link))
b=getMoreSearch(url)
a=[]
for item in b:
	crawlSearch(item,a)
contactSearch(a)
print "Done"

a=[]
link=turnToSearch("Halo 5")
crawlSearch(link,a)

for item in a:
	print item
"""





