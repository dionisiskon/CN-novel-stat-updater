"""

Books updater/Library for 69shuba,Comrademao and MTLNovel because I've overfilled my bookmarks!


"""

# Import Libraries
import requests
from bs4 import BeautifulSoup
import argparse
import json
import os
from rich.console import Console
from time import sleep
from googletrans import Translator
import sys

# Arguments and console/translator
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
parser.add_argument('--load_bookmark', help = 'Load the bookmark file extractred from a browser')
args, leftovers = parser.parse_known_args()

# Current path
dir_path = os.path.dirname(os.path.realpath(__file__))

# Check for OS
if os.name == 'nt':
	# For Windows
	path_of_file = '\cnnovels.json'
else:
	# For Mac and Unix
	path_of_file = '/cnnovels.json'

def detection(page, link):
	console.print('\nSearching for chapter information automatically...\n', style='bold green')
	if '69shuba' in link and 'txt' in link:
		soup = BeautifulSoup(page.content, 'html.parser')
		a = soup.find_all('h1')
		chapter = a[0].text
		b = translator.translate(chapter).text
		splitter = b.split(' ')
		index = splitter.index('Chapter') + 1
		chapter = splitter[index].replace('.', '').replace(':', '')
		console.print('\nChapter information found! Inserting {} as chapter...\n'.format(chapter), style='bold green')
		args.link = 'https://www.69shuba.com/book/' + link.split('/')[4] + '.htm'
		args.chapter = chapter
	elif 'comrademao' in link and 'chapter' in link:
		soup = BeautifulSoup(page.content, 'html.parser')
		a = soup.find_all('h3')[0].text
		b = translator.translate(a).text
		c = b.split(' ')
		chapter = c[-1].replace('.','').replace(':', '')
		chapter = chapter.replace('chapter','').replace('Chapter','')
		console.print('\nChapter information found! Inserting {} as chapter...\n'.format(chapter.replace('\n', '').replace(' ','')), style='bold green')
		args.link = 'https://comrademao.com/novel/' + link.split('/')[-3]
		args.chapter = chapter
	elif 'mtlnovel' in link and 'chapter' in link:
		splitter = link.split('-')
		res = list(filter(lambda x: 'chapter' in x, splitter))
		index = splitter.index(res[0]) + 1
		chapter = splitter[index]
		console.print('\nChapter information found! Inserting {} as chapter...\n'.format(chapter), style='bold green')
		args.chapter = chapter
		args.link = 'https://www.mtlnovel.com/' + link.split('/')[-3]
	else:
		console.print('No chapter information could be extracted. Setting chapter as 1 in the json file...\n', style='blue')
# Function to create a file
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

# Function to add to an existing file
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

if args.link:
	if '69shuba' in args.link:
		console.print("You have inputted a 69shuba link\n", style='bold green')
		page = requests.get(args.link)
		detection(page, args.link)
		if page.status_code == 200:
			doesExist = os.path.exists(dir_path + path_of_file)
			if doesExist == False:
				create('69shuba')
			else:
				update('69shuba')
	elif 'comrademao' in args.link:
		console.print("You have inputted a comrademao link\n", style='bold green')
		headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
		page = requests.get(args.link, headers=headers)
		detection(page, args.link)
		if page.status_code == 200:
			doesExist = os.path.exists(dir_path + path_of_file)
			if doesExist == False:
				create('ComradeMao')
			else:
				update('ComradeMao')
	elif 'mtlnovel' in args.link:
		console.print("You have inputted a MTLNovel link\n", style="bold green")
		doesExist = os.path.exists(dir_path + path_of_file)
		detection('', args.link)
		if doesExist == False:
			create('MTLNovel')
		else:
			update('MTLNovel')
	else:
		console.print("Incompatible link found!", style='bold red')
elif args.check:
	doesExist = os.path.exists(dir_path + path_of_file)
	if doesExist == False:
		console.print("You can't check when a file doesn't exist! Try again with a valid argument!\n", style='bold red')
		sys.exit()
	headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
	with open("cnnovels.json", 'r') as jsonFile:
		data = json.load(jsonFile)
	if '69shuba' in data:
		for link in data['69shuba']:
			chapternum = int(data['69shuba'][link])
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
elif args.delete:
	choiceCounter = 1
	console.print("Deleting process initiated...", style = 'bold red')
	doesExist = os.path.exists(dir_path + path_of_file)
	deleteList = []
	category = []
	if doesExist == True:
		with open('cnnovels.json', 'r') as jsonFile:
			data=json.load(jsonFile)
		console.print('You currently have these novels in your json file:\n')
		if '69shuba' in data:
			console.print('69shuba:', style = 'bold blue')
			for item in data['69shuba']:
				page = requests.get(item)
				soup = BeautifulSoup(page.content, 'html.parser')
				booknav2 = soup.find('div', class_ = 'booknav2')
				h1 = booknav2.find('h1').text
				title = translator.translate(h1).text
				console.print(str(choiceCounter) + ' : ' + title + ' ' + item)
				choiceCounter +=1
				deleteList.append(item)
				category.append('69shuba')
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
		console.print(str(choiceCounter) + ': ' + 'Delete all')
		choiceCounter += 1
		choice = int(input('Please select your choice\n'))
		if choice > choiceCounter - 1 or choice < 1:
			console.print("The choice number you selected is wrong. Try again!", style="bold red")
		else:
			if choice > len(deleteList):
				asd = input('\nAre you sure? type "y" or "yes" for deleting everything\n')
				if asd == 'y' or asd == 'yes':
					os.remove('cnnovels.json')
					console.print('The bookmarks were deleted successfully!', style='bold blue')
					sys.exit()
				else:
					console.print('Try again with a valid option!', style='bold red')
					sys.exit()
			data[category[choice - 1]].pop(deleteList[choice - 1])
			if len(data[category[choice - 1]]) == 0:
				data.pop(category[choice - 1])
			if len(data) == 0:
				os.remove('cnnovels.json')
			else:
				with open("cnnovels.json", "w") as jsonFile:
					json.dump(data, jsonFile, indent = 2)
				print("The process has been terminated successfully")
	else:
		console.print("\nFile doesn't exist!\n", style='bold red')
elif args.list:
	doesExist = os.path.exists(dir_path + path_of_file)
	if doesExist == False:
		console.print("Your novel collection list is empty!", style='bold red')
	else:
		with open('cnnovels.json', 'r') as jsonFile:
			data=json.load(jsonFile)
		console.print('You currently have these novels in your json file:\n')
		if '69shuba' in data:
			console.print('69shuba:', style = 'bold blue')
			for item in data['69shuba']:
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
elif args.load_bookmark:
	# Tested with android chrome bookmarks file
	valid_urls = []
	f = open(sys.argv[2])
	data = json.load(f)
	for i in data['roots']['synced']['children']:
		if '69shuba' in i['url'] or 'comrademao' in i['url'] or 'mtlnovel' in i['url']:
			valid_urls.append(i['url'])
	f.close()
	if len(valid_urls) > 0:
		unique_urls = []
		chapters = []
		sources = []
		for i in range(len(valid_urls) -1, -1, -1):
			url_split = valid_urls[i].split('/')
			if url_split[4] not in unique_urls:
				if '69shuba' in valid_urls[i]:
					unique_urls.append(url_split[4])
					chapters.append(url_split[5])
					sources.append('69shuba')
				elif 'comrademao' in valid_urls[i]:
					unique_urls.append(url_split[4])
					chapters.append(url_split[5])
					sources.append('ComradeMao')
				else:
					unique_urls.append(url_split[3])
					chapters.append(url_split[4])
					sources.append('MTLNovel')
	else:
		console.print('No valid links inside bookmark file!', style='bold red')
		sys.exit()
	counter = 0
	headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
	for i in range(len(unique_urls)):
		if '69shuba' in sources[i]:
			page = requests.get('https://www.69shuba.com/txt/' + unique_urls[i] + '/' + chapters[i])
			soup = BeautifulSoup(page.content, 'html.parser')
			a = soup.find_all('h1')
			chapter = a[0].text
			b = translator.translate(chapter).text
			splitter = b.split(' ')
			index = splitter.index('Chapter') + 1
			args.chapter = splitter[index].replace('.', '').replace(':', '')
			args.link = 'https://www.69shuba.com/book/' + unique_urls[i] + '.htm'
		elif 'ComradeMao' in sources[i]:
			page = requests.get('https://comrademao.com/mtl/' + unique_urls[i] + '/' + chapters[i], headers=headers)
			soup = BeautifulSoup(page.content, 'html.parser')
			a = soup.find_all('h3')[0].text
			b = translator.translate(a).text
			c = b.split(' ')
			chapter = c[-1].replace('.','').replace(':', '')
			args.chapter = chapter
			args.link = 'https://comrademao.com/novel/' + unique_urls[i]
		else:
			args.chapter = chapters[i].split('-')[1]
			args.link = 'https://www.mtlnovel.com/' + unique_urls[i]
		doesExist = os.path.exists(dir_path + path_of_file)
		if doesExist == False:
			create(sources[i])
		else:
			update(sources[i])
		counter +=1
		console.print('Added {} novel to collection list'.format(str(counter)), style = 'bold green')
else:
	console.print("No argument was inserted. Please try executing the script again in the proper format!\n", style = 'bold red')
