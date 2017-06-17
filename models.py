from google.appengine.ext import ndb

class Invite(ndb.Model):
    code = ndb.StringProperty()
    name = ndb.StringProperty()
    email = ndb.StringProperty()
    guest = ndb.IntegerProperty(indexed=False, default=0)
    accepted = ndb.BooleanProperty()
    viewed = ndb.IntegerProperty(indexed=False, default=0)
    last_viewed = ndb.DateTimeProperty()
