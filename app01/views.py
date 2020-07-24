from django.shortcuts import render
import random
from .sms import sendSMS
from django.conf import settings

# Create your views here.

def send_sms(request):
    phone = settings.SMS_PHONE
    scode = random.randrange(1000, 9999)
    template_param_list = [str(scode), ]
    temp = settings.SMS_TEMPLATEID

    temp = request.GET.get('temp')   #http://127.0.0.1:8000/app/send/sms?temp=1
    if not temp:
        context1 = {'scode': scode, 'template_id': settings.SMS_TEMPLATEID, 'temp': "没有找到temp"}
        return render(request, 'sms.html', context1)
    #res = sendSMS(phone, 664156, template_param_list)
    res = ''
    context1 = {'scode': scode, 'res': res, 'template_id': settings.SMS_TEMPLATEID,'temp':temp}
    return render(request, 'sms.html', context1)


from django import forms
from app01 import models
from django.core.validators import RegexValidator


class RegisterModelForm(forms.ModelForm):

    mphone = forms.CharField(label="手机号", validators=[RegexValidator(r'(1[3|4|5|6|7|8|9]\d{9})$', '手机号格式错误'), ])
    passwd = forms.CharField(label="密码", widget=forms.PasswordInput())
    cpasswd = forms.CharField(label="确认密码", widget=forms.PasswordInput())
    code = forms.CharField(label="验证码", widget=forms.TextInput())

    class Meta:
        model = models.userInfo
        fields = ['usernm', 'email', 'mphone', 'code', 'passwd', 'cpasswd', ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = '请输入{}'.format(field.label)


def register(request):
    form = RegisterModelForm()
    return render(request, 'register.html', {'form': form})


from django_redis import get_redis_connection

def getredis(request):
    r = get_redis_connection("default")
    r.set('13599927214','123 ', ex=60)
    try:
        values = r.get('13599927214').decode('utf-8')
    except Exception as e:
        values = e.__str__()
    return render(request, 'redis.html', {'value': values})
