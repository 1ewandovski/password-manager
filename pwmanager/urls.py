"""pwmanager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/dev/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from django.conf.urls import url
#from django.conf.urls import *
from . import view,operateDB,search
 
urlpatterns = [
    path('hello/', view.hello),
    path('register/', search.register),
    path('login/',search.login),
    path('adddata/', search.adddata),
    path('adddatareturn/', search.adddata_return),
    path('updatedata/', search.updatedata),
    path('updatedatareturn/', search.updatedata_return),
    path('deletedata/', search.delete),
    path('deletedatareturn/', search.delete_return),
    path('searchall/',search.searchdata),
    path('searchweb/',search.searchwebdata),
    path('searchall2/',search.SearchData_v2),
    #url(r'^testget$',search.test_get),
    #url(r'^testpost$',search.test_post),
    #url(r'^register$',search.register),
    #url(r'^deletedata$',search.delete),
    #url(r'^adddata$',search.adddata),
]
