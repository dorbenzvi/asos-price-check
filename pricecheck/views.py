import threading
from django.shortcuts import render
from pricecheck.models import Alert
from . import forms
import json,urllib
from django.http import HttpResponseRedirect,HttpResponse
import re
from pricecheck.forms import registerForm, UserForm
from django.views.generic.edit import DeleteView
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from time import sleep
from pricecheck.sendMail import sendEmail

def activate():
    t = threading.Thread(name='scraper', target=checkPriceDrop)
    t.daemon = True
    t.start()


def home(request):
    all_alerts_list = Alert.objects.all()
    alert_list = Alert.objects.all()
    date_dict = {'alerts': alert_list}
    form = forms.createAlert()
    if request.method == 'POST':
        form = forms.createAlert(request.POST)
        if form.is_valid():
            if check_Url(form.cleaned_data['product_url']):
                price = getProductprice(form.cleaned_data['product_url'])
                p = Alert(None, form.cleaned_data['product_name'], form.cleaned_data['product_url'], price,request.user.email)
                p.save()
            else:
                return render(request, 'pricecheck/home.html', context={'error':"Url Error",'form': form, 'alerts': all_alerts_list})
    return render(request, 'pricecheck/home.html', context={'form': form, 'alerts': all_alerts_list})


def about(request):
    return render(request, 'pricecheck/about.html')



def users(request):
    form1 = registerForm()
    if request.method == "POST":
        form1 = registerForm(request.POST)
        if form1.is_valid():
            form1.save(commit=True)
            return home(request)
        else:
            print("Error form invalid")

    return render(request, 'pricecheck/users.html', context={'form': form1})


#Get price of product from asos.com
def getProductprice(product_url):
    productId = getProductid(product_url)
    newProducturl = "https://www.asos.com/api/product/catalogue/v3/stockprice?productIds="+productId+"&store=ROW&currency=USD&keyStoreDataversion=ekbycqu-23"
    response = urllib.request.urlopen(newProducturl)
    data = json.loads(response.read())
    return float(data[0]['productPrice']['current']['value'])


def getProductid(product_url):
    productId = re.findall("/\d{7,9}",product_url)
    productId=productId[0][1:]
    return productId

class AlertDeleteView(DeleteView):
    model = Alert
    template_name = 'pricecheck/delete.html'
    context_object_name = 'alert'
    success_url = 'http://127.0.0.1:8000/pricecheck'


def check_Url(url):
    return re.match("https://www.asos.com/\S+", url)


def register(request):
    registered = False

    if request.method == "POST":
        user_form = UserForm(data=request.POST)

        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            registered = True
        else:
            print(user_form.errors)
    else:
        user_form = UserForm()

    return render(request, 'pricecheck/register.html', {'user_form':user_form, 'registered': registered})

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('Price-Home'))


def user_login(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('Price-Home'))
            else:
                return HttpResponse("Account not active")
        else:
            print("Someone tried to login and failed!")
            print("Username: {} and password :{}".format((username,password)))
            return HttpResponse("invalid login details!")
    else:
        return render(request,'pricecheck/login.html')


def checkPriceDrop():
    while True:
        sleep(3600)
        alert_list = Alert.objects.all()
        for alert in alert_list:
            if alert.product_price > getProductprice(alert.product_url):
                alert1 = Alert.objects.get(id=alert.id)
                alert1.product_price = getProductprice(alert.product_url)
                sendEmail(alert, alert1.product_price)
                alert1.save()





