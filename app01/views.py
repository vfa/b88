from django.shortcuts import render
import random
from .sms import sendSMS
from django.conf import settings

# Create your views here.

def send_sms(request):


    phone = settings.SMS_PHONE
    scode = random.randrange(1000, 9999)
    template_param_list = [str(scode), ]

    temp = request.GET.get('temp')
    if not temp:
        context1 = {'scode': scode, 'template_id': settings.SMS_TEMPLATEID, 'temp': "没有找到temp"}
        return render(request, 'sms.html', context1)
    #res = sendSMS(phone, 664156, template_param_list)
    res = ''
    context1 = {'scode': scode, 'res': res, 'template_id': settings.SMS_TEMPLATEID,'temp':temp}
    return render(request, 'sms.html', context1)