# expõe o objeto 'application' para o servidor WSGI do PythonAnywhere
import sys, os
project_home = os.path.expanduser('~/testeDeploy')  # ajuste o nome da pasta
if project_home not in sys.path:
    sys.path.insert(0, project_home)

from app import app as application
