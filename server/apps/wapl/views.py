from django.shortcuts import render
from django.shortcuts import render, redirect
from django.http.request import HttpRequest
from . import forms
from . import models
from django.contrib import auth
import requests
from django.http import JsonResponse

def main(request:HttpRequest,*args, **kwargs):
    return render(request, "main.html")

def start(request:HttpRequest, *args, **kwargs):
    return render(request, "test_start.html")

def signup(request:HttpRequest, *args, **kwargs):
    if request.method == 'POST':
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('wapl:main')
        else:
            return redirect('wapl:signup')
    else:
        form = forms.SignupForm()
        context = {
            'form': form,
        }
        return render(request, template_name='signup.html', context=context)

def login(request:HttpRequest, *args, **kwargs):
    if request.method == 'POST':
        form = forms.LoginForm(data=request.POST)
        print(form.is_valid())
        if form.is_valid():
            user = form.get_user()
            auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('wapl:main')
        else:
            context = {
                'form': form,
            }
            return render(request, template_name='login.html', context=context)
    else:
        form = forms.LoginForm()
        context = {
            'form': form,
        }
        return render(request, template_name='login.html', context=context)

def logout(request:HttpRequest, *args, **kwargs):
    auth.logout(request)
    return redirect('wapl:start')

def kakao_login(request, *args, **kwargs):
    client_id = "9b8c21fe30f9bef16b12a8a512bf18a0"
    REDIRECT_URI = "http://localhost:8000/accounts/kakao/login/callback/"
    return redirect(
        f"https://kauth.kakao.com/oauth/authorize?client_id={client_id}&redirect_uri={REDIRECT_URI}&response_type=code"
    )

def kakao_callback(request):
    try:
        code = request.GET.get("code")
        client_id = "9b8c21fe30f9bef16b12a8a512bf18a0"
        redirect_uri = "http://localhost:8000/accounts/kakao/login/callback/"
        token_request = requests.get(
            f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={client_id}&redirect_uri={redirect_uri}&code={code}"
        )
        token_json = token_request.json()
        
        error = token_json.get("error",None)
        if error is not None :
            return JsonResponse({"message": "INVALID_CODE"}, status = 400)
        access_token = token_json.get("access_token")
        #------get kakaotalk profile info------#
        profile_request = requests.get(
            "https://kapi.kakao.com/v2/user/me", headers={"Authorization" : f"Bearer {access_token}"},
        )
        profile_json = profile_request.json()
        kakao_id = profile_json.get("id")
    except KeyError:
        return JsonResponse({"message" : "INVALID_TOKEN"}, status = 400)
    except access_token.DoesNotExist:
        return JsonResponse({"message" : "INVALID_TOKEN"}, status = 400)

    if models.User.objects.filter(kakao_id = kakao_id).exists():
        user = models.User.objects.get(kakao_id = kakao_id)
        login(request, user)
        return redirect('wapl:main')
    else:
        user = models.User(
            kakao_id = kakao_id,
        ).save()
        login(request, user)
        return redirect('wapl:main')