from django.http import QueryDict
try:
    from django.utils.deprecation import MiddlewareMixin
except ImportError:
    MiddlewareMixin = object


# class HttpPostOtherMiddleware(MiddlewareMixin):
    # def process_request(self, ):