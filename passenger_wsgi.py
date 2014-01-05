import sys, os
INTERP = os.path.join(os.environ['HOME'], 'venvs', 'pymileage', 'bin', 'python')
if sys.executable != INTERP:
    os.execl(INTERP, INTERP, *sys.argv)
sys.path.append(os.getcwd())
from app import app as application

# Uncomment next two lines to enable debugging
# from werkzeug.debug import DebuggedApplication
# application = DebuggedApplication(application, evalex=True)
