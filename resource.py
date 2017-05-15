'''This is the model class of a resource.It can be created, edited, reserved and deleted.
The data is stored in google datastore'''

from datetime import time,datetime
from tags import Tags
from tag_resource import TagResource
from google.appengine.ext import ndb


class Resource(ndb.Model):
    '''Models an individual resource entry with several attributes.
    owner id and resource name can not be empty.'''
    #res_id = ndb.IntegerProperty()
    owner_id = ndb.StringProperty()
    name = ndb.StringProperty()
    start_time = ndb.TimeProperty()
    end_time = ndb.TimeProperty()
    tags = ndb.StringProperty(repeated=True)
    newest_rev = ndb.DateTimeProperty()
    #email = ndb.StringProperty()
    #res_count = ndb.IntegerProperty()
    #res_image =

    @classmethod
    def create_resource(cls, owner_id, name, start_time, end_time, tags):
        '''create resource and set the default value for attributes'''
        if start_time == "":
            start_time = time(0)
        if end_time == "":
            end_time = time(0)
        if len(tags) == 0:
            res = Resource(owner_id=owner_id, name=name, start_time=start_time, end_time=end_time, newest_rev=datetime.now())
        else:
            res = Resource(owner_id=owner_id, name=name, start_time=start_time, end_time=end_time, tags=tags, newest_rev=datetime.now())
        key = res.put()

        #create the entity for Tags and TagResource
        if len(tags) != 0:
            print "the length is", len(tags)
            print tags
            for t in tags:
                Tags.create_tag(t)
                TagResource.create_tag_resource(key.id(), parent_key=ndb.Key("Tags", t))

    @classmethod
    def update_resource(cls, res_id, name, start_time, end_time, tags):
        '''edit the resource attributes'''
        res = ndb.Key("Resource", res_id).get()
        origin_tags = res.tags

        
        # update
        res.name = name
        res.start_time = start_time
        res.end_time = end_time
        res.tags = tags
        if start_time == "":
            res.start_time = time(0)
        if end_time == "":
            res.end_time = time(0)
        key = res.put()

        # update Tags and TagResource
        tags = set(tags)
        origin_tags = set(origin_tags)
        insert_tags = tags - origin_tags
        delete_tags = origin_tags - tags

        # delete origin tags
        if len(delete_tags) != 0:
            for t in tags:
                Tags.decrease_tag_count(t)
                TagResource.delete_tag_resource(key.id(), parent_key=ndb.Key("Tags", t))

        # create new tags
        if len(insert_tags) != 0:
            for t in tags:
                Tags.create_tag(t)
                TagResource.create_tag_resource(key.id(), parent_key=ndb.Key("Tags", t))


    @classmethod
    def get_resource(cls, res_id):
        '''get the resource entity by resource unique id. '''
        res_key = ndb.Key("Resource", res_id)
        return res_key.get()

    @classmethod
    def get_available_time(cls, res_id):
        '''''get the available duration by resource unique id.'''
        res_key = ndb.Key("Resource", res_id)
        res = res_key.get()
        return res.start_time, res.end_time

    @classmethod
    def get_resources_for_owner(cls, user_id):
        return cls.query(cls.owner_id == user_id).fetch()

    @classmethod
    def get_all_resources(cls):
        return cls.query().order(-cls.newest_rev).fetch()

    @classmethod
    def update_reserve_time(cls, res_id, new_time):
        res_key = ndb.Key("Resource", res_id)
        res = res_key.get()
        if new_time > res.newest_rev:
            res.newest_rev = new_time
        res.put()
