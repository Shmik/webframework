from urls import urlpatters
from views import http_404

class Router:
    def __init__(self):
        self.patterns = urlpatters
        self.paths, self.views = zip(*urlpatters)

    def __call__(self, path):
        try:
            index = self.paths.index(path)
        except:
            return http_404
        return self.views[index]