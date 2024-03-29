from flask import Flask, render_template

from frontend.views import home, profile, summary, search

app = Flask(__name__)
app.config['SECRET_KEY'] = "A very secret key"


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


app.register_blueprint(home.home_bp)
app.register_blueprint(profile.profile_bp)
app.register_blueprint(summary.summary_bp)
app.register_blueprint(search.search_bp)
