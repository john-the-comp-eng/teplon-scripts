from constants import *
from mysqlConnection import mySqlConnection

files = 25
articlesFound = {}
for fileNumber in range(1, files):

    with open(f"./tgChats/messages{fileNumber}.html", "r") as file:
            content = file.read()
            words = content.split(' ')

            for prothermArticle in VAILLANT_PARTS_ARTICLES:
                if prothermArticle not in articlesFound.keys():
                    articlesFound[prothermArticle] = 0
                for word in words:
                    if word == prothermArticle:
                        articlesFound[prothermArticle] += 1

print(articlesFound)
dbObj = mySqlConnection()
for article in articlesFound.keys():
     dbObj.updateEntity("product", "article", {"article": article, "tgChatMentions": articlesFound[article]}, True, True)
