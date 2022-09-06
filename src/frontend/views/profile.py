from backend.load import db
from flask import Blueprint, render_template

profile_bp = Blueprint('profile_bp', __name__, url_prefix='/profile')


@profile_bp.route('/<name>')  # name has + for whitespace
def profile(name):
    rname = name.replace("+", " ")
    f = db.get_member(rname)
    return render_template("profile.html", faculty=f)
