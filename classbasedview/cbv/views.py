from django.shortcuts import render

# Create your views here.
from django.views import View
class HomeView(View):
    def get(self, request):
        return render(request, 'index.html')
    
    def post(self, request):
        name = request.POST.get('name')
        context = {
            'name': name
        }
        return render(request, 'index.html', context)
    
    def put(self, request):
        return render(request, 'index.html')
    
    def delete(self, request):
        return render(request, 'index.html')
