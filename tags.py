'''This is the model class of resource tags.
It is used to group several resources with the same tag.
The data is stored in google datastore'''

from google.appengine.ext import ndb

class Tags(ndb.Model):
    '''Tags Model: id = tag content, count = the amount of resources has this tag'''
    count = ndb.IntegerProperty()

    @classmethod
    def create_tag(cls, key):
        '''create a tag entity in Tags and accumulate its counts'''
        tag = cls.get_by_id(key)
        if tag:
            tag.count = tag.count + 1
        else:
            tag = Tags(id=key, count=1)
        tag.put()

    @classmethod
    def decrease_tag_count(cls, key):
        '''when a resource do not belong to one tag, it should decrease the count'''
        tag = cls.get_by_id(key)
        if tag.count == 1:
            tag.key.delete()
        else:
            tag.count = tag.count - 1
            tag.put()

    @classmethod
    def get_top_tags(cls, top):
        '''get top tags which have most resource, return list of tag entity'''
        return cls.query().order(-cls.count).fetch(top)


