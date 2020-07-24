#!/usr/bin/env python
# -*- coding:utf-8 -*-
# by lanfc
'''
用户账户相关的功能：注册、短信、登录、注销
'''
from django.shortcuts import render
from web.forms.account import RegisterModelForm, CheckSMSForm,smsRegisterModelForm
from django.http import JsonResponse

def register(request):
    """注册"""
    if request.method == 'GET':
        form = RegisterModelForm()
        return render(request, 'web/register.html', {'form': form})

    form = RegisterModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return JsonResponse({'status': True, 'data': '/login/'})
    else:
        print("test:::form-->", form)
        return JsonResponse({'status': False, 'error': form.errors})

def smsregister(request):
    """注册"""
    if request.method == 'GET':
        form = smsRegisterModelForm()
        return render(request, 'web/sms_login.html', {'form': form})

    form = RegisterModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return JsonResponse({'status': True, 'data': '/login/'})
    else:
        return JsonResponse({'status': False, 'error': form.errors})

def send_sms(request):
    """ 发送短信 """
    #phone = request.GET.get("mphone") #测试render用
    form = CheckSMSForm(request, data=request.GET)

    if form.is_valid():
        return JsonResponse({'status': True})
    else:
        return JsonResponse({'status': False, 'error': form.errors})

