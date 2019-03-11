from webob import Response
from jinja2 import Template
from config.jinja import env

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
    template = env.get_template('welcome.html')
    rendered = template.render(heading='Welcome to my new page')
    response.text = rendered
    return response