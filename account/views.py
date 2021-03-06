from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm, RegistrationForm, UserProfileForm, UserForm, UserProfileForm, UserInfoForm
from django.contrib.auth.decorators import login_required
from .models import UserProfile, UserInfo
from django.contrib.auth.models import User
from django.urls import reverse

from django.contrib.auth import views as auth_views


from django.shortcuts import render
from  .models import *
from django.http import HttpResponse

from django.conf import settings
from django.core.mail import send_mail



from django.views.generic import View

# Create your views here.
from random import Random
# 随机生成字符串
def random_str(randomlength=8):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars)-1
    random = Random()
    for i in range(randomlength):
        str += chars[random.randint(0, length)]
    return str   # 将拼接的字符串返回


def register(request):

    if request.method == "POST":
        user_form = RegistrationForm(request.POST)
        userprofile_form = UserProfileForm(request.POST)

        if user_form.is_valid()*userprofile_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()

            new_profile = userprofile_form.save(commit=False)
            new_profile.user = new_user
            code = random_str(16)  # 生成16位的随机字符串
            new_profile.code = code
            new_profile.save()
            username = user_form.cleaned_data['username']
            email = user_form.cleaned_data['email']

            sendEmail( email,code)
            return HttpResponse('请登录邮件激活')
            # return HttpResponseRedirect(reverse("account:user_login"))
        else:
            return render(request, "account/register.html", {"form": user_form, "profile": userprofile_form})
    else:
        user_form = RegistrationForm()
        userprofile_form = UserProfileForm()
        return render(request, "account/register.html", {"form": user_form, "profile":userprofile_form})



def sendEmail(email,code):
    email_title = "校园交流论坛账号验证"
    email_body = "请点击下面链接激活你的账号：http://127.0.0.1:8000/account/active/{0}".format(code)

    send_mail(email_title,email_body,settings.EMAIL_HOST_USER,[email])


class ActiveUserView(View):
    def get(self,request,active_code):
        users = UserProfile.objects.get(code=active_code)
        if users:
            users.is_active = True
            users.save()
        else:
            users.delete()
            return HttpResponse('Fail！Register Again!')
        return HttpResponseRedirect(reverse("account:user_login"))



def user_login(request):
    if request.method == "POST":
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            cd = login_form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user:
                login(request, user)
                return HttpResponse("欢迎您！您已成功登陆")
            else:
                return HttpResponse("您输入的用户名与密码不符")
        else:
            return HttpResponse("Invalid login")

    if request.method == "GET":
        login_form = LoginForm()
        return render(request, "account/login.html", {"form": login_form})



@login_required()
def myself(request):
    userprofile = UserProfile.objects.get(user=request.user) if hasattr(request.user, 'userprofile') else UserProfile.objects.create(user=request.user)
    userinfo = UserInfo.objects.get(user=request.user) if hasattr(request.user, 'userinfo') else UserInfo.objects.create(user=request.user)
    return render(request, "account/myself.html", {"user":request.user, "userinfo":userinfo, "userprofile":userprofile})

@login_required(login_url='/account/login/')
def myself_edit(request):
    userprofile = UserProfile.objects.get(user=request.user) if hasattr(request.user, 'userprofile') else UserProfile.objects.create(user=request.user)
    userinfo = UserInfo.objects.get(user=request.user) if hasattr(request.user, 'userinfo') else UserInfo.objects.create(user=request.user)
    if request.method == "POST":
        user_form = UserForm(request.POST)
        userprofile_form = UserProfileForm(request.POST)
        userinfo_form = UserInfoForm(request.POST)
        if user_form.is_valid() * userprofile_form.is_valid() * userinfo_form.is_valid():
            user_cd = user_form.cleaned_data
            userprofile_cd = userprofile_form.cleaned_data
            userinfo_cd = userinfo_form.cleaned_data
            request.user.email = user_cd['email']
            userprofile.StudentID = userprofile_cd['StudentID']
            userprofile.phone = userprofile_cd['phone']
            userinfo.school = userinfo_cd['school']
            userinfo.profession = userinfo_cd['profession']
            userinfo.address = userinfo_cd['address']
            userinfo.aboutme = userinfo_cd['aboutme']
            request.user.save()
            userprofile.save()
            userinfo.save()
        return HttpResponseRedirect('/account/my-information/')
    else:
        user_form = UserForm(instance=request.user)
        userprofile_form = UserProfileForm(initial={"StudentID":userprofile.StudentID, "phone":userprofile.phone})
        userinfo_form = UserInfoForm(initial={"school":userinfo.school, "profession":userinfo.profession, "address":userinfo.address, "aboutme":userinfo.aboutme})
        return render(request, "account/myself_edit.html", {"user_form":user_form, "userprofile_form":userprofile_form, "userinfo_form":userinfo_form})



from .models import UserInfo
@login_required(login_url='/account/login/')
def user_delete(request):
    user_id = request.session.get('_auth_user_id')
    print("user-id:"+user_id)
    user = User.objects.get(id=user_id)
    print("user:"+user.username+"\t"+user.email)
    if request.user == user:
        # auth_views.LogoutView.as_view(request)
        auth_views.LogoutView.as_view()
        user.delete()
        return HttpResponseRedirect(reverse("account:user_login"))
    else:
        return HttpResponse("您没有删除该用户的权限")