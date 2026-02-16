from django.shortcuts import render
from .models import Member

def member(request):
    mymembers = Member.objects.all()
    return render(request, "index.html", {"mymembers": mymembers})

def details(request, id):
    mymember = Member.objects.get(id=id)
    return render(request, "details.html", {"mymember": mymember})
