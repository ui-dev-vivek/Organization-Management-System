from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from subsidiaries.models import Subsidiaries
from django.urls import resolve

def is_client(view_func):
    @login_required
    def decorated_view_func(request, *args, **kwargs):
        if request.user.is_authenticated and not request.user.is_superuser:
            resolved_kwargs = resolve(request.path_info).kwargs
            subsidiary_slug = resolved_kwargs.get('subsidiary')       
            subsidiary=Subsidiaries.objects.get(clients__user__id=request.user.id);
            if not request.user.is_client or subsidiary.slug!=subsidiary_slug:
                return redirect('/404-error')  
            return view_func(request, *args, **kwargs)
        else:
            return redirect('/')
    return decorated_view_func
#code Closed!