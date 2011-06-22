from django.template import Context, loader
from django.template.loader import render_to_string
from django.http import HttpResponse

def index(request, view_id):
#    return HttpResponse("Hello, world. You're at %s."%(view_id))
    t = loader.get_template(view_id)
    c = Context({})
    return HttpResponse(t.render(c))