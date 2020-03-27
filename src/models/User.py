from marshmallow import fields, Schema
import datetime
from . import db
from . import bcrypt
from .Need import NeedySchema

class UserModel(db.Model):
  """
  User Model
  """

  # table name
  __tablename__ = 'users'
  

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(128), nullable=True)
  phone_number=db.Column(db.String(128),  unique=True, nullable=False)
  password = db.Column(db.String(128), nullable=True)
  pin=db.Column(db.String(128),nullable=True)
  created_at = db.Column(db.DateTime)
  modified_at = db.Column(db.DateTime)
  #needys = db.relationship('NeedyModel', backref='users', lazy=True)

  # class constructor
  def __init__(self, data):
    """
    Class constructor
    """
    self.phone_number = data.get('phone_number')
    self.pin = data.get('pin')
    if 'password' in data.keys():
        self.password = self.__generate_hash(data.get('password'))
    self.created_at = datetime.datetime.utcnow()
    self.modified_at = datetime.datetime.utcnow()

  def save(self):
    db.session.add(self)
    db.session.commit()


  def update(self, data):
    for key, item in data.items():
        if key == 'password': 
            self.password = self.__generate_hash(item)
        setattr(self, key, item)
    self.modified_at = datetime.datetime.utcnow()
    db.session.commit()


  def delete(self):
    db.session.delete(self)
    db.session.commit()


  def __generate_hash(self, password):
    return bcrypt.generate_password_hash(password, rounds=10).decode("utf-8")
  

  def check_hash(self, password):
    return bcrypt.check_password_hash(self.password, password)
  
  def check_pin(self,pin):
    return (str(pin) == self.pin)


  @staticmethod
  def get_user_by_phone_number(pn):
    return UserModel.query.filter_by(phone_number=pn).first()

  @staticmethod
  def get_all_users():
    return UserModel.query.all()

  @staticmethod
  def get_one_user(id):
    return UserModel.query.get(id)

  
  def __repr(self):
    return '<id {}>'.format(self.id)



class UserSchema(Schema):
  """
  User Schema
  """
  id = fields.Int(required=False, dump_only=True)
  name = fields.Str(required=False)
  phone_number = fields.Str(required=True)
  password = fields.Str(required=False)
  pin = fields.Str(required=False)
  created_at = fields.DateTime(required=False, dump_only=True)
  modified_at = fields.DateTime(required=False, dump_only=True)
  #needys = fields.Nested(NeedySchema,required=False, many=True)