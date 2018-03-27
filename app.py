import argparse
import json

from flask import Flask, render_template
from flask_httpauth import HTTPDigestAuth

from bot import Bot, os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('DEEPMEX_SECRET')
auth = HTTPDigestAuth()
bot = Bot()

@auth.get_password
def get_pw(username):
    if username != os.environ.get('DEEPMEX_USERNAME'):
        return None
    return os.environ.get('DEEPMEX_PASSWORD')

@app.route('/')
@auth.login_required
def index():
    market_price = bot.market_last_price()
    position     = bot.bitmex.current_position()
    history      = bot.bitmex.wallet_history()

    return render_template('index.html',
                           market_price=market_price,
                           position=position,
                           history=history,
                           data=json.dumps(history))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', default=False, action='store_true')
    args = parser.parse_args()

    try:
        bot.debug = args.debug
        bot.run()
        app.run(host='0.0.0.0')
    except (KeyboardInterrupt, SystemExit):
        bot.exit()