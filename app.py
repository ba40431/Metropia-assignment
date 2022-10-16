from flask import *
from routes.user import *
from routes.url import *
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__, template_folder = 'templates', static_folder = 'static')
app.config['JSON_AS_ASCII'] = False
app.config['TEMPLATES_AUTO_RELOAD'] = True
	
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config = {
        'app_name': 'Metropia-assignment API'
    }
)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix = SWAGGER_URL)
app.register_blueprint(get_user)
app.register_blueprint(post_user)
app.register_blueprint(patch_user)
app.register_blueprint(delete_user)
app.register_blueprint(get_url)
app.register_blueprint(post_url)
app.register_blueprint(patch_url)
app.register_blueprint(delete_url)


@app.route('/')
def index():
	return render_template('index.html')

@app.route('/user/<id>')
def user(id):
	return render_template('user.html')

@app.route('/static/<path:path>')
def send_static(path):
	return send_from_directory('static', path)


if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 3000)
