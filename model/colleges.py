from random import randrange
from datetime import date
import os, base64
import json

from __init__ import app, db
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash

#This material was based on a template provided by our teacher.
class College(db.Model):
    __tablename__ = 'colleges'  # table name is plural, class name is singular

    # Define the Player schema with "vars" from object
    id = db.Column(db.Integer, primary_key=True)
    _name = db.Column(db.String(255), unique=False, nullable=True)
    _link = db.Column(db.String(255), unique=False, nullable=True)
    _image = db.Column(db.String(255), unique=False, nullable=True)
    
    def __init__(self, name, link, image):
        self._name = name    # variables with self prefix become part of the object, 
        self._link = link
        self._image = image

    # a name getter method, extracts name from object
    @property
    def name(self):
        return self._name
    
    # a setter function, allows name to be updated after initial object creation
    @name.setter
    def name(self, name):
        self._name = name
    
    @property
    def link(self):
        return self._link
    
    @link.setter
    def link(self, link):
        self._link = link
        
    @property
    def image(self):
        return self._image
    
    @image.setter
    def image(self, image):
        self._image = image
    
    # output content using str(object) in human readable form, uses getter
    # output content using json dumps, this is ready for API response
    def __str__(self):
        return json.dumps(self.read())

    # CRUD create/add a new record to the table
    # returns self or None on error
    def create(self):
        try:
            # creates a player object from Player(db.Model) class, passes initializers
            db.session.add(self)  # add prepares to persist person object to Users table
            db.session.commit()  # SqlAlchemy "unit of work pattern" requires a manual commit
            return self
        except IntegrityError:
            db.session.remove()
            return None

    # CRUD read converts self to dictionary
    # returns dictionary
    def read(self):
        return {
            "id": self.id,
            "name": self.name,
            "link": self.link,
            "image": self.image
        }

    # CRUD update: updates name, uid, password, tokens
    # returns self
    def update(self, dictionary):
        """only updates values in dictionary with length"""
        for key in dictionary:
            if key == "name":
                self.name = dictionary[key]
            if key == "link":
                self.link = dictionary[key]
            if key == "image":
                self.image = dictionary[key]
        db.session.commit()
        return self

    # return self
    def delete(self):
        colleges = self
        db.session.delete(self)
        db.session.commit()
        return colleges

"""Database Creation and Testing """
# Builds working data for testing
def initColleges():
    with app.app_context():
        db.create_all()
        c1 = College(name='Stanford University',link='https://admission.stanford.edu/apply/',image='https://identity.stanford.edu/wp-content/uploads/sites/3/2020/07/block-s-right.png')
        c2 = College(name='Harvard University',link='https://college.harvard.edu/admissions/apply',image='https://1000logos.net/wp-content/uploads/2017/02/Harvard-Logo.png')
        c3 = College(name='MIT',link='https://apply.mitadmissions.org/portal/apply',image='https://upload.wikimedia.org/wikipedia/commons/thumb/0/0c/MIT_logo.svg/2560px-MIT_logo.svg.png')
        c4 = College(name='Georgia Tech',link='https://admission.gatech.edu/apply/',image='https://brand.gatech.edu/sites/default/files/inline-images/GTVertical_RGB.png')
        c5 = College(name='Duke University',link='https://admissions.duke.edu/apply/',image='https://upload.wikimedia.org/wikipedia/commons/thumb/0/04/Duke_Blue_Devils_logo.svg/909px-Duke_Blue_Devils_logo.svg.png')
        c6 = College(name='Yale University',link='https://www.yale.edu/admissions',image='https://upload.wikimedia.org/wikipedia/commons/thumb/6/6e/Yale_University_logo.svg/2560px-Yale_University_logo.svg.png')
        c7 = College(name='Princeton University',link='https://admission.princeton.edu/apply',image='https://upload.wikimedia.org/wikipedia/commons/thumb/d/d0/Princeton_seal.svg/1200px-Princeton_seal.svg.png')
        c8 = College(name='Columbia University',link='https://undergrad.admissions.columbia.edu/apply',image='https://admissions.ucr.edu/sites/default/files/styles/form_preview/public/2020-07/ucr-education-logo-columbia-university.png?itok=-0FD6Ma2')
        c9 = College(name='University of Chicago',link='https://collegeadmissions.uchicago.edu/apply',image='https://upload.wikimedia.org/wikipedia/commons/c/cd/University_of_Chicago_Coat_of_arms.png')
        c10 = College(name='UC Berkeley',link='https://admissions.berkeley.edu/apply-to-berkeley/',image='https://upload.wikimedia.org/wikipedia/commons/thumb/a/a1/Seal_of_University_of_California%2C_Berkeley.svg/1200px-Seal_of_University_of_California%2C_Berkeley.svg.png')
        c11 = College(name='UCLA',link='https://admission.ucla.edu/apply',image='https://upload.wikimedia.org/wikipedia/commons/thumb/d/d1/UCLA_Bruins_primary_logo.svg/1200px-UCLA_Bruins_primary_logo.svg.png')
        #Add new data to this line
        colleges = [c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11]
        """Builds sample user/note(s) data"""
        for college in colleges:
            try:
                '''add user to table'''
                object = college.create()
                print(f"Created new uid {object.id}")
            except:  # error raised if object nit created
                '''fails with bad or duplicate data'''
                print(f"Records exist uid {college.id}, or error.")