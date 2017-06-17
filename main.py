import webapp2
import os
from datetime import datetime


from google.appengine.api import users
from google.appengine.ext.webapp import template
from admin import AdminMainPage, InviteAdminHandler

from models import Invite


class Main(webapp2.RequestHandler):
    def get(self, invite_code):
        invite = Invite.query(Invite.code==invite_code).get()
        if invite:
            invite.last_viewed = datetime.now()
            invite.viewed += 1
            invite.put()
            path = os.path.join(os.path.dirname(__file__), './templates/invite.html')
            context = {
                'invite': invite,
                'rsvped': invite.accepted is not None,
                'accepted': invite.accepted is None or invite.accepted,
                'rejected': invite.accepted is False,
            }
            self.response.out.write(template.render(path, context))
        else:
            self.response.set_status(404)
            self.response.write('not found')

    def post(self, invite_code):
        invite = Invite.query(Invite.code==invite_code).get()
        if invite:
            errors = {}
            status = self.request.get('status')
            if status not in ['accepted', 'rejected']:
                errors['status'] = 'invalid'
            else:
                invite.accepted = (status == 'accepted')
            if status == 'accepted':
                guest = self.request.get('guest')
                try:
                    guest = int(guest)
                    if guest < 0:
                        errors['guest'] = 'has to be more than zero'
                    else:
                        invite.guest = guest
                except:
                    errors['guest'] = 'has to be a number'


            path = os.path.join(os.path.dirname(__file__), './templates/invite.html')
            if errors:
                context = {
                    'invite': invite,
                    'updated': False,
                    'errors': errors,
                    'accepted': invite.accepted is None or invite.accepted,
                    'rejected': invite.accepted is False,
                }
            else:
                invite.put()
                context = {
                    'invite': invite,
                    'updated': True,
                    'accepted': invite.accepted is None or invite.accepted,
                    'rejected': invite.accepted is False,
                }
            self.response.out.write(template.render(path, context))
        else:
            self.response.set_status(404)
            self.response.write('not found')


app = webapp2.WSGIApplication([
    webapp2.Route(r'/invite/admin', handler=AdminMainPage, name="admin-home"),
    webapp2.Route(r'/invite/add', handler=InviteAdminHandler, name="admin-add"),
    webapp2.Route(r'/<invite_code:.*?>', handler=Main, name="invite")
]);
