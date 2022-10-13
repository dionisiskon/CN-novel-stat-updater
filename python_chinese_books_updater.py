"""

Books updater for 69shu


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
console.print("\n69shu books updater\n", style="bold blue")
parser = argparse.ArgumentParser(description="69shu books updater")
parser.add_argument('--update')
parser.add_argument('--chapter')
parser.add_argument('--check')
args, leftovers = parser.parse_known_args()

if args.update is not None:
	page = requests.get(args.update)
	if page.status_code == 200:
		doesExist = os.path.exists(r'\Users\{yourUserName}\{yourFolder}\69shunovels.json')
		if doesExist == False:
			if args.chapter is not None:
				dictionary = {args.update : args.chapter}
				console.print("Inserting new novel to your personal list")
				with open("69shunovels.json", "w") as jsonFile:
					json.dump(dictionary, jsonFile)
			else:
				dictionary = {args.update : "1"}
				console.print("Inserting new novel to your personal list. Not finding chapter selection...Inputting 1 as chapter")
				with open("69shunovels.json", 'w') as jsonFile:
					json.dump(dictionary, jsonFile)
		else:
			if args.chapter is not None:
				with open("69shunovels.json", 'r') as jsonFile:
					data = json.load(jsonFile)
				data[args.update] = args.chapter				
				with open("69shunovels.json", 'w') as jsonFile:
					json.dump(data, jsonFile)
			else:
				print("It already exists!")

else:
	if args.check is not None:
		with open("69shunovels.json", 'r') as jsonFile:
			data = json.load(jsonFile)
			for link in data:
				chapternum = int(data[link])
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
						console.print("There are {} chapters you haven't read yet. You can visit the website at {} to read them now!\n".format(len(d) - chapternum, url))
				sleep(2)