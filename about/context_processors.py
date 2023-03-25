from .models import AboutWebsite,AboutMe

def about_website_context(request):
    return { 
        'website':AboutWebsite.objects.last(),
    }

def about_me_context(request):
    return {
        'about_me':AboutMe.objects.last()
    }