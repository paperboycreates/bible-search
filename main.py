#
#   Title:          Bible Search Tool
#   Authors:        Jacob Sheets
#   Description:    Searches entire bible for requested text
#   Date:           10/23/2020
#   version:        1.0
#
import sys
import string
import csv

def exit():
    sys.exit()

def openBible():
    bible = ""
    with open("bible.txt") as f:
        bible = f.readlines()
    return bible

# Book Format and Convert
def convertBook(b):
    bibleAbbrev = {}
    book = b

    with open("Bible_Abbreviations.csv", mode='r') as f:
        reader = csv.reader(f)
        bibleAbbrev = {rows[0]:rows[1] for rows in reader}

    if b in bibleAbbrev:
        book = bibleAbbrev.get(b)

    book = "THE BOOK OF " + book.upper()
    return book

# Chapter Format and Convert
def convertChapter(b, c):
    chapter = ""
    if (b == "THE BOOK OF PSALMS"):
        chapter = "PSALM " + c
    else:
        chapter = "CHAPTER " + c

    return chapter

# Bible Search
def bibleSearch(b, c, v):
    text = openBible()
    book = convertBook(b)
    chapter = convertChapter(book, c)

    foundBook = False
    foundChapter = False
    foundVerse = False

    for line in text: 
        # Break if found the next book or EOF
        if(foundBook and line[0:12] == "THE BOOK OF " or "" == line ):
            break
        
        # Skip if blank line
        if (line == '\n'):
            continue

        # Find Book
        if (book == line.strip('\n')):
            foundBook = True

        # Find Chapter
        if (chapter == line.strip('\n') and foundBook):
            foundChapter = True

        # Grab First "word"
        verse = line.split()
        verseNum = verse[0]

        # Find Verse
        if (verseNum == v and foundBook and foundChapter):
            foundVerse = True
            final = book[12:] + " " + c + ":" + line.strip('\n')
            prettyPrint(final)
            break

    #Errors
    if(foundBook == False):
        print("**Book not Found**")
        return
    if(foundChapter == False):
        print("**Chapter not Found**")
        return
    if(foundVerse == False):
        print ("**Verse not Found**")

    print ("(q) for exit")

# Print Formating
def prettyPrint(final):

    verses = open('verses.txt', 'a') 
    words = final.split()
    lines = []
    current = ''
    for word in words:
        if len(current) + 1 + len(word) > 80:
            lines.append(current)
            current = word
        else:
            current = current + " " + word
    lines.append(current)

    for line in lines:
        verses.write(line.lstrip() + '\n')
        print(line.lstrip())
    verses.close()
    

def main():

    search = True

    print("Bible Verse Search Tool")

    while search:
        bookName = str(input("Book: "))
        if (bookName == 'q'):
            exit()
        chapterNum = str(input("Chapter: "))
        verseNum = str(input("Verse: "))
        bibleSearch(bookName, chapterNum, verseNum)

if __name__ == '__main__':
    main()