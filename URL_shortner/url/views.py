import string
import random
from django.shortcuts import render, redirect
from .models import Urldata
from .forms import UrlForm



# Create your views here.
def shorten_url(request):
    if request.method == 'POST':
        form = UrlForm(request.POST)
        if form.is_valid():
            slug = ''.join(random.choice(string.ascii_letters ) for _ in range(10))


            url = form.cleaned_data['url']
            new_url = Urldata(url=url,slug=slug)
            new_url.save()
            # short_url = generate_short_url()
            # Urldata.objects.create(url=url, short_url=short_url)
            return redirect('/')#(request, 'shorten_url.html', {'form': form, 'short_url': short_url})
    else:
        form = UrlForm()
    data= Urldata.objects.all()
    context = {
        'form': form,
        'data': data
    }
    return render(request, 'index.html', {'form': form})

def url_redirect(request, slug):
    try:
        url_data = Urldata.objects.get(short_url=slug)
        return redirect(url_data.url)
    except Urldata.DoesNotExist:
        return redirect('/')
