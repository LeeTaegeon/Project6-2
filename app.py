from flask import Flask, request, send_file, make_response, jsonify, render_template, redirect, send_from_directory
from flask.helpers import url_for
from munch import Munch

from models import StarGANv2
from utils import load_cfg, cache_path

from PIL import Image
import werkzeug

cfg = load_cfg()
app = Flask(__name__)


@app.context_processor
def inject_config():
    return dict(cfg=cfg)
 

@app.route('/')
def login():
    return render_template('login.html')


@app.route("/login_confirm", methods=['POST'])
def login_confirm():
    id_ = request.form['id_']
    pw_ = request.form['pw_']
    if id_ == 'LeeTaegeon' and pw_ == '12345':
        return redirect(url_for('index'))
    else:
        return redirect(url_for('login'))


@app.route("/index")
def index():
    return render_template('index.html')



@app.route("/model", methods=['GET', 'POST'])
def model():
    return render_template('celebahq.html')


@app.route('/model/<model_id>', methods=['GET'])
def model_page(model_id):
    if model_id in cfg.models:
        model = cfg.models[model_id]
        return render_template(f'{model_id}.html', title=model['name'], description=model['description'])
    else:
        return render_template('index.html', message=f'No such model: {model_id}.', is_warning=True)
    

@app.route('/api/model', methods=['POST'])
def model_inference():
    res = Munch({
        "success": False,
        "message": "default message",
        "data": None
    })

    try:
        model_name = request.form['model']
        if model_name == 'celebahq':
            res = StarGANv2.controller(request)
        else:
            res.message = f"no such model: {model_name}"
    except Exception as e:
        res.message = str(e)
        print(e)
    return res


@app.route('/cache/<path:filename>')
def cached_image(filename):
    return send_from_directory(cache_path, filename)



StarGANv2.init(cfg.device)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)