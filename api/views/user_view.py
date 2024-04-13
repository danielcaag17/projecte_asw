from django.http import HttpResponse
from django.template import loader


# TODO: perque surt aquest error de que  no troba .html
def view_user(request):
    template = loader.get_template('view_user.html')
    return HttpResponse(template.render())
