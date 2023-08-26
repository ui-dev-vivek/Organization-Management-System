from django.shortcuts import redirect

class RoleRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        user = request.user

        if user.is_authenticated:
            if user.is_employee:
                if not request.path.startswith('/empolyees/'):
                    return redirect('/')
            elif user.is_client:
                if not request.path.startswith('/clients/'):
                    return redirect('/')

        return response
