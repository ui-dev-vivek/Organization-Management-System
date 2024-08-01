from django.shortcuts import HttpResponse, render, get_object_or_404, redirect
import os
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from .decorators import is_employee
from subsidiaries.models import Subsidiaries
from projects.models import Projects, EmployeeOnProject
from django.http import HttpResponseBase, request, JsonResponse
from employees.models import Employees
from PIL import Image
from django.contrib import messages
from authapp.models import User
from projects.models import ProjectTask, Projects, TaskChecklist, Attachments


@is_employee
def dashboard(request, subsidiary):
    # logged_in_user=request.user
    # user_projects = Projects.objects.filter(employeeonproject__employees__user=logged_in_user)
    return render(request, "employee/dashboard.html")


@is_employee
def emp_profile(request, subsidiary):
    user = request.user
    try:
        employee = Employees.objects.get(user=user)
    except Employees.DoesNotExist:
        messages.success(request, "Employee record not found for the user.")
        # return render(request,'error.html',{'error_message': 'Employee record not found for the user.'});
    if request.method == "POST":
        user.first_name = request.POST.get("first_name")
        user.last_name = request.POST.get("last_name")
        user.email = request.POST.get("email")
        user.save()
        messages.success(request, "Profile updated successfully.")

    data = {"user": request.user}
    return render(request, "employee/profile.html", data)


@is_employee
def project(request, subsidiary, slug):
    employee_data = Employees.objects.get(user=request.user)
    project = get_object_or_404(Projects, slug=slug)

    userproject = EmployeeOnProject.objects.filter(
        employees=employee_data, project=project
    )
    allemployes = (
        EmployeeOnProject.objects.select_related("employees__user")
        .filter(project=project)
        .all()
    )
    members = []
    for employee in allemployes:
        employee_data = employee.employees
        user_data = employee_data.user
        employee_with_user = {
            "name": user_data.first_name + " " + user_data.last_name,
            "employee_type": employee_data.get_emp_type_display,
            "is_lead": employee.is_lead,
            "profile_image": employee_data.profile_image.url,
        }
        members.append(employee_with_user)

    project_tasks = ProjectTask.objects.filter(project=project)
    tasks_data = []

    for task in project_tasks:
        checklist_items = TaskChecklist.objects.filter(project_task=task)
        total_checklist_count = checklist_items.count()
        checked_count = checklist_items.filter(status=True).count()
        if total_checklist_count != 0:
            progress = (checked_count / total_checklist_count) * 100
        else:
            progress = 0
        task_data = {
            "task": task,
            "checklist_items": checklist_items,
            "checked": checked_count,
            "taskchecklistcount": total_checklist_count,
            "progress": progress,
        }
        tasks_data.append(task_data)

    attachments = Attachments.objects.filter(project=project)

    attachment_data = []
    for attachment in attachments:
        attachment_data.append(
            {
                "id": attachment.uid,
                "file_name": attachment.file_name,
                "attachment_file": attachment.attachment_file.url.split("/")[-1],
            }
        )

    data = {
        "project": project,
        "userproject": userproject,
        "members": members,
        "tasks_data": tasks_data,
        "attachments": attachment_data,
    }

    return render(request, "employee/project.html", data)


@is_employee
def project_task_view(request, subsidiary):
    if request.method == "POST":
        try:
            data = request.POST  

          
            project = data.get("project")
            title = data.get("title")
            description = data.get("description")

           

            end_date = data.get("end_date")
            if not project or not title or not description or not end_date:
                message.error(request, "Fill all fields.")
                return redirect(request.META.get("HTTP_REFERER"))
            # Assuming project_id is the ID of the associated project
            project = get_object_or_404(Projects, id=project)

            task = ProjectTask.objects.create(
                project=project,
                assigned_to=request.user,
                title=title,
                description=description,
                end_date=end_date,
            )

            messages.success(request, "Task added successfully.")

        except Exception as e:
            messages.error(request, "Falied to add Task.")
        return redirect(request.META.get("HTTP_REFERER"))


@is_employee
def update_project_task(request, subsidiary):
    try:
        task = get_object_or_404(ProjectTask, uid=request.POST.get("task_id"))
        task.title = request.POST.get("title", task.title)
        task.description = request.POST.get("description", task.description)
        task.end_date = request.POST.get("end_date", task.end_date)
        task.save()

        checklist_ids = request.POST.getlist("checklist_id[]")
        titles = request.POST.getlist("titles[]")

        statuses = request.POST.getlist("status[]")

        projecttask = get_object_or_404(ProjectTask, uid=request.POST.get("task_id"))

        for i in range(len(checklist_ids)):
            if checklist_ids[i] != "no":
                checklist_item = get_object_or_404(TaskChecklist, uid=checklist_ids[i])
                checklist_item.title = titles[i]
                checklist_item.status = True if checklist_ids[i] in statuses else False
                checklist_item.save()

            else:
                if titles[i] != "":
                    TaskChecklist.objects.create(
                        project_task=projecttask, title=titles[i], status=False
                    )
                else:
                    messages.error(request, "Empty Checklists are removed!")

        messages.success(request, "Task and checklist updated successfully.")
    except Exception as e:
        # return JsonResponse({'error': str(e)}, status=400)
        messages.error(request, "Falied To Create checklist.")
    return redirect(request.META.get("HTTP_REFERER"))


@is_employee
def upload_attachment(request, subsidiary):
    if "attachment" in request.FILES:
        attachment = request.FILES["attachment"]

        # Check if the file extension is allowed
        allowed_extensions = [
            ".zip",
            ".docx",
            ".xlsx",
            ".ppt",
            ".pdf",
            ".png",
            ".jpg",
            ".jpeg",
            ".webp",
        ]
        extension = os.path.splitext(attachment.name)[1].lower()
        if extension not in allowed_extensions:
            error="Invalid file extension. Allowed extensions are: {}".format(",".join(allowed_extensions))
            messages.error(request,error)
            return redirect(request.META.get("HTTP_REFERER"))
        project = get_object_or_404(Projects, id=request.POST.get("project_id"))
        # Save the attachment to the server
        upload_path = "static/attachments/" + subsidiary + "-" +project.slug+"-"+ attachment.name
        with open(upload_path, "wb+") as destination:
            for chunk in attachment.chunks():
                destination.write(chunk)
        
        attachment_instance = Attachments.objects.create(
            project=project,
            upload_by=request.user,
            file_name=request.POST.get("file_name"),  # attachment.name,
            attachment_file=upload_path,
        )

        messages.success(request, "Attachment File Uploaded!")
    return redirect(request.META.get("HTTP_REFERER"))


# XHttp
@is_employee
def delete_project_task(request, subsidiary, task_id):
    try:
        task = get_object_or_404(ProjectTask, uid=task_id)
        task.delete()
        return JsonResponse({"message": "Task deleted successfully."}, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


def delete_project_task_checklist(request, subsidiary, task_id):
    try:
        task = get_object_or_404(TaskChecklist, uid=task_id)
        task.delete()
        return redirect(request.META.get("HTTP_REFERER"))
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


@is_employee
def delete_project_task(request, subsidiary, task_id):
    try:
        task = get_object_or_404(ProjectTask, uid=task_id)
        task.delete()
        return JsonResponse({"message": "Task deleted successfully."}, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


def delete_attachment(request, subsidiary, task_id):
    try:
        task = get_object_or_404(Attachments, uid=task_id)
        task.delete()
        return redirect(request.META.get("HTTP_REFERER"))
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


# XHttp Methods. For JS
@is_employee
def upload_profile_image(request, subsidiary):
    if request.method == "POST" and request.FILES.get("profile_image"):
        user = request.user
        try:
            employee = Employees.objects.get(user=user)
        except ObjectDoesNotExist:
            return JsonResponse(
                {"error": "Employee record not found for the user."}, status=400
            )

       
        if employee.profile_image:
            old_image_path = os.path.join(settings.MEDIA_ROOT, str(employee.profile_image.url))
            if os.path.exists(old_image_path):
                os.remove(old_image_path)

        uploaded_image = request.FILES["profile_image"]

        
        img = Image.open(uploaded_image)
        img = img.resize((150, 150), Image.ANTIALIAS)

       
        resized_image_path = os.path.join("profile_images", uploaded_image.name)

       
        resized_image_full_path = os.path.join(settings.MEDIA_ROOT, resized_image_path)
        img.save(resized_image_full_path)

        employee.profile_image = resized_image_path
        employee.save()

        
        image_url = os.path.join(settings.MEDIA_URL, resized_image_path)
        return JsonResponse({"image_url": image_url})
    else:
        return JsonResponse(
            {"error": "Image not provided or invalid request."}, status=400
        )

# code Closed!
