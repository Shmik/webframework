from webob import Request, Response
from urls import urlpatters
from router import Router

router = Router()

class App(object):

    def __call__(self, environ, start_response):
        request = Request(environ)
        response = self.handle_request(request)

        return response(environ, start_response)

    def handle_request(self, request):
        view = router(request.path)
        return view(request)
