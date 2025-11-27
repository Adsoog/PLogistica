from django.shortcuts import render


def casa(request):
    return render(request, 'casa/pages/casa.html')