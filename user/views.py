# -*- coding:utf-8 -*-
from io import BytesIO
from django.shortcuts import HttpResponse
from django.shortcuts import render,redirect
from utils.check_code import create_validate_code
from django import forms
from django.forms import fields
from django.forms import widgets
from user import models
import datetime
import re
import json
import time
from utils import pagination
class User(forms.Form):
    username = fields.CharField(error_messages={'required': '用户名不能为空'},
                                widget=widgets.Input(attrs={'type': "text", 'class': "form-control", 'name': "username",
                                                            'id': "username", 'placeholder': "请输入用户名"}))
    password = fields.CharField(error_messages={'required': '密码不能为空.'},
                                widget=widgets.Input(
                                    attrs={'type': "password", 'class': "form-control", 'name': "password",
                                           'id': "password",
                                           'placeholder': "请输入密码"})
                                )
class Newuser(forms.Form):
    username=fields.CharField(max_length=12,min_length=3,error_messages={'required':'用户名不能为空','max_length':'用户名长度不能12','min_length':'用户名长度不能小于3'},
                              widget=widgets.Input(attrs={'type':"text",'class':"form-control",'name':"username",'id':"username",'placeholder':"请输入用户名"}))
    email=fields.EmailField(error_messages={'required':'邮箱不能为空','invalid':'邮箱格式不正确.'}, widget=widgets.Input(attrs={'type':"email",'class':"form-control",'name':"email",'id':"email",'placeholder':"请输入邮箱名"}))
    password=fields.CharField(max_length=12, min_length=6,
                               error_messages={'required': '密码不能为空.', 'max_length': '密码长度不能大于12',
                                               'min_length': '密码长度不能小于6'},
                              widget=widgets.Input(
                                  attrs={'type': "password", 'class': "form-control", 'name': "password", 'id': "password",
                                         'placeholder': "请输入密码"})
                              )
    confirm_password=fields.CharField(max_length=12, min_length=6,
                               error_messages={'required': '不能为空.', 'max_length': '两次密码不一致',
                                               'min_length': '两次密码不一致'},
                                      widget=widgets.Input(
                                          attrs={'type': "password", 'class': "form-control", 'name': "confirm_password",
                                                 'id': "confirm_password",
                                                 'placeholder': "请重新输入密码"})
                                      )
def check_code(request):
    """
    验证码
    :param request:
    :return:
    """
    # stream = BytesIO()
    # img, code = create_validate_code()
    # img.save(stream, 'PNG')
    # request.session['CheckCode'] = code
    # return HttpResponse(stream.getvalue())

    # data = open('static/imgs/avatar/20130809170025.png','rb').read()
    # return HttpResponse(data)

    # 1. 创建一张图片 pip3 install Pillow
    # 2. 在图片中写入随机字符串
    # obj = object()
    # 3. 将图片写入到制定文件
    # 4. 打开制定目录文件，读取内容
    # 5. HttpResponse(data)

    stream = BytesIO()
    img, code = create_validate_code()
    # f=open('cc.png','wb')
    # img.save(f,'PNG')
    img.save(stream,'PNG')
    request.session['CheckCode'] = code
    return HttpResponse(stream.getvalue())
    # return HttpResponse(open('cc.png','rb').read())


def login(request):
    """
    登陆
    :param request:
    :return:
    """
    # if request.method == "POST":
    #     if request.session['CheckCode'].upper() == request.POST.get('check_code').upper():
    #         pass
    #     else:
    #         print('验证码错误')
    er=''
    s = ''
    if request.method=='GET':
        obj=User()
        return render(request,'login.html',{'obj':obj})
    if  request.method == 'POST':
        obj=User(request.POST)
        code = request.POST.get('check_code')
        auto=request.POST.get('auto')
        if auto:
            request.session.set_expiry(2419200)
        else:
            pass
        if code.upper() == request.session['CheckCode'].upper():
            u=request.POST.get('username')
            t1=models.User.objects.filter(username=u)
            if t1:
                pwd=request.POST.get('password')
                if pwd==t1[0].pwd:
                  request.session['user']=u
                  request.session['is_login']=True
                  request.session['pwd']=pwd
                  return redirect('/classroom/')
                else:
                  s='''
                  <script>alert('密码错误!!!请重新输入!!!');</script>
                  '''
            else:
                s = '''
           <script>alert('该用户名不存在!!!请检查是否正确!!!');</script>
                                '''

        else:
           er='验证码错误'
        return render(request, 'login.html',{'obj':obj,'er':er,'s':s})


def register(request):
    """
    注册
    :param request:
    :return:
    """
    er=''
    if request.method=='GET':
        obj=Newuser()
        return render(request, 'register.html',{'obj':obj,'er':er})
    if request.method == 'POST':
       try:
        obj=Newuser(request.POST)
        r=obj.is_valid()
        if r:
            code = request.POST.get('check_code')
            if code.upper() == request.session['CheckCode'].upper():
                user=request.POST.get('username')
                email=request.POST.get('email')
                u = models.User.objects.filter(username=user)
                if u:
                    s='''
                    <script>alert('用户名已经存在，请从新输入用户名！');
                </script>
                    '''
                else:
                    pwd1=request.POST.get('password')
                    pwd2=request.POST.get('confirm_password')
                    if pwd1!=pwd2:
                        s='''
                        <script>alert('两次密码不一致，请核对重新输入！');</script>'''
                    else:
                        models.User.objects.create(username=user,pwd=pwd1,email=email)
                        s='''
                        <script>alert('注册成功！');
                        </script>'''
                return render(request,'register.html',{'obj':obj,'er':er,'s':s})
            else:
                er='验证码错误'
                return render(request,'register.html',{'obj':obj,'er':er})

        else:
            s='''
            <script>alert('信息格式不正确,注册失败！');
                </script>'''
            return render(request,'register.html',{'obj':obj,'er':er,'s':s})
       except:
           s='''
           <script>alert('意外出错！！！！');</script>'''
           obj=Newuser()
           return render(request,'register.html',{'s':s,'obj':obj})
# def check(request):
#     f=request.session.get('is_login',False)
#     print(f)
#     if f:
#         u = request.session.get('user')
#         pwd = request.session.get('pwd')
#         users = models.User.objects.filter(username=u, pwd=pwd)
#         user = users[0].id
#         if request.method == 'POST':
#             sign_flag = request.POST.get('sign')
#             print('sign_flag', type(sign_flag), sign_flag)
#             print('12313')
#             if sign_flag == 'True':
#                 models.Attendence.objects.create(stu=user, start_time=datetime.datetime.now())
#                 print('12313')
#             elif sign_flag == 'False':
#                 cur_attendent = models.Attendence.objects.filter(stu=user, end_time=None)
#                 tmp_time = datetime.datetime.now()
#                 duration = round((tmp_time - cur_attendent.last().start_time).seconds / 3600, 1)
#                 cur_attendent.update(end_time=tmp_time, duration=duration)
#             return HttpResponse(request, '操作成功')
#         else:
#             # 查询上一个签到的状态
#             pre_att = models.Attendence.objects.filter(stu=user).order_by('id').last()
#             # print(pre_att.end_time)
#             if pre_att:
#                 # 如果当前时间距上次签到时间超过六小时，并且上次签退时间等于签到时间
#                 if (datetime.datetime.now() - pre_att.start_time.replace(
#                         tzinfo=None)).seconds / 3600 > 6 and pre_att.end_time == None:
#                     # Attendence.objects.filter(stu=user, end_time=None).update(end_time=pre_att.start_time+datetime.timedelta(hours=2),duration=2,detail="自动签退")
#                     pre_att.delete()
#                     sign_flag = True
#
#                 elif (datetime.datetime.now() - pre_att.start_time.replace(
#                         tzinfo=None)).seconds / 3600 < 6 and pre_att.end_time == None:
#                     sign_flag = False
#                 else:
#                     sign_flag = True
#             else:
#                 sign_flag = True
#             att_list = models.Attendence.objects.all().order_by('-id')
#
#             return render(request, 'check.html',{'user':users[0]})
#
#     return render(request, '/check/', {'error_msg': ''})
def classroom(request):
    f = request.session.get('is_login', False)
    user = request.session.get('user', None)
    if f:
      obj=models.Classroom.objects.all()
      return render(request,'classroom.html',{'obj':obj,'u':user})
    else:
          obj = User()
          return render(request, 'login.html', {'obj': obj})
def information(request):
    error=''
    f = request.session.get('is_login', False)
    if f:
        if request.method=='GET':
            user = request.session.get('user',None)
            obj = models.User.objects.filter(username=user)
        # elif request.method=='POST':
        #         id=request.POST.get('id')
        #         # p=request.POST.get('pwd')
        #         e=request.POST.get('email')
        #         phone=request.POST.get('phone')
        #         r=request.POST.get('realname')
        #         re_phone=re.compile('^1[3|5|7|8|]\d{9}$')
        #         re_email=re.compile('^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$')
        #         re_realname=re.compile('^[\u4e00-\u9fa5 ]{2,4}$')
        #         b=re_email.match(e)
        #         a=re_phone.match(phone)
        #         c=re_realname.match(r)
        #         if a and b and c:
        #           print(id)
        #           print(a,b,c)
        #           models.User.objects.filter(id=id).update(email=e,phone=phone,realname=r)
        #           error = '''
        #                                <script>alert('修改成功！！');</script>
        #                                '''
        #         else:
        #              error='''
        #              <script>alert('邮箱或电话或姓名格式不正确！！请重新填写！！');</script>
        #              '''
        #         obj=models.User.objects.filter(id=nid)
        return render(request,'information.html',{'obj':obj[0],'u':user})
    else:
        obj = User()
        return render(request,'login.html',{'obj':obj})
def viewroom(request,nid):
    f=request.session.get('is_login',False)
    user=request.session.get('user',None)
    if f:
      obj=models.Schedule.objects.filter(location_id=nid)
      obj2=models.meetingApply.objects.all()
      obj3=models.Allowed_time.objects.all()
      return render(request,'viewroom.html',{'nid':nid,'obj':obj,'obj2':obj2,'obj3':obj3,'u':user})
    else:
        obj=User()
        return render(request,'login.html',{'obj':obj})
def logout(request):
    request.session.clear()
    obj=User()
    return render(request,'login.html',{'obj':obj})
def basic_change(request):
    ret = {'status': True, 'error': None, 'data': None}
    print(request.method,request.POST)
    try:
        id = request.POST.get('id')
        # p=request.POST.get('pwd')
        e = request.POST.get('email')
        phone = request.POST.get('phone')
        r = request.POST.get('realname')
        re_phone = re.compile('^1[3|5|7|8|]\d{9}$')
        re_email = re.compile('^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$')
        re_realname = re.compile('^[\u4e00-\u9fa5 ]{2,4}$')
        b = re_email.match(e)
        a = re_phone.match(phone)
        c = re_realname.match(r)
        if a and b and c:
            print(id)
            print(a, b, c)
            models.User.objects.filter(id=id).update(email=e, phone=phone, realname=r)
            # obj = models.User.objects.filter(id=id)
            ret['error'] = '修改成功'
        else:
            ret['status']=False
            ret['error'] = '邮箱或电话或姓名格式不正确！！请重新填写！！！'
    except Exception as e:
        ret['status'] = False
        ret['error'] = '请求错误'
    print(json.dumps(ret))
    return HttpResponse(json.dumps(ret))
def password(request):
    f=request.session.get('is_login',None)
    user=request.session.get('user',None)
    if f:
        if request.method=='GET':
            change_obj=Newuser
            return render(request,'password.html',{'change_obj':change_obj})
        elif request.method=='POST':
            # change_obj=User(request.POST)
            ret={'status':True,'data':None,'error':None}
            obj = models.User.objects.filter(username=user).first()
            old=request.POST.get('old_pwd')
            new=request.POST.get('new_pwd')
            confirm_new=request.POST.get('confirm_pwd')
            if old and new and confirm_new:
                if old==obj.pwd:
                    if len(new)>=6 and len(new)<=12:
                        if new==confirm_new:
                            if old!=new:
                                ret['error']='修改成功'
                                obj.pwd=new
                                obj.save()
                            else:
                                ret['status']=False
                                ret['error']='新密码与原密码相同！！！'
                        else:
                            ret['error']=False
                            ret['error']='新密码两次不一致，请检查！！'
                    else:
                        ret['status'] = False
                        ret['error'] = '密码长度应大于六位，小于十二位！！！'
                else:
                    ret['status']=False
                    ret['error']='原密码错误，请再次输入！！'
            else:
                ret['status'] = False
                ret['error'] = '原密码，新密码，再次输入均不能为空！！'
            return HttpResponse(json.dumps(ret))

    else:
        obj=User()
        return render(request,'login.html',{'obj':obj})
def list(request,nid):
    user=request.session.get('user',None)
    if nid=='0':
        obj=models.meetingApply.objects.all().order_by('-applytime')
        count=obj.count()
        page_id=int(request.GET.get('p',1))
        c_obj = pagination.Page(page_id, count)
        obj=obj[c_obj.start:c_obj.end]
        a=c_obj.page_str('0')
    else:
        obj=models.meetingApply.objects.filter(homeID=nid).order_by('-applytime')
        count = obj.count()
        page_id = int(request.GET.get('p', 1))
        c_obj = pagination.Page(page_id, count)
        obj=obj[c_obj.start:c_obj.end]
        a = c_obj.page_str('1')
    return render(request,'list.html',{'obj':obj,'nid':nid,'a':a,'u':user})
def order(request):
    f = request.session.get('is_login', None)
    user = request.session.get('user', None)
    statu=True
    if f:
        if request.method=='GET':
            obj=models.Classroom.objects.all()
            obj2=models.Allowed_time.objects.all()
            obj3=models.User.objects.filter(username=user).first()
            return render(request,'order.html',{'obj':obj,'obj2':obj2,'obj3':obj3,'u':user})
        elif request.method=='POST':
            ret = {'status': True, 'data': None, 'error': None}
            location=request.POST.get('location')
            date=request.POST.get('date')
            # date = datetime.datetime.strptime(date, '%Y-%m-%d')
            begintime=request.POST.get('begintime')
            endtime=request.POST.get('endtime')
            people=request.POST.get('user_id')
            phone=request.POST.get('phone')
            total=request.POST.get('total')
            today = datetime.datetime.now().strftime('%Y-%m-%d')
            today_time=datetime.datetime.now().strftime('%H:%M:%S')
            topic=request.POST.get('topic')
            # print(location,date,begintime,endtime,people,phone,total,today,today_time,topic)
            if location and date and begintime and endtime and people and endtime and phone and total and topic:
                if date<today:
                    ret['status'] = False
                    ret['error'] = '只能预约今天及以后的时间！！'
                elif date==today:
                    if today_time>begintime:
                        ret['status'] = False
                        ret['error'] = '只能预约当前时间以后的时间！！'
                    if endtime <= begintime:
                        ret['status'] = False
                        ret['error'] = '预约时间结束时间应大于开始时间！！'
                    else:
                        obj = models.meetingApply.objects.filter(day=date, homeID_id=location)
                        for row in obj:
                            print(row.beginTime, row.endTime)
                            # print(type(begintime))
                            # print(type(row.beginTime.strftime('%H:%M:%S')))
                            # print(type(today))
                            if begintime > row.beginTime.strftime('%H:%M:%S') and begintime < row.endTime.strftime(
                                    '%H:%M:%S'):
                                ret['status'] = False
                                ret['error'] = '预约时间与别人预约的冲突！！'
                                statu = False
                            if endtime > row.beginTime.strftime('%H:%M:%S') and endtime < row.endTime.strftime(
                                    '%H:%M:%S'):
                                ret['status'] = False
                                ret['error'] = '预约时间与别人预约的冲突！！'
                                statu = False
                        if (statu):
                            data = {
                                'day': date,
                                'beginTime': begintime,
                                'endTime': endtime,
                                'applytime': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                'homeID_id': location,
                                'statusID_id': 1,
                                'workerID_id': people,
                                'attendance': total,
                                'topic': topic,

                            }
                            print(data)
                            models.meetingApply.objects.create(**data)
                            ret['error'] = '预约成功！！！'
                else:
                        if endtime <= begintime:
                            ret['status'] = False
                            ret['error'] = '预约时间结束时间应大于开始时间！！'
                        else:
                             obj=models.meetingApply.objects.filter(day=date,homeID_id=location)
                             for row in obj:
                                 print(row.beginTime,row.endTime)
                                 # print(type(begintime))
                                 # print(type(row.beginTime.strftime('%H:%M:%S')))
                                 # print(type(today))
                                 if begintime>row.beginTime.strftime('%H:%M:%S') and begintime<row.endTime.strftime('%H:%M:%S'):
                                     ret['status'] = False
                                     ret['error'] = '预约时间与别人预约的冲突！！'
                                     statu=False
                                 if endtime >row.beginTime.strftime('%H:%M:%S') and endtime < row.endTime.strftime('%H:%M:%S'):
                                     ret['status'] = False
                                     ret['error'] = '预约时间与别人预约的冲突！！'
                                     statu=False
                             if (statu):
                                 data={
                                     'day':date,
                                     'beginTime':begintime,
                                     'endTime':endtime,
                                     'applytime':datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                     'homeID_id':location,
                                     'statusID_id':1,
                                     'workerID_id':people,
                                     'attendance':total,
                                     'topic':topic,

                                 }
                                 print(data)
                                 models.meetingApply.objects.create(**data)
                                 ret['error']='预约成功！！！'
            else:
                ret['status'] = False
                ret['error'] = '预约信息请填全！！'
            return HttpResponse(json.dumps(ret))
    else:
        obj = User()
        return render(request, 'login.html', {'obj': obj})