from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    #Construct a dict to pass to the template engine
    context_dict = {'boldmessage': 'Crunchy, creamy, cookie, candy, cupcake!'}

    #Returns a rendered response to send to the client
    return render(request, 'rango/index.html', context=context_dict)
   

def about(request):
    context_dict = {'boldmessage': 'This tutorial has been put together by Claire.'}
    return render(request, 'rango/about.html', context=context_dict)

