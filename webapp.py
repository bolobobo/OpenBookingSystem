from flask import Flask, render_template, request
from resource import Resource
from google.appengine.ext import ndb
from google.appengine.api import users
from datetime import time
from tag_resource import TagResource
from tags import Tags

app = Flask(__name__)

@app.route('/')
def index():
    user = users.get_current_user()
    if user:
        nickname = user.nickname()
        logout_url = users.create_logout_url('/')
        print user.user_id()
        return render_template("logout.html", logout_url=logout_url)
    else:
        login_url = users.create_login_url('/')
        #return "hello login"
        return render_template("login.html", login_url=login_url)

@app.route('/test')
def test():
    # ------------basic:create Resource
    # res = Resource(owner_id=99, res_name='salad')
    # res = Resource(owner_id=89, name='table', start_time=time(9), end_time=time(18))
    # key = res.put()
    # print key
    # print key.id()

    # ------------test datetime
    # res1 = resource = Resource(owner_id=66, name='salad', start_time=datetime.datetime(2015, 1, 12, 23, 43, 23), end_time=datetime.datetime(2015, 1, 12, 23, 43, 23))

    # ------------function:create_resource
    # res_tags=["apple","pen","pineapple","pineapplepen"]
    # res2 = Resource.create_resource(owner_id=899, name='bottle', start_time=time(6), end_time=time(19), tags=res_tags)

    # ------------basic:fetch
    # key = Resource.query(Resource.owner_id == 66).fetch(3)
    # print key

    # ------------function: TagResource.get_resource_group | Tags.get_top_tags
    # print TagResource.get_resource_group(ndb.Key("Tags", "pen"))
    # print Tags.get_top_tags(2)
    # print Tags.get_top_tags(2)[1].key.id()

    # ------------function:get_resource(cls, res_id):
    # print Resource.get_resource(5047308127305728)

    # ------------function:get_available_time(cls, res_id), return datetime object
    # print Resource.get_available_time(5047308127305728)

    # ------------test time sort
    # resources = Resource.query().fetch()
    # print resources[1].start_time.hour
    # times = [] 
    # for e in resources:
    #     times.append([e.start_time.hour+e.start_time.minute/60.0, e.end_time.hour+e.end_time.minute/60.0])
    # times.sort()
    # print times

    # ------------test query and
    l_r = Resource.query(Resource.owner_id == 399, Resource.name == "bottle").fetch()

    print l_r[0].start_time.hour

    # ------------test query datetime
    # l_r = Resource.query(Resource.start_time.date == 1).fetch()

    # print l_r
    return "hello"


# @app.route("/create", method=['POST'])
# def create_resource():
#     name = request.form['name']
#     # todo: user system
#     owner_id = request.form['owner_id']
#     start_time = request.form['start_time']
#     end_time = request.form['end_time']
#     tags = request.form['tags']
#     if tags != "":
#         tags = tags.split(" ")
#     Resource.create_resource(owner_id=owner_id, name=name, start_time=start_time, end_time=end_time, tags=tags)


# @app.route("/res/edit")
# def edit_resource():
#     pass

if __name__ == '__main__':
  app.run(debug=True)