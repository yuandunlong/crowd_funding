from flask import  Blueprint,render_template

index_ctrl=Blueprint('index_ctrl',__name__)

@index_ctrl.route('/',methods=['GET'])
def index():

    return render_template("app/index.html")
