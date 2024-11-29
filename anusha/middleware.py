# myapp/middleware.py
# from django.shortcuts import redirect

# class OTPMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         if not request.user.is_authenticated and not request.path.startswith('/generate-verify-otp/'):
#             return redirect('generate-verify-otp')
#         response = self.get_response(request)
#         return response
# ===================bhanu============

