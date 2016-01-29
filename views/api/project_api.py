from flask import Blueprint, request
from database.models import Project,db
from utils.decorator import json_response, require_token
from services import project_service

project_api = Blueprint('project_api', __name__)


@project_api.route('/public/project/get_projects_by_page', methods=['POST'])
@json_response
def get_projects_by_page(result):
    data = request.get_json()

    page = data.get('page', 1)
    page_size = data.get('page_size', 20)
    is_recommend = data.get('is_recommend', None)
    status = data.get('status', None)
    order_by = data.get('order_by')
    if order_by == "update":
        order_by = 'updated_time desc'
    elif order_by == "create":
        order_by = "created_time desc"
    (projects, paginate) = project_service.query_projects_by_page(page=page, page_size=page_size, order_by=order_by,
                                                                  querys={"status": status,
                                                                          'is_recommend': is_recommend})

    arr = []
    for project in projects:
        arr.append(project.as_map())
    result['projects'] = arr


@project_api.route('/public/project/get_project_by_id', methods=['POST'])
@json_response
def get_project_by_id(result):
    data = request.get_json()

    project_id = data.get('project_id', None)

    project = Project.query.get(project_id)

    if project:
        result['project'] = project.as_map()


@project_api.route('/private/project/add_support', methods=['POST'])
@require_token
@json_response
def add_support():
    data = request.json
    project_id = data.get('project_id', None)
    if project_id:
        project = Project.query.get(project_id)
        project.support_times=project.support_times+1
        db.session.commit()