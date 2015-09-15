from flask import Blueprint,request
from database.models import Project
from utils.decorator import json_response,require_token
from services import project_service
project_api=Blueprint('project_api', __name__)
@project_api.route('/public/project/get_projects_by_page',methods=['POST'])
@json_response
def get_projects_by_page(result):
    data=request.get_json()

    page=data.get('page',1)
    page_size=data.get('page_size',20)

    projects=project_service.get_projects_by_page(page,page_size)

    arr=[]
    for project in projects:
        arr.append(project.as_map())
    result['projects']=arr

