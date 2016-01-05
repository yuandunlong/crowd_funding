from flask import  Blueprint,render_template

home_ctrl=Blueprint('home_ctrl',__name__)

@home_ctrl.route("/home")
def index():

    return render_template("home/index.html")
