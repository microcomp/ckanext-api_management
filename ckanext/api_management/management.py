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
    def APIManagement(self):
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
        return base.render("API_management/api_management.html") 