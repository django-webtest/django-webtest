from django import forms
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect

class PasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput())

    def clean_password(self):
        if self.cleaned_data['password'] != 'foo':
            raise forms.ValidationError('Incorrect password.')
        return self.cleaned_data['password']

def check_password(request):
    form = PasswordForm(request.POST or None)
    if form.is_valid():
        return HttpResponseRedirect('/')
    return render(request, 'form.html', {'form': form})


class SearchForm(forms.Form):
    q = forms.CharField(required=False)

def search(request):
    form = SearchForm(request.GET)
    q = None
    if form.is_valid():
        q = form.cleaned_data['q']
    return render(request, 'get_form.html', {'form': form, 'q': q})

def set_session(request):
    request.session['test'] = 'foo'
    return HttpResponseRedirect('/')

def redirect_to_protected(request):
    return redirect('protected')

@login_required
def protected(request):
    return HttpResponse('ok: {0}'.format(request.user.username))

def remove_prefix_redirect(request, arg):
    return HttpResponseRedirect("/" + arg)

def cookie_test(request):
    cookie = request.COOKIES.get(str('test_cookie'), None)
    return HttpResponse('cookie: {0}'.format(cookie))
