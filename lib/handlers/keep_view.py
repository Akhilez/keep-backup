from django.shortcuts import render
from keep.lib.keep_manager import KeepManager
from datetime import datetime


def get_view(request):
    context = {}
    template = 'keep/home.html'
    if request.method == 'POST':
        if 'backup_submit' in request.POST:
            email = request.POST['email']
            password = request.POST['password']

            keep = KeepManager(email, password)
            data = keep.get_data()
            if data is None:
                context['failed'] = True
            context['data'] = data
            context['datetime'] = datetime.now()

    return render(request, template, context)

