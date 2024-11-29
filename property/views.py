from django.http import HttpResponse

def sample_page(request):
    return HttpResponse("<h1>Sample Page - The App is Running!</h1>")
