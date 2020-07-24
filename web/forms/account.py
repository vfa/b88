#!/usr/bin/env python
# -*- coding:utf-8 -*-
# by lanfc
from django import forms
from web import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.conf import settings
import random
from web.views.sms import sendSMS
from web.views.encrpt import md5
from django_redis import get_redis_connection


class BootstrapForm():
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = '请输入{}'.format(field.label)

class RegisterModelForm(BootstrapForm, forms.ModelForm):

    mphone = forms.CharField(label='手机号', validators=[RegexValidator(r'^(1[3|4|5|6|7|8|9])\d{9}$', '手机号格式错误'), ])
    passwd = forms.CharField(label="密码",
                             min_length=8,
                             max_length=64,
                             widget=forms.PasswordInput(),
                             error_messages={'min_length': "密码长度不能小于8个字符",
                                             'max_length': "密码长度不能超过64个字符"})
    cpasswd = forms.CharField(label="确认密码", widget=forms.PasswordInput())
    code = forms.CharField(label="验证码", widget=forms.TextInput())

    class Meta:
        model = models.userInfo
        fields = ['usernm', 'email', 'mphone', 'code', 'passwd', 'cpasswd', ]

    def clean_usernm(self):
        """用户名校验的钩子"""
        usernm = self.cleaned_data['usernm']
        exists = models.userInfo.objects.filter(usernm=usernm).exists()
        if exists:
            raise ValidationError('用户名已存在')
        return usernm

    def clean_email(self):
        """邮箱校验的钩子"""
        email = self.cleaned_data['email']
        exists = models.userInfo.objects.filter(email=email).exists()
        if exists:
            raise ValidationError('邮箱已存在')
        return email

    def clean_mphone(self):
        """手机号校验的钩子"""
        mphone = self.cleaned_data.get('mphone')
        if len(mphone)<1:
            raise ValidationError('手机号不能为空')
        exists = models.userInfo.objects.filter(mphone=mphone).exists()
        if exists:
            raise ValidationError('手机号已存在')
        return mphone

    def clean_passwd(self):
        passwd = self.cleaned_data.get('passwd')
        if len(passwd)<8:
            raise ValidationError('密码必须大于8位')
        passwd = md5(passwd)
        return passwd

    def clean_cpasswd(self):
        """密码校验的钩子"""
        passwd = self.cleaned_data.get('passwd')
        cpasswd = self.cleaned_data['cpasswd']
        
        if passwd != md5(cpasswd):
            raise ValidationError('密码不一致')
        return cpasswd

    def clean_code(self):
        """邮箱校验的钩子"""
        code = self.cleaned_data['code']
        mphone = self.cleaned_data.get('mphone')
        if not mphone or len(mphone)<1:
            raise ValidationError('验证码校验失败')

        r = get_redis_connection()
        scode = r.get(mphone)

        if not scode:
            raise ValidationError('手机号错误或者验证码已失效...')

        if code.strip() != scode.decode('utf-8'):
            raise ValidationError('验证码校验失败')
        return code


class smsRegisterModelForm(BootstrapForm, forms.ModelForm):
    mphone = forms.CharField(label='手机号', validators=[RegexValidator(r'^(1[3|4|5|6|7|8|9])\d{9}$', '手机号格式错误'), ])

    code = forms.CharField(label="验证码", widget=forms.TextInput())

    class Meta:
        model = models.userInfo
        fields = ['mphone', 'code',]


    def clean_mphone(self):
        """手机号校验的钩子"""
        mphone = self.cleaned_data.get('mphone')
        if len(mphone) < 1:
            raise ValidationError('手机号不能为空')
        exists = models.userInfo.objects.filter(mphone=mphone).exists()
        if exists:
            raise ValidationError('手机号已存在')
        return mphone

    def clean_code(self):
        """邮箱校验的钩子"""
        code = self.cleaned_data['code']
        mphone = self.cleaned_data.get('mphone')
        if not mphone or len(mphone) < 1:
            raise ValidationError('验证码校验失败')

        r = get_redis_connection()
        scode = r.get(mphone)

        if not scode:
            raise ValidationError('手机号错误或者验证码已失效...')

        if code.strip() != scode.decode('utf-8'):
            raise ValidationError('验证码校验失败')
        return code

class CheckSMSForm(forms.Form):

    mphone = forms.CharField(label='手机号', validators=[RegexValidator(r'^(1[3|4|5|6|7|8|9])\d{9}$', '手机号格式错误'), ])

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

    def clean_mphone(self):
        """手机号校验的钩子"""
        mphone = self.cleaned_data['mphone']

        # 校验短信模板的ID号。
        templateid = self.request.GET.get('tplid')
        #print(type(templateid), '----', type(settings.SMS_TEMPLATEID))  #js过来的为string类型。
        if templateid != str(settings.SMS_TEMPLATEID):
            raise ValidationError('短信模板错误..')

        # 校验数据库是否已经有手机号
        exists = models.userInfo.objects.filter(mphone=mphone).exists()
        if exists:
            raise ValidationError('手机号已存在')

        # 校验成功则发短信
        scode = random.randrange(1000, 9999)
        #res = sendSMS(mphone, templateid, [scode, ])
        res = {'result':0}
        if res['result'] !=0:
            raise ValidationError("短信发送失败{}".format(res['errmsg']))

        # 将短信验证码写入REDIS
        r = get_redis_connection("default")
        r.set(mphone, scode, ex=60)

        return mphone

