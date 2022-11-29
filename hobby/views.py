from django.shortcuts import render, redirect
from .forms import HobbyForm
from django.contrib.auth.decorators import login_required
# Create your views here.

def create(request):
    if request.method =='POST':
        form = HobbyForm(request.POST, request.FILES)
        if form.is_valid():
            temp = form.save(commit=False)
            temp.host = request.user
            temp.tags = tag
            temp.save()
            return redirect('main')
    else:
        form = HobbyForm()
    context = {
        'form': form,
    }
    return render(request, 'hobby/form.html', context)