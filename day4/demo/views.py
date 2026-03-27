from django.shortcuts import render

def home(request):
    return render(request, 'index.html')

# def about(request):
#     return HttpResponse("about")

# def services(request):
#     return HttpResponse("services")