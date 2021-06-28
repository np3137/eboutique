from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth.hashers import check_password
from store.models.customer import Customer
from store.models.product import Product
from django.views import View
from django.contrib.auth.decorators import login_required
from django.contrib import auth


class Login(View):

    return_url = None

    def get(self, request):
        Login.return_url = request.GET.get('return_url')
        print(Login.return_url)
        return render(request, 'login.html')

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        customer = Customer.get_customer_by_email(email)
        error_message = None
        if customer:
            flag = check_password(password, customer.password)
            if flag:
                request.session['customer'] = customer.id
                request.session['email'] = email
                if Login.return_url:
                    return HttpResponseRedirect(Login.return_url)
                else:
                    Login.return_url = None
                    return redirect('homepage')
            else:
                error_message = 'Email or Password invalid !!'
        else:
            error_message = 'Email or Password invalid !!'
        print(email, password)
        return render(request, 'login.html', {'error': error_message})


def logout(request):
    try:
        for key in list(request.session.keys()):
            del request.session[key]
    except KeyError:
        pass
    return redirect('login')
