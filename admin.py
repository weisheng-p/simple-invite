import webapp2
import os
import uuid

from google.appengine.api import users
from google.appengine.ext.webapp import template

from models import Invite

invite_code_len = 6


class AdminMainPage(webapp2.RequestHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__), './templates/admin/index.html')
        self.response.out.write(template.render(path, {}))


class InviteAdminHandler(webapp2.RequestHandler):
    def post(self):
        name = self.request.get('name')
        email = self.request.get('email')
        invite_code = uuid.uuid4().hex[:invite_code_len].upper()
        while(Invite.query(Invite.code==invite_code).get()):
            invite_code = uuid.uuid4().hex[:invite_code_len].upper()
        invite = Invite(code=invite_code, name=name, email=email)
        invite.put()
        context = {
            'invite': invite,
            'invite_url': webapp2.uri_for('invite', invite_code=invite.code)
        }
        path = os.path.join(os.path.dirname(__file__), './templates/admin/index.html')
        self.response.out.write(template.render(path, context))
