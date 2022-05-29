from .models import Institute

def institute_links(request):
    institute_list = Institute.objects.all()
    return dict(institute_list=institute_list)
