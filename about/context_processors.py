from .models import AboutWebsite

def about_website(request):
    return { 
        'website':AboutWebsite.objects.last(),
    }