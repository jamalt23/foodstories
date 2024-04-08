from django.shortcuts import render
from accounts.forms import RegisterForm

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
    form = RegisterForm()
    return render(request, 'register.html', {'form': form})
