from django.shortcuts import render

# Create your views here.
def echo_page(request):
    return render(request, "app/echopage.html")