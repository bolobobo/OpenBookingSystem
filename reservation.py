'''This is the model class of a reservation. It can be created and deleted.
The data is stored in google datastore'''

from google.appengine.ext import ndb
from resource import Resource

class Reservation(ndb.Model):
    pass