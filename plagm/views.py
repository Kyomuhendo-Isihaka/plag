from distutils.command.upload import upload
from http.client import HTTPResponse
from posixpath import split
from turtle import ht
from urllib.parse import uses_relative
from urllib.request import HTTPCookieProcessor
from django.shortcuts import render, redirect
from plag import plag_detection as pld
from django.core.files.storage import FileSystemStorage
import pathlib
import os
import datetime
import requests
import mysql.connector
from difflib import SequenceMatcher
con = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "",
    database = "plag"
)

mycursor = con.cursor()




# Create your views here.


def register(request):
    error = ""
    if request.method=="POST":
        name= request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        contact = request.POST.get('contact')
        passwordConfirm = request.POST.get('passwordConfirm')

        if password==passwordConfirm:
            pld.register(name, email, password, contact)

            print("good to go")
        else:
            error= "password mismatch"
            print('error')
    

    return render(request,"Register.html", {'message':error})

def login(request):
    sms = ""
    username = ""
    # requests.set_cookie('userID', "helper")
    if request.method=="POST":
        email = request.POST.get('email')
        password = request.POST.get('password')     

        # # pld.userlogin(name,password )
        sql = "SELECT * FROM account"
        mycursor.execute(sql)
        result = mycursor.fetchall()

        for i in result:
        #     # print(i)        
            if i[2]== email and i[3]== password:
                username = str(i[1])
                print(username)
                print("loggedin")
               
                html = redirect('/dashboard/') 
                html.set_cookie("accountname",username,360000)  
                return html

                
            else:    
                print("failed")
                sms= "invalid email or password"
    return render(request,"login.html",{"sms":sms}) 
    
 

def checkplag(request):
    name = ""
    cook = request.COOKIES["accountname"]
    # if request.method == "POST":
    # name = request.POST.get("x")


    
    # username = ""       
    return render(request,"checkplag.html",{"name":cook})

def listen(request):
    text=""
    cook = request.COOKIES["accountname"]
    print(cook)
    if request.method == "POST":

        
        file= request.FILES["file"]
        # extention = pathlib.Path(file).suffix
        
        fs = FileSystemStorage()
        fs.save(file.name, file)
        path = "D:/plag/"+ str(file)
        split_tup =os.path.splitext(path)
        file_extention = split_tup[1]
        # if file_extention =='.pdf':
        # with open(path) as file:
            # text=file.read()
        # print(text) 
        # print("file ok")
        # text=pld.pdf_to_txt(path)
        text=pld.audio_book(path,2)
    
        pld.speak(text)
        # else:
            # print("invalid file") 
            # pld.speak('uploaded file is not a pdf')   

        print(file_extention)
        print(file)
    return render(request, "listen.html",{"text":text,"name":cook}) 

def checkpasslip(request):
    cook = request.COOKIES["accountname"]
    return render(request, "checkpasslip.html",{"name":cook})  

def dictionary(request):
    cook = request.COOKIES["accountname"]
    return render(request, "dictionary.html",{"name":cook})         

def results(request):
    n=""
    size =""
    
    if request.method == "POST":
        
        file= request.FILES["file"]
        # file1= request.POST.get("file")
        # print(file.name)
        # print(type(file))
        name = str(file.name)

        
        
        # filename = str(request.POST.get("file"))
        # extention = pathlib.Path(file).suffix
        # print(extention)
        fs = FileSystemStorage()
        fs.save(file.name,file)



        pld.pdf_txt_db(name,name)

        p1 = "D:/plag/t1.txt"
        p2 = "D:/plag/t.txt"
        print(p1)

        with open(p1) as file1, open(p1) as file2:
            file1data = file1.read()
            file2data = file2.read()
            similarity = SequenceMatcher(None, file1data, file2data).ratio()
            print(similarity*100)
            n = similarity*100
        
        # newfile =str(file)
        
        # pdf_uploads = 'D:/plag/'+str(file)
        # pld.pdf_text(pdf_uploads,file)

        size = file.size
        print(type(name))
        pld.new_upload(name,size)


    return render(request,"results.html",{"n":n,"size":size})    