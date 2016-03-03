from flask import  Blueprint,render_template
from database.models import News
home_ctrl=Blueprint('home_ctrl',__name__)

@home_ctrl.route("/home")
def index():

    return render_template("home/index.html")

@home_ctrl.route("/news")
def news():

    news=News.query.paginate(1,20);
    return render_template("home/news_center.html",news=news)

@home_ctrl.route("/apps")
def app():
    return render_template("home/app.html")