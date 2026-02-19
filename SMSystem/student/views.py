from django.shortcuts import render

# Create your views here.
from .forms import InputForm

def input_view(request):
    if request.method == 'POST':
        form = InputForm(request.POST)
        if form.is_valid():
            # Process the form data here (e.g., save to database)
            name = form.cleaned_data['name']
            age = form.cleaned_data['age']
            roll_number = form.cleaned_data['roll_number']
            # You can save this data to your model or perform other actions
            return render(request, 'success.html', {'name': name})
    else:
        form = InputForm()
    
    return render(request, 'index.html', {'form': form})

