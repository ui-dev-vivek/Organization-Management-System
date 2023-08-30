from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from dotenv import dotenv_values
from django.contrib.auth import authenticate, login, logout
# from django.http import HttpResponseRedirect, HttpResponse
# from django.contrib.auth.decorators import login_required
# from django.shortcuts import get_object_or_404
# from subsidiaries.models import Organizations
# from subsidiaries.models import Subsidiaries
# from employees.models import Employees
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
# from django.core.mail import send_mail

# Create your views here.
ENV = dotenv_values(".env")


def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                # Redirect to your desired page after login
                if request.user.role == "employee":
                    subsidiary = request.user.employees.subsidiary
                elif request.user.role == "client":
                    subsidiary = request.user.employees.subsidiary
                else:
                    messages.error(request, "You Have No Any Subsidiry")

                return redirect(subsidiary.slug + "/" + request.user.role)
            else:
                messages.error(request, "Your account is not active.")
        else:
            messages.error(request, "Invalid Email/Username or Password.")
    data = {"app_name": ENV.get("APP_NAME")}
    # Create a template named 'login.html'
    return render(request, "auth/login.html", data)


def user_logout(request):
    logout(request)
    return redirect("/")


def forgot_password(request):
    if request.method == "POST":
        email = request.POST.get("email")
        user = User.objects.get(email=email)

        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        reset_link = request.build_absolute_uri("/") + f"reset-password/{uid}/{token}/"
        print(reset_link)
        # send_mail(
        #     'Reset Your Password',
        #     f'Click the link to reset your password: {reset_link}',
        #     'from@example.com',
        #     [email],
        #     fail_silently=False,
        # )
        messages.success(request, "Reset link send on register link")
    data = {"app_name": ENV.get("APP_NAME")}
    return render(request, "auth/forgot_password.html", data)


def reset_password(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64)
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        if request.method == "POST":
            new_password = request.POST.get("new_password")
            user.set_password(new_password)
            user.save()
            messages.success(
                request,
                "Your password has been successfully reset. You can now log in with your new password.",
            )
            return redirect("/")

        return render(request, "auth/reset_password.html")

    return render(request, "invalid_token.html")


# @login_required
# def subsidiaries(request):
#     user = request.user
#     try:
#         employee = Employees.objects.get(user=user)
#         organization = employee.subsidiary.organization
#         subsidiaries = organization.subsidiaries_set.all()
#     except Employees.DoesNotExist:
#         organization = None
#         subsidiaries = []
#     data = {
#         'app_name': ENV.get('APP_NAME'),
#         'organization':organization ,
#         'subsidiaries':subsidiaries
#     }
#     return render(request,'auth/subsidiaries.html',data);
