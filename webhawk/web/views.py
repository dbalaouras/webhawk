import os

from flask import render_template
from flask import send_from_directory

from . import website_blueprint as webapp


@webapp.route("")
def dashboard():
    """
    Render HomePage
    :return: Flask Response
    """
    return render_template('dashboard.html')


@webapp.route('favicon.ico')
@webapp.route('favico.ico')
def favicon():
    """
    Send FavIcon
    :return: Flask Response
    """
    return send_from_directory(os.path.join(webapp.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')
