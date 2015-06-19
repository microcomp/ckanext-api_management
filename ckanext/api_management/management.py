# coding=utf-8
import urllib

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import ckan.model as model
import ckan.logic as logic
import ckan.lib.base as base
import ckan.lib.helpers as h
import ckan.lib.navl.dictization_functions as df
import ckan.plugins as p
from ckan.common import _, c, g
#import ckan.lib.app_globals.Globals as g
import ckan.plugins.toolkit as toolkit
import json
import time
import uuid

import logging
import ckan.logic
import __builtin__
import datetime
def apikey_exist(apikey):
	user = model.Session.query(model.User).filter(model.User.apikey == apikey).first()
	return user != None
class APIManagementController(base.BaseController):
    def _setup_template_variables(self, context, data_dict):
        try:
            user_dict = logic.get_action('user_show')(context, data_dict)
        except logic.NotFound:
            abort(404, _('User not found'))
        except logic.NotAuthorized:
            abort(401, _('Not authorized to see this page'))
        c.user_dict = user_dict
        c.is_myself = user_dict['name'] == c.user
        c.about_formatted = h.render_markdown(user_dict['about'])

    def APIManagement(self):
        context = {'model': model, 'session': model.Session,
                   'user': c.user or c.author, 'auth_user_obj': c.userobj,
                   'for_view': True}
        if c.userobj == None:
            base.abort(401, base._('Not authorized to see this page'))
        data_dict = {"id":c.userobj.id}

        self._setup_template_variables(context, data_dict)
        return base.render("API_management/api_management.html") 
    def NewAPIKey(self):
        context = {'model': model, 'session': model.Session,
                   'user': c.user or c.author, 'auth_user_obj': c.userobj,
                   'for_view': True}
        new_key = unicode(uuid.uuid4()) 
        while apikey_exist(new_key):
             new_key = unicode(uuid.uuid4())
        user = model.Session.query(model.User).filter(model.User.id == c.userobj.id).first()
        user.apikey = new_key
        user.save()
        model.Session.commit()
        from_ = base.request.params.get('from', '')

        return h.redirect_to(controller='user', action='read', id=c.userobj.id)
        
def is_installed():
    return True

