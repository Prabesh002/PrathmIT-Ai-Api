import urllib.parse
import werkzeug.urls
if not hasattr(werkzeug.urls, 'url_quote'):
    werkzeug.urls.url_quote = urllib.parse.quote

from flask import Flask
import os
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    from app.routes import home, upload, query
    app.register_blueprint(home.bp)
    app.register_blueprint(upload.bp)
    app.register_blueprint(query.bp)
    return app
