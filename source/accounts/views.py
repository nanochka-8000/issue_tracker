from django.contrib.auth import login
from django.shortcuts import redirect, render

from .forms import RegisterForm


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            next_url = request.GET.get('next') or request.POST.get('next')
            if next_url:
                return redirect(next_url)
            return redirect('task_list')
    else:
        form = RegisterForm()

    next_url = request.GET.get('next', '')
    return render(request, 'accounts/register.html', {
        'form': form,
        'next': next_url,
    })