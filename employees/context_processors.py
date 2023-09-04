from projects.models import Projects
from django.contrib.auth.decorators import login_required
from django.urls import resolve
@login_required
def user_projects(request):
    resolved_kwargs = resolve(request.path_info).kwargs
    subsidiary = resolved_kwargs.get('subsidiary') 
    logged_in_user = request.user
    user_projects = Projects.objects.filter(employeeonproject__employees__user=logged_in_user)
    return {'user_projects': user_projects,'subsidiary':subsidiary}
