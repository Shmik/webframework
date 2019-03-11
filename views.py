from webob import Response

def http_404(request):
    response = Response()
    response.text = 'Http404'
    return response

def hello_world(request):
    response = Response()
    response.text = 'Hello World'
    return response

def welcome(request):
    response = Response()
    response.text = 'Welcome to this page'
    return response