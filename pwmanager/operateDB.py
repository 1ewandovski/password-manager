# -*- coding: utf-8 -*-
"""
Created on Sat May 16 19:22:18 2020

@author: yaoyizhou
"""

from django.http import HttpResponse
#from externtool.pwgenerator import hdremember_pw
from PassModel.models import Data,Users
from hashlib import sha256,md5
from uuid import uuid4
from pwmanager.encryption import Encryption

# 定义数据库原子操作
#def UserRegister(email,password):  #用户注册
#    salt = str(uuid4()).replace('-','')
#    email = email
    #print(salt)
#    hash_pwd = sha256((str(email)+ salt+str(password)).encode('utf8')).hexdigest()
    #hash_pwd = md5((str(email)+ salt+str(password)).encode('utf8')).hexdigest() 
    #print(hash_pwd)
#    user = Users(email=email,salt= salt,main_password=hash_pwd)    #salt32位 hash64位
#    user.save()
#    return 

#def addData(id,domain,account,password,email):       #新增一条账号密码记录
#    user = Users.objects.get(email=email)
#    enc = Encryption(user.main_password.encode())  #main_password是个string，要转成bytes
#    salt = enc.gen_salt()
#    pwd_save = enc.encrypt(password.encode())
#    data = Data(id=id,domain_name=domain,salt=salt,account_name=account,password=pwd_save,email=user) #外键要通过user输入而不是user.email
#    data.save()
#    return

# get the password for the website login 处理一条账户密码记录
#def decodeData(email,id):  
#    user = Users.objects.get(email=email)
#    data = Data.objects.get(id=id)
#    enc = Encryption(user.main_password.encode(),data.salt.encode())
#    pwd = enc.decrypt(data.password.encode()).decode('utf-8')
#    return pwd

#def updateData(id,password,email):    #更新一条账号密码记录
#    data = Data.objects.get(id=id)
#    user = Users.objects.get(email=email)
#    enc = Encryption(user.main_password.encode())
#    salt = enc.gen_salt()
#    new_pwd_save = enc.encrypt(password.encode())
#    data.password = new_pwd_save
#    data.salt = salt
#    data.save()
#    return 

# 定义数据库原子操作
def UserRegister(email,password):  #用户注册


    salt = str(uuid4())
    email = str(email)
    password = str(password)
    hash_pwd = sha256((email+ salt + password).encode()).hexdigest() 
    user = Users(email=email,salt= salt,main_password=hash_pwd)
    user.save()
    return 

def addData(id,domain,account,password,email):       #新增一条账号密码记录
    #pwd=hdremember_pw(min_length=15,max_length=25,no_special_characters=True)
    #user_email=Users.objects.get(email='1848702839@qq.com')
    user = Users.objects.get(email=email)
    enc = Encryption(user.main_password.encode())
    salt = enc.gen_salt().decode('utf-8')
    pwd_save = enc.encrypt(password.encode()).decode('utf-8')
    data = Data(id=id,domain_name=domain,salt=salt,account_name=account,password=pwd_save,email=user)
    data.save()
    return

# get the password for the website login
def decodeData(email,id):
    user = Users.objects.get(email=email)
    data = Data.objects.get(id=id)
    enc = Encryption(user.main_password.encode())
    enc.set_salt(data.salt.encode())
    pwd = enc.decrypt(data.password.encode()).decode('utf-8')
    return pwd

def updateData(id,password,email):    #更新一条账号密码记录
    data = Data.objects.get(id=id)
    user = Users.objects.get(email=email)
    enc = Encryption(user.main_password.encode())
    salt = enc.gen_salt().decode('utf-8')
    new_pwd_save = enc.encrypt(password.encode()).decode('utf-8')
    data.password = new_pwd_save
    data.salt = salt
    data.save()
    return 

def Userlogin(email,password):     #用户登录
    #user = Users.objects.filter(email=email,password=password)
    user = Users.objects.get(email=email)
    if user.main_password == sha256((str(email)+user.salt+str(password)).encode('utf8')).hexdigest():  #有个小问题，已改
        return user
    else :
        return None

def Userlive(useremail):     #查看用户账号是否已注册
    user = Users.objects.filter(email=useremail)
    if user :
        return True
    else :
        return False

def searchByDomain(domain,email):
    data = Data.objects.filter(domain_name=domain,email=email)
    if data :
        return data
    else :
        return None

def deleteData(id):    #删除一条账号密码记录
    if Data.objects.filter(id=id).delete():     #filter相当于where
        return True
    else :
        return False
    
def searchByEmail(email):    #搜索某个用户全部的账号密码记录
    data = Data.objects.filter(email=email)
    if data :
        return data
    else :
        return None

def searchByID(id):   #搜索某个id的账号密码记录
    data = Data.objects.get(id=id)
    if data :
        return data
    else :
        return None

