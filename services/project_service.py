# -*- coding: utf-8 -*-

from database.models import Project
def get_projects_by_page(page=1,page_size=20,order_by='updated_time desc'):

    projects=Project.query.order_by(order_by).limit(int(page_size)).offset((int(page)-1)*int(page_size)).all()
    return projects







