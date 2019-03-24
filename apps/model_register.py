import sys
import apps.models
from config.settings import INSTALLED_MODELS

class ModelRegister():
    def get_apps(self):
        apps = []
        for conf in INSTALLED_MODELS:
            [module, class_name] = conf.split('.')
            klass = getattr(sys.modules[f'apps.models.{module}'], class_name)
            apps.append(klass)
        return apps
