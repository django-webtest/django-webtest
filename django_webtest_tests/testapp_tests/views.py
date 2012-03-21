from django import forms
from django.http import HttpResponseRedirect
from django.views.generic.simple import direct_to_template

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
    return direct_to_template(request, 'form.html', {'form': form})


class SearchForm(forms.Form):
    q = forms.CharField(required=False)
    
def search(request):
    form = SearchForm(request.GET)
    q = None
    if form.is_valid():
        q = form.cleaned_data['q']
    return direct_to_template(request, 'get_form.html', 
                              {'form': form, 'q': q})

def set_session(request):
    request.session['test'] = 'foo'
    return HttpResponseRedirect('/')
