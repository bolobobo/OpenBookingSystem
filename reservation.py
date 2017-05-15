'''This is the model class of a reservation. 
It can be created and deleted.
The data is stored in google datastore'''

from google.appengine.ext import ndb
from resource import Resource
from datetime import datetime

class Reservation(ndb.Model):
    '''model class of reservation, key is auto'''
    resource_id = ndb.GenericProperty()
    user_id = ndb.StringProperty()
    date = ndb.DateProperty()
    start_time = ndb.DateTimeProperty()
    end_time = ndb.DateTimeProperty()
    valid = ndb.BooleanProperty()
    resource_name = ndb.StringProperty()

    @classmethod
    def create_reservation(cls, resource_id, user_id, date, start_time, end_time,resource_name):
        # if not cls.is_available(resource_id, date, start_time, end_time):
        #     return False
        rev = Reservation(resource_id=resource_id, user_id=user_id, date=date, start_time= start_time, end_time=end_time, valid=True,resource_name=resource_name)
        rev.put()
        Resource.update_reserve_time(resource_id, datetime.now())

    @classmethod
    def is_available(cls, resource_id, date, start_time, end_time):
        resource = Resource.get_by_id(resource_id)
        print resource
        res_start = resource.start_time
        res_start = res_start.hour + res_start.minute/60.0
        res_end = resource.end_time
        res_end = res_end.hour + res_end.minute/60.0
        existed_rev = cls.query(cls.resource_id == resource_id, cls.date == date).fetch()
        print existed_rev

        start_time = start_time.hour + start_time.minute/60.0
        end_time = end_time.hour + end_time.minute/60.0

        if start_time < res_start or end_time > res_end:
            return False
        times = []
        times.append([res_start, res_start])
        times.append([res_end, res_end])
        times.append([start_time, end_time])

        for e in existed_rev:
            times.append([e.start_time.hour + e.start_time.minute/60.0, e.end_time.hour + e.end_time.minute/60.0])

        times.sort()

        for i in range(len(times) - 1):
            if times[i][1] > times[i+1][0]:
                return False
        return True

    @classmethod
    def delete_reservation(cls, reservation_id):
        rev_key = ndb.Key("Reservation", reservation_id)
        rev_key.delete()

    @classmethod
    def detect_reservation_expired(cls, reservation_id):
        rev_key = ndb.Key("Reservation", reservation_id)
        rev = rev_key.get()
        rev.valid = False
        rev.put()

    @classmethod
    def get_reservations_for_user(cls, user_id):
        '''get the valid reservation for user, update the expired reservation'''
        reservations = cls.query(cls.user_id == user_id, cls.end_time < datetime.now(), cls.valid == True).fetch()
        for r in reservations:
            r.valid = False
            r.put()
        # reservations = cls.query(cls.user_id == user_id).fetch()
        # current_time = datetime.now()
        # for r in reservations:
        #     if r.end_time < current_time:
        #         r.valid = False
        #         r.put()
        return cls.query(cls.user_id == user_id, cls.start_time > datetime.now(), cls.valid == True).fetch()

    @classmethod
    def get_reservations_for_resource(cls, resource_id):
        '''get reservation for resource'''
        return cls.query(cls.resource_id == resource_id).fetch()

    @classmethod
    def get_user_id(cls, reservation_id):
        '''get reservation for resource'''
        return Resource.get_by_id(reservation_id)
