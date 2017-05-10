from google.appengine.ext import ndb

class Tag(ndb.Model):
    resource_id = ndb.IntegerProperty()

    @classmethod
    def query_resource_group(cls, ancestor_key):
        # todo: order by resource counts: cls.query(ancestor=ancestor_key).order(-cls.date)
        return cls.query(ancestor=ancestor_key)