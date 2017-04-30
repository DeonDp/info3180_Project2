from . import db

class UserProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    email = db.Column(db.String(255))
    password = db.Column(db.String(255))
    cpassword = db.Column(db.String(255))
    
    def is_authenticated(self):
        return True
    
    def is_active(self):
        return True
    
    def is_anonymous(self):
        return False
    
    def get_id(self):
        try:
            return unicode(self.id)  # python 2 support
        except NameError:
            return str(self.id)  # python 3 support
    
    def __repr__(self):
        return '<User %r>' % (self.email)

    
class WishItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    wish_title = db.Column(db.String(80))
    wish_des = db.Column(db.String(80))
    UserProfile_id = db.Column(db.Integer, db.ForeignKey(UserProfile.id))
    wish_link = db.Column(db.String(255))
    image=db.Column(db.LargeBinary)
        
  
