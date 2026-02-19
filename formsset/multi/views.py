from django.shortcuts import render
from django.forms import formset_factory
from .forms import ContactForm


# Create your views here.

def contact_view(request):
    formsett= formset_factory(ContactForm, extra=3)
    formset = formsett()
    return render(request, 'multi/contact.html', {'formset': formset})
