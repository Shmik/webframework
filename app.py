from webob import Request, Response

class App(object):

    def __call__(self, environ, start_response):
        request = Request(environ)
        response = self.handle_request(request)

        return response(environ, start_response)

    def handle_request(self, request):
        response = Response()
        response.text = 'Hello, World again'
        return response
