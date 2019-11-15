from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, UserInfo
import re

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)



def email_check(email):
    pattern = re.compile(r"\"?([-a-zA-Z0-9.`?{}]+@\w+\.\w+)\"?")
    return re.match(pattern, email)

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm Pssword", widget=forms.PasswordInput)


    class Meta:
        model = User
        fields = ("username", "email")

    def clean_username(self):
        username = self.cleaned_data.get('username')

        if len(username) < 2:
            raise forms.ValidationError(u"用户名至少2位")
        elif len(username) > 50:
            raise forms.ValidationError(u"您的用户名太长")
        else:
            filter_result = User.objects.filter(username__exact=username)
            if len(filter_result) > 0:
                raise forms.ValidationError(u"用户名已存在")

        return username


    def clean_email(self):
        email = self.cleaned_data.get('email')

        if email_check(email):
            filter_result = User.objects.filter(email__exact=email)
            if len(filter_result) > 0:
                raise forms.ValidationError(u"邮箱已存在")
        else:
            raise forms.ValidationError(u"请输入有效邮箱")

        return email



    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 6:
            raise forms.ValidationError(u"密码至少6位")
        elif len(password) > 20:
            raise forms.ValidationError(u"密码至多20位")
        return password


    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')

        if password and password2 and password != password2:
            raise forms.ValidationError(u"两次密码不一致，请再次输入")
        return password2


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ("phone", "StudentID","is_active","code")

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')

        if len(phone) < 11:
            raise forms.ValidationError(u"手机号码至少11位")
        elif len(phone) > 20:
            raise forms.ValidationError(u"手机号码输入错误")
        else:
            filter_result = UserProfile.objects.filter(phone__exact=phone)
            if len(filter_result) > 0:
                raise forms.ValidationError(u"手机号码已存在")

        return phone

    def clean_StudentID(self):
        StudentID = self.cleaned_data.get('StudentID')

        if len(StudentID) < 9:
            raise forms.ValidationError(u"学号至少需要9位")
        elif len(StudentID) > 20:
            raise forms.ValidationError(u"学号格式错误")
        else:
            filter_result = UserProfile.objects.filter(StudentID__exact=StudentID)
            if len(filter_result) > 0:
                raise forms.ValidationError(u"学号已存在")

        return StudentID


class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserInfo
        fields = ("school", "profession", "address", "aboutme", 'photo')


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("email",)