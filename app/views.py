"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""

from app import app,db#login_manager
from flask import render_template, request, redirect, url_for,flash,jsonify,session,json,abort
from flask_login import login_user,logout_user,current_user,login_required
from bs4 import BeautifulSoup
from models import UserProfile
import requests
import urlparse
from send_email import send_email
from sqlalchemy import exc

url=""
uid=""
gname=""
###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')

@app.route('/api/users/register',methods=['POST','GET'])
def register():
    """Render website's registration page."""
    if request.method == 'POST':
        fname=request.form.get('firstname')
        lname=request.form.get('lastname') 
        email=request.form.get('E-mail') 
        password=request.form.get('password')
        cpassword=request.form.get('cpassword')
        user =UserProfile(first_name=fname,last_name=lname,
        email=email,password=password,cpassword=cpassword)
        db.session.add(user)
        db.session.commit()
    return render_template('register.html')
    
@app.route('/api/users/login',methods=['POST','GET'])
def login():
    """Render website's login page."""
    global uid
    if request.method == 'POST':
        input_email=request.form.get('E-mail') 
        password=request.form.get('password')
        query='SELECT id,first_name, last_name, email,password,cpassword FROM user_profile;'
        entries=db.session.execute(query)
        for entry in entries:
            user=UserProfile(id=entry[0],first_name=entry[1],last_name=entry[2],email=entry[3],
            password=entry[4],cpassword=entry[5])
            if input_email== user.email and  password ==user.password:
                session['logged_in'] = True #login_user(user)
                uid=user.get_id()
                flash('You are logged in')
                return redirect(url_for('user_wishlist',userid=uid))#"login succesful ".join(user.get_id())
        return "invalid credentials"
    return render_template('login.html')
    
@app.route('/api/users/<userid>/wishlist',methods=['POST','GET'])
def user_wishlist(userid):
    """Render website's wishlist page for specified user."""
    if not session.get('logged_in'):
        abort(401)
    global url
    global gname
    query="SELECT first_name FROM user_profile WHERE id ={0};".format(userid)
    name =db.session.execute(query).first()
    uname =[str(uname) for uname in name]
    gname= uname
    url=request.form.get("WishURL")
    
    return render_template('user_wishlist.html',name=uname[0])

@app.route('/share_wish',methods=['POST','GET'])
def share():
    global gname
    global uid
    """Render website's form to share user's wishlist with friends."""
    userid =uid
    from_name=gname[0]
    to_name=""
    if request.method == 'POST':
        to_email =request.form['f_emaiL']
        query="SELECT first_name,last_name FROM user_profile WHERE email ='{0}';".format(to_email)
        fullname =db.session.execute(query).first()
        if fullname is not None:
            for name in fullname:
                to_name+=name+" "
        else:
            to_name="Hello friend"
        query="SELECT email FROM user_profile WHERE id ={0};".format(userid)
        from_email=db.session.execute(query).first()
        if from_email is not None:
            from_email="""From: {} <{}>
            """.format(from_name,from_email[0])
            subject="{0}{1}'s wishlist".format(from_email,from_name)
        else:
            from_email="""From: {0} <{1}wishes@wishmail.com>
            """.format(from_name,from_name)
            subject="{0}{1}'s wishlist".format(from_email,from_name)
        msg="Wishes"
        if (send_email(to_name,to_email,from_name, from_email, subject, msg)==0):
            flash("Message Sent")
    return render_template('share_wish.html',name = gname[0])
      
@app.route('/api/thumbnails')
def url_json():
    global url
    if url is None:
        flash("Enter a valid url")
        return redirect(url_for("user_wishlist",userid=uid))
    else:
        result = requests.get(url)
        soup = BeautifulSoup(result.text, "html.parser")
        # This will look for a meta tag with the og:image property
        og_image = (soup.find('meta', property='og:image') or
                            soup.find('meta', attrs={'name': 'og:image'}))
        if og_image and og_image['content']:
            print og_image['content']
            print ''
        
        # This will look for a link tag with a rel attribute set to 'image_src'
        thumbnail_spec = soup.find('link', rel='image_src')
        if thumbnail_spec and thumbnail_spec['href']:
            print thumbnail_spec['href']
            print ''
        
        
        image = """<img src="%s"><br />"""
        img_list =[]
        for img in soup.findAll("img", src=True):
            img_list+= [str(url+img["src"])]
        results={"thumbnails": img_list}
        response =app.response_class(response=json.dumps(results),status=200, mimetype='application/json' )
        return response
    
@app.route('/api/users/{userid}/wishlist/{itemid}')
def delete_wish():
     """Render website's wishlist page to delete a user's wish."""
    # return render_template('user_wishlist.html',name=name,dwish=wishid)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('home'))

@app.route('/thumbnails/view')
def view_thumbnails():
    """Render website's thumbnail page."""
    return render_template('thumbnails.html',)

""" 
@login_manager.user_loader
def load_user(id):
    return UserProfile.query.get(int(id))"""
    
###
# The functions below should be applicable to all Flask apps.
###

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to tell the browser not to cache the rendered page.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port="8080")
