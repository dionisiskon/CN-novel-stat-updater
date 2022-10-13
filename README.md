# CN-novel-stat-updater

== It currently updates stats for 69shu.com and Comrademao ==

The python programs helps keeping stats of your favorite novels from a chinese website called 69shu.com. 

## Usage

## Arguments

## Required

--s : For selecting source (Add 1 for 69shu and 2 for comrademao)

example:
  python3 python_chinese_books_updater.py --check y --s 2

## Optional 

#### --check : Checking for updates 

example:
  python3 python_chinese_books_updater.py --check y --s 2
  
#### --update : Updating json file without chapter number

example:
  python3 python_chinese_books_updater.py --update https://www.69shu.com/txt/42794.htm  --s 1

This will update the json file with the novel with the last chapter read set as 1. 

#### --update : Updating json file with chapter number

Another example is updating using chapter number :

example:

  python3 python_chinese_books_updater.py --update https://www.69shu.com/txt/42794.htm --chapter 300 --s 1

### How to use

![change this command](images_for_book_updater/changethiscommand.png)

- Change the {yourUserName} with something like Paul or whatever your Username is.
- Change {yourFolder} with the folder containing the file. 

For example, if mine was at the Desktop and my username was Alex, then that would make the command r'\Users\Alex\Desktop\cnnovels.json'

## Screenshots

### Checking

![Checking screenshot](images_for_book_updater/Checking_example.png)
