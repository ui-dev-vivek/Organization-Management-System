from projects.models import Projects
from django.contrib.auth.decorators import login_required
from django.urls import resolve
# @login_required
def user_projects(request):
    if request.user.is_authenticated:
        resolved_kwargs = resolve(request.path_info).kwargs
        subsidiary = resolved_kwargs.get('subsidiary') 
        logged_in_user = request.user
        if request.user.is_client:
            user_projects = Projects.objects.filter(clientonproject__clients__user=logged_in_user)
        elif request.user.is_employee:
            user_projects = Projects.objects.filter(employeeonproject__employees__user=logged_in_user)
        else:
            user_projects=[]
        return {'user_projects': user_projects, 'subsidiary': subsidiary}
    else:
        return {'user_projects': []}
    

#code Closed!