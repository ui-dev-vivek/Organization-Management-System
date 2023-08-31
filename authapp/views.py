from django.shortcuts import render, redirect
from authapp.models import User
from dotenv import dotenv_values
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.http import HttpResponse

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
                if request.user.is_employee:
                    try:
                        subsidiary = request.user.employees.subsidiary
                        return redirect(subsidiary.slug + "/employee")
                    except:
                        messages.error(request, "Profile Incompletea!")
                elif request.user.is_client:
                    try:
                        subsidiary = request.user.employees.subsidiary
                        return redirect(subsidiary.slug + "/client")
                    except:
                        messages.error(request, "Profile Incomplete!")
                else:
                    messages.error(request, "You Have No Any Subsidiry")

                
            else:
                messages.error(request, "Your account is not active.")
        else:
            messages.error(request, "Invalid Email/Username or Password.")
    data = {"app_name": ENV.get("APP_NAME")}
    # Create a template named 'login.html'
    return render(request, "auth/login.html", data)

def redirect_login(request):
    return redirect('/')

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


def error_404(request):
    return render(request,'error/404.html')
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
