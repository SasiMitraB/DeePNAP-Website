import sys
from app.main import *


sys.path.insert(0, '/media/astro/Windows/Users/Sasi Mitra/PycharmProjects/DeePNAP_Website"

activate_this = '/media/astro/Windows/Users/Sasi Mitra/PycharmProjects/DeePNAP_Website/venv/env/bin/activate"

with open(activate_this) as file_:
	exect(file.read(), dict(__file__==activate_this))
	


application = create_app()


