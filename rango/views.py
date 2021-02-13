from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import reverse
from django.http import HttpResponse
#Import the Category & Page models
from rango.models import Category
from rango.models import Page
from rango.forms import CategoryForm
from rango.forms import PageForm

def index(request):
    #Query the database for a list of all categories currently stored, order them by
    #likes, descending. Retrieve the top 5 only -- or all if less than 5
    #Place these in context_dict dictionary that is passed out to the template engine
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]

    context_dict = {}
    context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    context_dict['categories'] = category_list
    context_dict['pages'] = page_list

    #Render response & send it back
    return render(request, 'rango/index.html', context=context_dict)


def about(request):
    context_dict = {'boldmessage': 'This tutorial has been put together by Claire.'}
    return render(request, 'rango/about.html', context=context_dict)


def show_category(request, category_name_slug):
    #Create a context dictionary which we can pass to the
    #template rendering engine
    context_dict = {}

    try:
        #Tries to find a category name slug with the given name
        #if not, .get() raises a DoesNotExist exception; otherwise returns
        #one model instance
        category = Category.objects.get(slug=category_name_slug)

        #retrieve all associated pages. filter() returns list of page objects
        #or empty list
        pages = Page.objects.filter(category=category)

        #adds our results list to the template context under name pages
        context_dict['pages'] = pages

        #we also add the catergory object from the database to the context dict
        context_dict['category'] = category
    except Category.DoesNotExist:
        #specified category not found. template displays the "no category" msg
        context_dict['category'] = None
        context_dict['pages'] = None

    #render response and return it to client
    return render(request, 'rango/category.html', context=context_dict)


def add_category(request):
    form = CategoryForm()

    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            #save the new category to the database
            form.save(commit=True)
            #redirect user back to index view
            return redirect('/rango/')
        else:
            #the form contains errors, print them to terminal
            print(form.errors)

    #Handles bad form, new form, or no form supplied cases
    return render(request, 'rango/add_category.html', {'form': form})

def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None

    #Can't add page to a category that doesn't exist
    if category is None:
        return redirect('/rango/')

    form = PageForm()

    if request.method == 'POST':
        form = PageForm(request.POST)

        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()

                return redirect(reverse('rango:show_category',
                                        kwargs={'category_name_slug':
                                                category_name_slug}))
        else:
            print(form.errors)

    context_dict = {'form': form, 'category': category}
    return render(request, 'rango/add_page.html', context=context_dict)
        

