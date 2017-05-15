from flask import Flask, render_template, request
from resource import Resource
from google.appengine.ext import ndb
from google.appengine.api import users
from datetime import time, date
from tag_resource import TagResource
from tags import Tags
from datetime import datetime
from reservation import Reservation
import traceback

app = Flask(__name__)


@app.route('/layout')
def layout():
    user = users.get_current_user()
    if user:
        nickname = user.nickname()
        logout_url = users.create_logout_url('/layout')
        print user.user_id()
        print logout_url
        return render_template("layout.html", log_url=logout_url, log_status="Log Out")
    else:
        login_url = users.create_login_url('/layout')
        print login_url
        return render_template("layout.html", log_url=login_url, log_status="Sign In")

@app.route('/')
def index():
    user = users.get_current_user()
    if user:
        nickname = user.nickname()
        logout_url = users.create_logout_url('/')
        reservations = Reservation.get_reservations_for_user(user.user_id())
        resources = Resource.get_resources_for_owner(user.user_id())
        all_resources = Resource.get_all_resources()
        return render_template("index.html", log_url=logout_url, log_status="Log Out", login_flag=True, reservations=reservations, resources=resources, all_resources=all_resources)
    else:
        login_url = users.create_login_url('/')
        return render_template("index.html", log_url=login_url, log_status="Sign In", login_flag=False)
@app.route('/create')
def create_resource():
    user = users.get_current_user()
    if user:
        nickname = user.nickname()
        logout_url = users.create_logout_url('/create')
        print user.user_id()
        return render_template("create.html", log_url=logout_url, log_status="Log Out", login_flag=True, create_status=False)
    else:
        login_url = users.create_login_url('/create')
        return render_template("create.html", log_url=login_url, log_status="Sign In",login_flag=False, create_status=False)
    
@app.route('/created', methods=['POST'])
def created():
    try:
        user = users.get_current_user()
        if not user:
            login_url = users.create_login_url('/create')
            return render_template("create.html", login_url=login_url, log_status="Sign In")
        logout_url = users.create_logout_url('/')
        owner_id = user.user_id()
        name = request.form['name'].encode('ascii','ignore')
        start_time = time(int(request.form['start_hour']), int(request.form['start_minute']))
        end_time = time(int(request.form['end_hour']), int(request.form['end_minute']))
        tags = request.form['tags'].encode('ascii','ignore')
        if tags != "":
            tags = tags.split(";")
        tags = filter(lambda x: x != "" , tags)
        Resource.create_resource(owner_id=owner_id, name=name, start_time=start_time, end_time=end_time, tags=tags)
        return render_template("create.html", log_url=logout_url, log_status="Log Out", login_flag=True, create_status=True)
    except:
        print traceback.print_exc()

@app.route("/resource/<resource_id>")
def resource_exhibit(resource_id):
    return_url = "/resource/" + resource_id
    resource = Resource.get_resource(int(resource_id))
    reservations = Reservation.get_reservations_for_resource(int(resource_id))
    print reservations
    owner_id = resource.owner_id.encode('ascii','ignore')
    name = resource.name
    start_time = resource.start_time.strftime("%H:%M")
    end_time = resource.end_time.strftime("%H:%M")
    tags = resource.tags
    user = users.get_current_user()
    if user:
        nickname = user.nickname()
        logout_url = users.create_logout_url(return_url)
        if user.user_id() == owner_id:
            return render_template("resource.html", name=name, start_time=start_time, end_time=end_time, tags=tags,resource_id=resource_id, reservations=reservations, log_url=logout_url, log_status="Log Out", revop_status=False,owner_flag=True)
        return render_template("resource.html", name=name, start_time=start_time, end_time=end_time, tags=tags,resource_id=resource_id, reservations=reservations,  log_url=logout_url, log_status="Log Out", revop_status=False, owner_flag=False)
    else:
        login_url = users.create_login_url(return_url)
        return render_template("resource.html", name=name, start_time=start_time, end_time=end_time, tags=tags,resource_id=resource_id, reservations=reservations, log_url=login_url, log_status="Sign In")

@app.route("/reserved", methods=['POST'])
def reserved():
    user = users.get_current_user()
    resource_id = request.form['resource_id']
    resource_name = Resource.get_resource(int(resource_id)).name
    reservations = Reservation.get_reservations_for_resource(int(resource_id))

    # process the datetime
    reserve_start = request.form['reserve_start'].encode('ascii','ignore')
    reserve_start = datetime.strptime(reserve_start, '%Y-%m-%d %H:%M')
    reserve_end = request.form['reserve_end'].encode('ascii','ignore')
    reserve_end = datetime.strptime(reserve_end, '%Y-%m-%d %H:%M')
    start_date = date(reserve_start.year, reserve_start.month, reserve_start.day)
    end_date = date(reserve_end.year, reserve_end.month, reserve_end.day)
    return_url = "/resource/" + resource_id

    if user:
        nickname = user.nickname()
        logout_url = users.create_logout_url(return_url)
        if reserve_start > reserve_end or reserve_start < datetime.now():
            return render_template("resource.html", log_url=logout_url, log_status="Log Out", revop_status=True,invalid_rev_flag=True, reservations=reservations)
        if start_date != end_date:
            return render_template("resource.html", log_url=logout_url, log_status="Log Out", revop_status=True,over_day_flag=True, reservations=reservations)
        if Reservation.is_available(int(resource_id), start_date, reserve_start, reserve_end):
            Reservation.create_reservation(int(resource_id), user.user_id(), start_date, reserve_start, reserve_end,resource_name)
            return render_template("resource.html", log_url=logout_url, log_status="Log Out", revop_status=True, rev_success_flag=True, reservations=reservations)
            
        else:
            return render_template("resource.html", log_url=logout_url, log_status="Log Out", revop_status=True, rev_success_flag=False, reservations=reservations)
    else:
        login_url = users.create_login_url(return_url)
        print login_url
        return render_template("resource.html", log_url=login_url, log_status="Sign In", revop_status=True, reservations=reservations)

@app.route("/user")
def profile():
    user = users.get_current_user()
    if user:
        nickname = user.nickname()
        logout_url = users.create_logout_url('/user')
        reservations = Reservation.get_reservations_for_user(user.user_id())
        resources = Resource.get_resource(user.user_id())
        print resources
        return render_template("user.html", reservations=reservations, resources=resources, log_url=logout_url, log_status="Log Out",login_flag=True)
    else:
        login_url = users.create_login_url('/user')
        return render_template("user.html", reservations=reservations, resources=resources, log_url=login_url, log_status="Sign In",login_flag=False)

@app.route('/cancel/<reservation_id>')
def cancel_reservation(reservation_id):
    user_id = Reservation.get_user_id(int(reservation_id))
    user = users.get_current_user()

    if user:
        nickname = user.nickname()
        logout_url = users.create_logout_url('/')
        if user_id == user.user_id():
            Reservation.delete_reservation(int(reservation_id))
            return render_template("cancel.html", log_url=logout_url, log_status="Log Out",cancel_success=True)
        else:
            return render_template("cancel.html", log_url=logout_url, log_status="Log Out",cancel_success=False)
    else:
        login_url = users.create_login_url('/')
        return render_template("cancel.html", log_url=login_url, log_status="Sign In", cancel_success=False)


@app.route('/edit/<resource_id>')
def edit_resource(resource_id):
    res = Resource.get_resource(int(resource_id))
    return_url = "/edit/" + resource_id
    print "-------",resource_id
    owner_id = res.owner_id
    start_time = res.start_time
    end_time = res.end_time

    user = users.get_current_user()

    if user:
        nickname = user.nickname()
        logout_url = users.create_logout_url(return_url)
        if owner_id == user.user_id():
            return render_template("edit.html", resource_id=resource_id, origin_name=res.name, origin_start_hour=start_time.hour,origin_start_minute=start_time.minute, origin_end_hour=end_time.hour, origin_end_minute=end_time.minute, origin_tags=';'.join(res.tags), log_url=logout_url, log_status="Log Out")
        else:
            return render_template("edited.html", log_url=logout_url, log_status="Log Out")
    else:
        login_url = users.create_login_url(return_url)
        return render_template("edited.html", log_url=login_url, log_status="Sign In", cancel_success=False)

@app.route('/updated', methods=['POST'])
def updated():
    resource_id = request.form['resource_id']
    return_url = "/edit/" + resource_id
    
    user = users.get_current_user()
    if not user:
        login_url = users.create_login_url(return_url)
        return render_template("edit.html", login_url=login_url, log_status="Sign In")
   
    logout_url = users.create_logout_url(return_url)
    # owner_id = user.user_id()
    name = request.form['name'].encode('ascii','ignore')
    start_time = time(int(request.form['start_hour']), int(request.form['start_minute']))
    end_time = time(int(request.form['end_hour']), int(request.form['end_minute']))
    tags = request.form['tags'].encode('ascii','ignore')
    print tags
    if tags != "":
        tags = tags.split(";")
    # try:
    Resource.update_resource(int(resource_id), name, start_time, end_time, tags)
    # except:
    #     print traceback.print_exc()

    return render_template("edit.html", log_url=logout_url, log_status="Log Out", login_flag=True, edit_status=True) 

@app.route("/tag/<tag>")
def get_tag_resource(tag):
    res = TagResource.get_resource_group(ndb.Key('Tags', tag))
    user = users.get_current_user()
    return_url = "/tag/" + tag
    if user:
        nickname = user.nickname()
        logout_url = users.create_logout_url(return_url)
        return render_template("tag.html", log_url=logout_url, log_status="Log Out", all_resources=res)
    else:
        login_url = users.create_login_url(return_url)
        print login_url
        return render_template("tag.html", log_url=login_url, log_status="Sign In", all_resources=res)
    # return render_template("tag.html", all_resources=res)



@app.route('/rss/<resource_id>')
def generate_rss(resource_id):
    res = Resource.get_resource(int(resource_id))
    name = res.name
    print type(name)
    reservations = Reservation.get_reservations_for_resource(int(resource_id))
    return render_template("rss.xml", name=name, start_time=res.start_time,end_time=res.end_time,tags=';'.join(res.tags), resource_id=resource_id,reservations=reservations)

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
    
    # res_tags=[""]
    # res2 = Resource.create_resource(owner_id="899", name='bottle', start_time=time(6), end_time=time(19), tags=res_tags)
    # res2.put()
    return "hello"
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
    # l_r = Resource.query(Resource.owner_id == 399, Resource.name == "bottle").fetch()

    # print l_r[0].start_time.hour

    # ------------test query datetime
    # l_r = Resource.query(Resource.start_time.date == 1).fetch()

    # print l_r

    # ------------function: TagResource.create_tag_resource()

    # res = TagResource()
    # res.key = ndb.Key(999, parent=ndb.Key("Tags", "pineapple"))
    # res.resource_id=888888
    # key = res.put()
    # # result= TagResource.get_resource_group(ndb.Key("Tags", "apple"))
    # # print result
    # return "hello"
    

if __name__ == '__main__':
  app.run(debug=True)