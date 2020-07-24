#!/usr/bin/env python
# -*- coding:utf-8 -*-
# by lanfc
from qcloudsms_py import SmsSingleSender
from qcloudsms_py.httpclient import HTTPError
from django.conf import settings


def sendSMS(phone_num, template_id, template_param_list):
    """
    单条发送短信
    :param phone_num: 手机号
    :param template_id: 腾讯云短信模板ID
    :param template_param_list: 短信模板所需参数列表，例如:【验证码：{1}，描述：{2}】，则传递参数 [888,666]按顺序去格式化模板
    :return:
    """
    appid = settings.SMS_APPID  # 自己应用ID
    appkey = settings.SMS_APPKEY  # 自己应用Key
    sms_sign = settings.SMS_APPSIGN  # 自己腾讯云创建签名时填写的签名内容（使用公众号的话这个值一般是公众号全称或简称）
    sender = SmsSingleSender(appid, appkey)

    try:
        response = sender.send_with_param(86, phone_num, template_id, template_param_list, sign=sms_sign)
    except HTTPError as e:
        response = {'result': 1000, 'errmsg': "网络异常发送失败。。。"}
    return response

# from django_redis import get_redis_connection
#
# def getredis(request):
#     r = get_redis_connection("default")
#     r.set('nickname', "老狼", ex=60)
#     try:
#         value = r.get('nicknamex').decode('utf-8')
#     except Exception as e :
#         value = e.__str__()
#     return render(request, 'redis.html', {'value': value})

