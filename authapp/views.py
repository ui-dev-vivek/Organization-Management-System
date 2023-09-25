from django.shortcuts import render, redirect
from authapp.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.http import HttpResponse
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from django.contrib.auth.decorators import login_required
from decouple import config
from django.core.mail import send_mail
from django.template.loader import render_to_string


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
                        return redirect(subsidiary.slug + "/employee/")
                    except:
                        messages.error(request, "Profile Incompletea!")
                elif request.user.is_client:
                    try:
                        subsidiary = request.user.clients.subsidiary
                        return redirect(subsidiary.slug + "/client/")
                    except:
                        messages.error(request, "Profile Incomplete!")
                elif request.user.is_superuser:
                    try:
                        # subsidiary = request.user.clients.subsidiary
                        return redirect("/admin/")
                    except:
                        messages.error(request, "Profile Incomplete!")
                else:
                    messages.error(request, "You Have No Any Subsidiry")
            else:
                messages.error(request, "Your account is not active.")
        else:
            messages.error(request, "Invalid Email/Username or Password.")
    data = {"app_name": config('APP_NAME')}
    # Create a template named 'login.html'
    return render(request, "auth/login.html", data)


def redirect_login(request):
    return redirect("/")


# @api_view(['POST'])
@login_required
def api_auth_token(request):
    if request.method == "POST": 
        token, created = Token.objects.get_or_create(user=request.user)
        return HttpResponse(token.key)
        


def user_logout(request):
    logout(request)
    return redirect("/")


def forgot_password(request):
    data = {"app_name": config('APP_NAME')}
    if request.method == "POST":
        email = request.POST.get("email")
        try:
            user = User.objects.get(email=email)
        except:
            messages.success(request, "Reset link send on register link")
            return render(request, "auth/forgot_password.html", data)
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        reset_link = request.build_absolute_uri("/") + f"reset-password/{uid}/{token}/"
        # print(reset_link)
        user_name=user.first_name + user.last_name
        # Send the email using the HTML template
        subject = 'Reset Your Password'
        message = f'Click the link to reset your password: {reset_link}'
        from_email = 'your-email@gmail.com'  # Use the same email as configured in settings.py
        recipient_list = [email]

        send_mail(
            subject,
            message,
            from_email,
            recipient_list,
            fail_silently=False,
            html_message=render_to_string('emails/password_reset_email.html', {'reset_link': reset_link,'name':user_name}),
        )
        messages.success(request, "Reset link send on register link")
    
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
            confirm_password=request.POST.get("confirm_password")
            if new_password != confirm_password:
                messages.error(request, "Password are not matched.")
                return redirect(request.META.get("HTTP_REFERER"))
            user.set_password(new_password)
            user.save()
            messages.success(
                request,
                "Your password has been successfully reset. You can now log in with your new password.",
            )
            return redirect("/")

        return render(request, "auth/reset_password.html")

    messages.error(request, "Forgot Password link is invalied. send agen.")
    return redirect("/forgot-password")


def error_404(request):
    return render(request, "error/404.html")


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
