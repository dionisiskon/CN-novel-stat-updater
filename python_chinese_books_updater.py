"""

Books updater/Library for 69shu,Comrademao and MTLNovel because I've overfilled my bookmarks!


"""

import requests
from bs4 import BeautifulSoup
import argparse
import json
import os
from rich.console import Console
from time import sleep
from googletrans import Translator

translator = Translator()
console = Console()
console.print("\nCN books stat updater\n", style="bold blue")
parser = argparse.ArgumentParser(description="CN books stat updater")
required = parser.add_argument_group('required arguments')
parser.add_argument('--link', help="Adding novel to library/Updating novel with chapter argument")
parser.add_argument('--chapter', help="Chapter number specification")
parser.add_argument('--check', help="Checking novel chapters progress")
parser.add_argument('--delete', help="Delete novel from database")
parser.add_argument('--list', help = 'List all novels that are currently inside the user\'s database')
args, leftovers = parser.parse_known_args()

dir_path = os.path.dirname(os.path.realpath(__file__))

def create(source):
	if args.chapter is not None:
		dict1 = {args.link : args.chapter}
		dictionary = {source : dict1}
		console.print("Inserting new novel to your personal list")
		with open("cnnovels.json", "w") as jsonFile:
			json.dump(dictionary, jsonFile, indent = 2)
	else:
		dict1 = {args.link : '1'}
		dictionary = {source : dict1}
		console.print("Inserting new novel to your personal list. Not finding chapter selection...Inputting 1 as chapter")
		with open("cnnovels.json", 'w') as jsonFile:
			json.dump(dictionary, jsonFile, indent = 2)
def update(source):
	if args.chapter is not None:
		with open("cnnovels.json", 'r') as jsonFile:
			data = json.load(jsonFile)
		if source in data:
			data[source][args.link] = args.chapter				
			with open("cnnovels.json", 'w') as jsonFile:
				json.dump(data, jsonFile, indent = 2)
		else:
			with open("cnnovels.json", 'r') as jsonFile:
				data = json.load(jsonFile)
			dict1 = {args.link : args.chapter}
			dictionary = {source : dict1}
			data.update(dictionary)
			console.print("Inserting new novel to your personal list")
			with open("cnnovels.json", "w") as jsonFile:
				json.dump(data, jsonFile, indent = 2)
	else:
		with open("cnnovels.json", 'r') as jsonFile:
			data = json.load(jsonFile)
		if source in data:
			data[source][args.link] = '1'			
			with open("cnnovels.json", 'w') as jsonFile:
				json.dump(data, jsonFile, indent = 2)
		else:
			with open("cnnovels.json", 'r') as jsonFile:
				data = json.load(jsonFile)
			dict1 = {args.link : '1'}
			dictionary = {source : dict1}
			data.update(dictionary)
			console.print("Inserting new novel to your personal list")
			with open("cnnovels.json", "w") as jsonFile:
				json.dump(data, jsonFile, indent = 2)
if args.link is not None:
	if '69shu' in args.link:
		console.print("You have inputted a 69shu link\n", style='bold red')
		page = requests.get(args.link)
		if page.status_code == 200:
			doesExist = os.path.exists(dir_path + '\cnnovels.json')
			if doesExist == False:
				create('69shu')
			else:
				update('69shu')
	elif 'comrademao' in args.link:
		console.print("You have inputted a comrademao link\n", style='bold red')
		headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
		page = requests.get(args.link, headers=headers)
		if page.status_code == 200:
			doesExist = os.path.exists(dir_path + '\cnnovels.json')
			if doesExist == False:
				create('ComradeMao')
			else:
				update('ComradeMao')
	else:
		console.print("You have inputted a MTLNovel link\n", style="bold red")
		doesExist = os.path.exists(dir_path + '\cnnovels.json')
		if doesExist == False:
			create('MTLNovel')
		else:
			update('MTLNovel')
elif args.check is not None:
	headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
	with open("cnnovels.json", 'r') as jsonFile:
		data = json.load(jsonFile)
	if '69shu' in data:
		for link in data['69shu']:
			chapternum = int(data['69shu'][link])
			url = link.replace("/txt",'').replace('.htm','/')
			page = requests.get(url)
			if page.status_code == 200:
				soup = BeautifulSoup(page.content, 'html.parser')
				a = soup.find('div', class_ = 'mybox')
				b = a.find_all("div")
				c = b[-1].find('ul')
				d = c.find_all('li')
				h3 = a.find('h3')
				div_h3 = h3.find('div', class_='bread')
				a_bread = div_h3.find_all('a')
				title = translator.translate(a_bread[2].text)
				title = title.text
				console.print(title, style='green')
				if len(d) == chapternum:
					console.print("You are on the latest chapter. Come back and check again for new updates!\n")
				else:
					console.print("Current chapter: {}\n".format(chapternum))
					console.print("There are {} chapters you haven't read yet. You can visit the website at {} to read them now!\n".format(len(d) - chapternum, link))
				sleep(2)
	if 'ComradeMao' in data:
		for link in data['ComradeMao']:
			chapternum = int(data['ComradeMao'][link])
			page = requests.get(link, headers=headers)
			if page.status_code == 200:
				soup = BeautifulSoup(page.content, 'html.parser')
				a = soup.find('div', class_ = 'eplister')
				b = a.find("ul")
				c = b.find_all('li')
				div = soup.find('div', class_ = 'infox')
				h1 = div.find('h1')
				title = h1.text
				console.print(title, style='green')
				if len(c) == chapternum:
					console.print("You are on the latest chapter. Come back and check again for new updates!\n")
				else:
					console.print("Current chapter: {}\n".format(chapternum))
					console.print("There are {} chapters you haven't read yet. You can visit the website at {} to read them now!\n".format(len(c) - chapternum, link))
			sleep(2)
	if 'MTLNovel' in data:
		from selenium import webdriver
		from webdriver_manager.chrome import ChromeDriverManager
		from selenium.webdriver.chrome.service import Service
		# MTTNovel Selenium
		options = webdriver.ChromeOptions()
		options.add_experimental_option('excludeSwitches', ['enable-logging'])
		options.add_argument('window-size=1920x1080')
		options.add_argument("--headless")
		options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 OPR/91.0.4516.72")
		for link in data['MTLNovel']:
			driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
			chapternum = int(data['MTLNovel'][link])
			if link.endswith('/'):
				url = link + 'chapter-list/'
			else:
				url = link + '/chapter-list/'
			page = driver.get(url)
			b = driver.find_elements("xpath", "//html/body/main/article/div/div[2]/div[3]/p/a")
			title = driver.find_element("xpath", "//html/body/main/article/div/div[2]/div[1]/h1").text
			console.print(title, style='green')
			if len(b) == chapternum:
				console.print("You are on the latest chapter. Come back and check again for new updates!\n")
			else:
				console.print("Current chapter: {}\n".format(chapternum))
				console.print("There are {} chapters you haven't read yet. You can visit the website at {} to read them now!\n".format(len(b) - chapternum, link))
			driver.quit()
if args.delete:
	choiceCounter = 1
	console.print("Deleting process initiated...", style = 'bold red')
	doesExist = os.path.exists(dir_path + '\cnnovels.json')
	deleteList = []
	category = []
	if doesExist == True:
		with open('cnnovels.json', 'r') as jsonFile:
			data=json.load(jsonFile)
		console.print('You currently have these novels in your json file:\n')
		if '69shu' in data:
			console.print('69shu:', style = 'bold blue')
			for item in data['69shu']:
				page = requests.get(item)
				soup = BeautifulSoup(page.content, 'html.parser')
				booknav2 = soup.find('div', class_ = 'booknav2')
				h1 = booknav2.find('h1').text
				title = translator.translate(h1).text
				console.print(str(choiceCounter) + ' : ' + title + ' ' + item)
				choiceCounter +=1
				deleteList.append(item)
				category.append('69shu')
			print('\n')
		if 'ComradeMao' in data:
			console.print('ComradeMao:', style = 'bold blue')
			for item in data['ComradeMao']:
				console.print(str(choiceCounter) + ': ' + ' '.join(elem.capitalize() for elem in item.split('novel/')[1].replace('/','').replace('-',' ').split()) + ' ' + item)
				choiceCounter +=1
				deleteList.append(item)
				category.append('ComradeMao')
			print('\n')
		if 'MTLNovel' in data:
			console.print('MTLNovel:', style = 'bold blue')
			for item in data['MTLNovel']:
				console.print(str(choiceCounter) + ': ' + ' '.join(elem.capitalize() for elem in item.split('/')[3].replace('-', ' ').split()) + ' ' + item)
				choiceCounter +=1
				deleteList.append(item)
				category.append('MTLNovel')
			print('\n')
		choice = int(input('Please select your choice\n'))
		if choice != choiceCounter - 1:
			console.print("The choice number you selected is wrong. Try again!", style="bold red")
		else:
			data[category[choiceCounter - 2]].pop(deleteList[choiceCounter - 2])
			if len(data[category[choiceCounter - 2]]) == 0:
				data.pop(category[choiceCounter - 2])
			if len(data) == 0:
				os.remove('cnnovels.json')
			else:
				with open("cnnovels.json", "w") as jsonFile:
					json.dump(data, jsonFile, indent = 2)
				print("The process has been terminated successfully")
if args.list:
	doesExist = os.path.exists(dir_path + '\cnnovels.json')
	if doesExist == False:
		console.print("Your novel collection list is empty!", style='bold red')
	else:
		with open('cnnovels.json', 'r') as jsonFile:
			data=json.load(jsonFile)
		console.print('You currently have these novels in your json file:\n')
		if '69shu' in data:
			console.print('69shu:', style = 'bold blue')
			for item in data['69shu']:
				page = requests.get(item)
				soup = BeautifulSoup(page.content, 'html.parser')
				a = soup.find('div', class_ = "booknav2")
				title = a.find('h1').text
				title = translator.translate(title).text
				console.print(' '.join(elem.capitalize() for elem in title.split()) + ' ' + item, style='bold green')
			print('\n')
		if 'ComradeMao' in data:
			console.print('ComradeMao:', style = 'bold blue')
			for item in data['ComradeMao']:
				console.print(' '.join(elem.capitalize() for elem in item.split('novel/')[1].replace('/','').replace('-',' ').split()) + ' ' + item, style='bold green')
			print('\n')
		if 'MTLNovel' in data:
			console.print('MTLNovel:', style = 'bold blue')
			for item in data['MTLNovel']:
				console.print(' '.join(elem.capitalize() for elem in item.split('/')[3].replace('-', ' ').split()) + ' ' + item, style='bold green')
			print('\n')
