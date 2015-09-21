from flask import Blueprint,request
from database.models import Project
from utils.decorator import json_response,require_token

project_api=Blueprint('project_api', __name__)
@project_api.route('/public/get_projects_by_page',methods=['GET'])
@json_response
def get_projects_by_page(result):
    data=request.get_json()

    page=data.get('page',1)
    page_size=data.get('page_size',20)

    #Project.query.limit

