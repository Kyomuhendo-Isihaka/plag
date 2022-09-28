from unittest import result
from django.shortcuts import render, redirect
from textblob import Word
import re
import pyttsx3
import PyPDF2
from pathlib import Path
# import pywhatkit
from difflib import SequenceMatcher
import os
import mysql.connector

import cv2


con = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="plag"
)

mycursor = con.cursor()


def pdf_txt_db(source, mytxt):
    path2 = "D:/plag/"+source
    path1 = "D:/plag/"+mytxt+".txt"
    pdffileobj = open(path2, 'rb')
    pdfreader = PyPDF2.PdfFileReader(pdffileobj)
    x = pdfreader.numPages
    print(x)

    for i in range(-1, (x-1)):
        pageobj = pdfreader.getPage(i)
        text = pageobj.extractText()
        print(text)
        with open(path1, "a") as file:
            file.write(text)
            file.close()


def new_upload(filename, size):
    sql = "INSERT INTO file_uploads(filename,size)VALUES(%s,%s)"
    values = (filename, size)
    mycursor.execute(sql, values)
    con.commit()


def register(name,email,password,contact):
    sql= "INSERT INTO account(name,email,password,contact)VALUES(%s,%s,%s,%s)"
    values = (name, email, password, contact)

    mycursor.execute(sql,values)

    con.commit()
    return redirect('/')

# def userlogin(name, password):
#     username =""

#     sql = "SELECT * FROM users"
#     mycursor.execute(sql)
#     result = mycursor.fetchall()
#     for i in result:

#         if i[1]==name and i[3]==password:
#             username = i[1]
#             print("loggedin")
#             return redirect('/dasboard')
#         else:
#             print("login Failed")
#             return redirect('/')

#     return username


k = cv2.waitKey(1)

speaker = pyttsx3.init()
path_to_txt = "D:/Plagiarism/kushoo.txt"


def spellcheck(word):
    word = Word(word)

    result = word.correct()

    sentence = " put some senetence"
    words = sentence.split()

    words = [word.lower() for word in words]

    words = [re.sub()for word in words]

    # for word in words:

    pass


def speak(words):
    while True:
        if k == ord("q"):
            break

        else:
            voice = speaker.getProperty('voice')
            speaker.setProperty('voices', voice[1])
            speaker.say(words)
            speaker.runAndWait()
            speaker.endLoop()


def plagiarism_percentage(doc1, doc2):
    with open(doc1) as file1, open(doc2) as file2:
        file1data = file1.read()
        file2data = file2.read()
        similarity = SequenceMatcher(None, file1data, file2data).ratio()
        print(similarity*100)
        n = similarity*100
        return n


def audio_book(pdf_source, page_no):
    file = []
    book = open(pdf_source, 'rb')
    pdfReader = PyPDF2.PdfFileReader(book)
    pages = pdfReader.numPages
    print(pages)
    for num in range(0, 3):
        page = pdfReader.getPage(num)
        text = page.extractText()
        file.append(text)

        # speak(text)
        print(text)
    print(file)
    return file


def pdf_to_txt(doc1):
    pdffileobj = open(doc1, 'rb')
    pdfreader = PyPDF2.PdfFileReader(pdffileobj)
    x = pdfreader.numPages
    file = []
    for i in range(0, (x-1)):

        pageobj = pdfreader.getPage(i)
        text = pageobj.extractText()
        file.append(text)
        # print(file[i])
    # print(text)
        # file1 = open(path_to_txt, "w")
        # file1.write(text)
        # file1.close()
        # print(i)
    print(file)
    return file


def pdf_text(doc1, name):
    source = 'D:/plag/'+name+'.txt'
    pdffileobj = open(doc1, 'rb')
    pdfreader = PyPDF2.PdfFileReader(pdffileobj)
    x = pdfreader.numPages
    print(x)
    for i in range(0, (x-1)):

        pageobj = pdfreader.getPage(i)
        text = pageobj.extractText()
        with open(source, "w") as file:
            file.write(text)
            file.close()

        # print(text)
        # file1 = open(source, "w")
        # file1.write(text)
        # file1.close()


# # images to text
# def drawing_to_text():
#     pywhatkit.image_to_ascii_art('imageDirectory.pgn', 'imageDirectory.txt')
# source to the pdf file
pdf = "D:/Plagiarism/kushoo.pdf"

# function to convert pdf to txt file
# pdf_to_txt(pdf)


# this is a functionn to convert pdf to text and speaking it out
# audio_book(pdf,2)


path1 = "D:/Plagiarism/file1.txt"
path2 = "D:/Plagiarism/file2.txt"


# calculating the percentage of plagiarism
# plagiarism_percentage(path1,path2)
print("shaka plagiarism checker")
