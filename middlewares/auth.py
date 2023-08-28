from django.shortcuts import render, redirect
from subsidiaries.models import Subsidiaries
from django.contrib import messages


class RoleRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if not request.user.is_authenticated:
            return render(request, "auth/login.html")
        user = request.user
        if user.is_authenticated:
            try:
                url_parts = request.path.split("/")  
                print(url_parts)              
                if user.role == "employee":
                    subsidiary_slug = Subsidiaries.objects.get(
                    employees__user_id=request.user.id
                    ).slug
                     
                    if (url_parts[1] != subsidiary_slug ):
                        messages.error(
                            request,
                            "Subsidiary Not match!",
                        )
                        return redirect("/logout")
                elif user.role == "client":
                    subsidiary_slug = Subsidiaries.objects.get(
                    clients__user_id=request.user.id
                    ).slug
                    if (url_parts[1] != subsidiary_slug and url_parts[2] !='employee'):
                        messages.error(
                            request,
                            "Subsidiary Not match!",
                        )
                        return redirect("/logout")
            except Subsidiaries.DoesNotExist:
                messages.success(
                    request,
                    "You Are Not Asosiative with any Orgnizations",
                )
                return redirect("/logout")
        else:
            messages.error(
                request,
                "Authentication falied!",
            )
            return redirect("/")

        return response
