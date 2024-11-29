# yourapp/middleware.py

class XFrameOptionsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        print("Custom X-Frame-Options Middleware executed")  # Debug print
        response['X-Frame-Options'] = 'SAMEORIGIN'  # or 'ALLOW-FROM http://example.com'
        return response
