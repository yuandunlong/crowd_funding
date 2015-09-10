from flask import request, Blueprint
from services.user_service import get_challenge
user_ctrl = Blueprint("user_ctrl", __name__)

@user_ctrl.route("/user/get_challenge",methods=['GET'])
def get_challenge():
    return get_challenge()



