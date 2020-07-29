# -*- coding: utf-8 -*-
"""
Created on Sat May 16 18:26:16 2020

@author: yaoyizhou
"""

from django.http import HttpResponse
 
def hello(request):
    return HttpResponse("Hello world ! ")