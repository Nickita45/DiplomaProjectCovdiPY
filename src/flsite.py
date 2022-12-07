from flask import Flask, render_template, request, flash, redirect, url_for, session, abort
import imblearn
import matplotlib.pyplot as plt

from src.models import utils
from src.models.naive_bayes import naive_bayes

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dsadsdasdadsdadad'

models_ = ["GNB", "Decision Tree", "Neural Network", "Random Forest", "SVM"]

menu = [{"name": "Setup", "url": "install-flask"},
        {"name": "Info", "url": "info=page"},
        {"name": "Contacts", "url": "contact"}]


@app.route("/")
def index():
    return render_template('index.html', title="main", menu=menu)


@app.route("/home")
def about():
    return "<h1>About website</h1>"


@app.route("/contact", methods=["POST", "GET"])
def contact():
    if request.method == 'POST':
        if len(request.form['username']) > 2:
            flash('Message send', category='success')
        else:
            flash('Error sending', category='error')
        print(request.form)
        print(request.form['username'])

    return render_template('contact.html', title="Feedback", menu=menu)


# path: said take all line include /
# int: only numbers
# float: only floats
@app.route("/profile/<path:username>")
def profile(username):
    if 'userLogged' not in session or session['userLogged'] != username:
        abort(401)
    return f"Client name: {username}"


@app.route("/login", methods=["POST", "GET"])
def login():
    if 'userLogged' in session:
        return redirect(url_for('profile', username=session['userLogged']))
    elif request.method == 'POST' and request.form['username'] == "selfedu" and request.form['psw'] == "123":
        session['userLogged'] = request.form['username']
        return redirect(url_for('profile', username=session['userLogged']))

    return render_template('login.html', title="Авторизация", menu=menu)


@app.errorhandler(404)
def pageNotFount(error):
    return render_template('page404.html', title="Страница не найдена", menu=menu)



# DIPLOMA PROJECT
@app.route("/models", methods=["POST", "GET"])
def models():
    modelType = None
    if request.method == 'POST':
        modelType = request.form['modelslist']
        checked = 'sampling_status' in request.form
        features = utils.get_feature_names()
        feature_importances = sorted(naive_bayes(sampling=checked))
        _, weight = zip(*feature_importances)
        #plt_bar_chart(features, weight, "GNB", "permuation importance", 4383, 1051)
        utils._save_plt_bar_chart(features, weight, modelType, "permuation importance", request.form['shape_count_yes'], request.form['shape_count_no'])

    return render_template('modelPage.html', title="Feedback", models_=models_,modelType=modelType)


if __name__ == '__main__':
    app.run(debug=True)
