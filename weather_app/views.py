from django.shortcuts import render, redirect, render_to_response
from .forms import UserForm

# Create your views here.
def user_new(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=True)
            return redirect('/success')
    else:
        form = UserForm()

    return render(request, 'user_create.html', {'form': form})

def subscription_success(request):
   return render_to_response('subscription_success.html')
