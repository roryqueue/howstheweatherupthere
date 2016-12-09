from django.shortcuts import render
from .forms import UserForm

# Create your views here.
def user_new(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.author = request.user
            user.published_date = timezone.now()
            user.save()
            return redirect('')
    else:
        form = UserForm()
    return render(request, 'user_create.html', {'form': form})