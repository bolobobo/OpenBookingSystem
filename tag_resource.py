'''This is the model class of resource tags.
It is used to group several resources with the same tag.
The data is stored in google datastore'''

from google.appengine.ext import ndb

class TagResource(ndb.Model):
    '''assign each resource into specific tag group
    parent = tag content
    key = resource_id + parent
    resource_id = the unique id of each resource'''
    resource_id = ndb.GenericProperty()

    @classmethod
    def create_tag_resource(cls, resource_id, parent_key):
        '''create a tag_resource, the key is the combination of tag and resource id'''
        res = TagResource(resource_id=resource_id, parent=parent_key)
        res.put()

    @classmethod
    def delete_tag_resource(cls, resource_id, parent_key):
        '''delete a entity if a resource do not belong to a tag anymore'''
        res_key = ndb.Key(resource_id, parent=parent_key)
        res_key.delete()

    @classmethod
    def get_resource_group(cls, ancestor_key):
        '''the ancestor key is ndb.Key("Tags", tag), return list of tag_resource entity for given ancestor key'''
        # todo: order by resource counts: cls.query(ancestor=ancestor_key).order(-cls.date)
        #ancestor_key = ndb.Key('Tags', tag)
        # return the Query object
        entities = cls.query(ancestor=ancestor_key).fetch()
        resources = []
        for e in entities:
            resources.append(ndb.Key("Resource", e.resource_id).get())
        return resources

