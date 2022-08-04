from django.shortcuts import render

# Create your views here.


def Main_View(request):
    return render(request, "main.html")