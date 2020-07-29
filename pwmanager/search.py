# -*- coding: utf-8 -*-
"""
Created on Sun May 17 11:43:00 2020

@author: yaoyizhou
"""
from django.http import HttpResponse,JsonResponse
from django.shortcuts import render
from pwmanager import operateDB
from django.forms import model_to_dict

global_id = 1   #data表的自增id

def test_get(request):
    return render('get.html')

def test_post(request):
    return render('post.html')

def register(request):    #用户注册,测试完毕
    if request.POST:
        if operateDB.Userlive(request.POST['email']): 
            #print('email exists')
            return JsonResponse({'code':300,'message':'账户已注册'})
        else :         
            operateDB.UserRegister(request.POST['email'],request.POST['password']) #向数据库中插入
            return JsonResponse({'code':200,'message':'账户创建成功'})
    else :
        return JsonResponse({'code':400,'message':'invalid post request'})
    
def login(request):     #用户登录,测试完毕
    if request.POST:
        if operateDB.Userlogin(request.POST['email'],request.POST['password']):
            return JsonResponse({'code':200,'message':'登录成功'})
        else :
            return JsonResponse({'code':300,'message':'登录失败'})
    else :
        return JsonResponse({'code':400,'message':'invalid post request'})

def delete(request):    #删除某条口令记录
    request.encoding='utf-8'
    if 'id' in request.GET and request.GET['id']:
        if operateDB.deleteData(request.GET['id']):
            return JsonResponse({'code':200,'message':'删除成功'})
        else :
            return JsonResponse({'code':300,'message':'该记录不存在'})
    else :
        return JsonResponse({'code':400,'message':'invalid get request'})

def delete_return(request):    #删除某域名下的口令记录,并返回该域名下剩余的所有记录
    request.encoding='utf-8'
    if 'id' in request.GET and request.GET['id'] and 'domain' in request.GET and request.GET['domain']and 'email' in request.GET and request.GET['email']:
        if operateDB.deleteData(id=request.GET['id']):
            templist=[]
            tempdic={'id':0,'domain':request.GET['domain'],'account':'','password':'',}
            data=operateDB.searchByDomain(domain=request.GET['domain'],email=request.GET['email'])
            for num in range(data.count()):
                tempdic['id']=data[num].id
                tempdic['password']=operateDB.decodeData(request.GET['email'],data[num].id)
                tempdic['account']=data[num].account_name
                templist.append(tempdic)                
            return JsonResponse(templist)
        else :
            return JsonResponse({'code':300,'message':'该记录不存在'})
    else :
        return JsonResponse({'code':400,'message':'invalid get request'})
    
def adddata_return(request):   #新增一条账户密码记录，好像需要写throw，返回该域名下所有的账户记录
    if request.POST:
        global global_id
        global_id = global_id + 1 #每一条记录的id          
        operateDB.addData(global_id,request.POST['domain'],request.POST['account'],request.POST['password'],request.POST['email']) 
        templist=[]
        tempdic={'id':0,'domain':request.POST['domain'],'account':'','password':'',}
        data=operateDB.searchByDomain(domain=request.POST['domain'],email=request.POST['email'])
        for num in range(data.count()):
            tempdic['id']=data[num].id
            tempdic['password']=operateDB.decodeData(request.POST['email'],data[num].id)
            tempdic['account']=data[num].account_name
            templist.append(tempdic)                
        return JsonResponse(templist)
    else :
        return JsonResponse({'code':400,'message':'invalid post request'})
    
def adddata(request):   #新增一条账户密码记录，好像需要写throw
    if request.POST:
        global global_id
        global_id = global_id + 1 #每一条记录的id          
        operateDB.addData(global_id,request.POST['domain'],request.POST['account'],request.POST['password'],request.POST['email'])                        
        return JsonResponse({'code':200,'message':'新增记录成功'})
    else :
        return JsonResponse({'code':400,'message':'invalid post request'})

def updatedata_return(request):   #修改一条记录的密码
    if request.POST:
        operateDB.updateData(request.POST['id'],request.POST['password'],request.POST['email'])
        templist=[]
        domain=operateDB.searchByID(request.POST['id']).domain_name
        tempdic={'id':0,'domain':domain,'account':'','password':'',}
        data=operateDB.searchByDomain(domain=domain,email=request.POST['email'])
        for num in range(data.count()):
            tempdic['id']=data[num].id
            tempdic['password']=operateDB.decodeData(request.POST['email'],data[num].id)
            tempdic['account']=data[num].account_name
            templist.append(tempdic)                
        return JsonResponse(templist)
    else :
        return JsonResponse({'code':400,'message':'invalid post request'})

def updatedata(request):   #修改一条记录的密码
    if request.POST:
        operateDB.updateData(request.POST['id'],request.POST['password'],request.POST['email'])
        return JsonResponse({'code':200,'message':'修改记录成功'})
    else :
        return JsonResponse({'code':400,'message':'invalid post request'})
    
def searchdata(request):   #搜索某个用户的所有记录
    request.encoding='utf-8'
    if 'email' in request.GET and request.GET['email']:
        data=operateDB.searchByEmail(request.GET['email'])
        templist=[]
        tempdic={'id':0,'domain':'','account':'','password':'',}
        for num in range(data.count()):
            tempdic['id']=data[num].id
            tempdic['password']=operateDB.decodeData(request.GET['email'],data[num].id)
            tempdic['account']=data[num].account_name
            tempdic['domain']=data[num].domain_name
            templist.append(tempdic)
        return JsonResponse(templist)
    else : 
        return JsonResponse({'code':400,'message':'invalid get request'})
    
def searchwebdata(request):  #搜索某个用户在某个域名的账户密码记录
    request.encoding='utf-8'
    if 'email' in request.GET and request.GET['email'] and 'domain' in request.GET and request.GET['domain']:
        templist=[]
        tempdic={'id':0,'domain':request.GET['domain'],'account':'','password':'',}
        data=operateDB.searchByDomain(domain_name=request.GET['domain'],email=request.GET['email'])
        for num in range(data.count()):
            tempdic['id']=data[num].id
            tempdic['password']=operateDB.decodeData(request.GET['email'],data[num].id)
            tempdic['account']=data[num].account_name
            templist.append(tempdic)                
        return JsonResponse(templist)
    else : 
        return JsonResponse({'code':400,'message':'invalid get request'})
    
def SearchData_v2(request):   #搜索某个用户的所有记录
    request.encoding='utf-8'
    if 'email' in request.GET and request.GET['email']:
        data=operateDB.searchByEmail(request.GET['email'])
        templist=[]
        tempdic={'id':0,'domain':'','account':'','password':'',}
        for num in range(data.count()):
            tempdic['id']=data[num].id
            tempdic['password']=operateDB.decodeData(request.GET['email'],data[num].id)
            tempdic['account']=data[num].account_name
            tempdic['domain']=data[num].domain_name
            templist.append(tempdic)
        return HttpResponse(templist)
    else : 
        return HttpResponse({'code':400,'message':'invalid get request'})

    