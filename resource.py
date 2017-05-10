'''This is the model class of a resource.It can be created, edited, reserved and deleted.
The data is stored in google datastore'''

from google.appengine.ext import ndb
import datetime

class Resource(ndb.Model):
    '''Models an individual resource entry with several attributes.
    owner id and resource name can not be empty.'''
    res_id = ndb.IntegerProperty()
    owner_id = ndb.IntegerProperty()
    res_name = ndb.StringProperty()
    res_start_time = ndb.DateTimeProperty()
    res_end_time = ndb.DateTimeProperty()
    res_tags = ndb.StringProperty(repeated=True)
    #email = ndb.StringProperty()

    @classmethod
    def update_resource(cls, res_id):
        '''edit the resource attributes'''
        pass


# def main():
#     resource = Resource(owner_id=66, res_name='canteen nyu', res_start_time=datetime.time(hour=9), res_end_time=datetime.time(hour=18))
#     print resource.put()

# if __name__ == '__main__':
#     main()
