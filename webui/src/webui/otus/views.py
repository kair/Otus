import time

from django.template import Context, loader
from django.http import HttpResponse
from webui.otus.models import Dashboard 

def index(request, view_id):
    t = loader.get_template(view_id)
    c = Context({'cs': time.strftime("%Y/%m/%d-%H:%M:%S", time.localtime(time.time()-60*60)),
                 'ce': time.strftime("%Y/%m/%d-%H:%M:%S", time.localtime()),
                 'metric': 'cpu_user',
                 'hostid': 'cloud1'})
    return HttpResponse(t.render(c))

def indexDashboard(request, dashboardname):
    graph_list = Dashboard.objects.filter(name = dashboardname)
    t = loader.get_template("dashboard.html")
    c = Context({'cs': time.strftime("%Y/%m/%d-%H:%M:%S", time.localtime(time.time()-60*60)),
                 'ce': time.strftime("%Y/%m/%d-%H:%M:%S", time.localtime()),
                 'dashboardname': dashboardname,
                 'graph_list': graph_list
                 }
                )
    return HttpResponse(t.render(c))
