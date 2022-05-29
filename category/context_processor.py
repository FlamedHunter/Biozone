from .models import Category

def categories_links(request):
    categories_list = Category.objects.all()
    return dict(categories_list=categories_list)

