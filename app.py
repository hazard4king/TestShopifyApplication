import json
from flask import Flask, render_template, url_for
from authlib.integrations.flask_client import OAuth

from ENV_VAR import FACEBOOK_CLIENT_ID, FACEBOOK_CLIENT_SECRET

app = Flask(__name__)
app.secret_key = 'Thisisasecretkey'
app.config['SERVER_NAME'] = 'localhost:5000'
fb = OAuth(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/facebook/')
def facebook():
    fb.register(
        name='facebook',
        client_id=FACEBOOK_CLIENT_ID,
        client_secret=FACEBOOK_CLIENT_SECRET,
        callbackURL='https://example.com/auth/facebook/callback',
        access_token_url='https://graph.facebook.com/oauth/access_token',
        access_token_params=None,
        authorize_url='https://www.facebook.com/dialog/oauth',
        authorize_params=None,
        api_base_url='https://graph.facebook.com/',
        client_kwargs={'scope': 'email'},
    )
    redirect_uri = url_for('facebook_auth', _external=True)
    return fb.facebook.authorize_redirect(redirect_uri)


@app.route('/facebook/auth/')
def facebook_auth():
    token = fb.facebook.authorize_access_token()
    resp = fb.facebook.get(
        'https://graph.facebook.com/me?fields=name,email')
    return render_template('display.html', jsonfile=json.dumps(resp.json()))


if __name__ == "__main__":
    app.run(debug=True)
