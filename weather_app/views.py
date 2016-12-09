from django.shortcuts import render, redirect
from .forms import UserForm

# Create your views here.
def user_new(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            return redirect('/')
    else:
        form = UserForm()
    return render(request, 'user_create.html', {'form': form})