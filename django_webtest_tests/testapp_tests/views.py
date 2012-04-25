from django import forms
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, redirect
from django.template.context import RequestContext

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
    ctx = RequestContext(request, {'form': form})
    return render_to_response('form.html', ctx)


class SearchForm(forms.Form):
    q = forms.CharField(required=False)

def search(request):
    form = SearchForm(request.GET)
    q = None
    if form.is_valid():
        q = form.cleaned_data['q']
    ctx = RequestContext(request, {'form': form, 'q': q})
    return render_to_response('get_form.html', ctx)

def set_session(request):
    request.session['test'] = 'foo'
    return HttpResponseRedirect('/')

def redirect_to_protected(request):
    return redirect('protected')

@login_required
def protected(request):
    return HttpResponse('ok')
