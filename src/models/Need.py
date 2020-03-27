from marshmallow import fields, Schema
from . import db
import datetime

class NeedyModel(db.Model):
  """
  Needy Model
  """

  __tablename__ = 'needy'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(128))
  cnic = db.Column(db.Text, unique=True, nullable=False)
  need = db.Column(db.Text)
  address = db.Column(db.Text)
  phone_number=db.Column(db.String(128))
  created_at = db.Column(db.DateTime)
  modified_at = db.Column(db.DateTime)

  def __init__(self, data):
    self.name = data.get('name')
    self.cnic = data.get('cnic')
    self.need = data.get('need')
    self.address= data.get('address')
    self.phone_number = data.get('phone_number') 
    self.created_at = datetime.datetime.utcnow()
    self.modified_at = datetime.datetime.utcnow()

  def save(self):
    db.session.add(self)
    db.session.commit()

  def update(self, data):
    for key, item in data.items():
      setattr(self, key, item)
    self.modified_at = datetime.datetime.utcnow()
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()
  
  @staticmethod
  def get_needy_by_cnic(cn):
    return NeedyModel.query.filter_by(cnic=cn).first()
    
    
  @staticmethod
  def get_all_needy():
    return NeedyModel.query.all()
  
  @staticmethod
  def get_one_needy(id):
    return NeedyModel.query.get(id)

  def __repr__(self):
    return '<id {}>'.format(self.id)

class NeedySchema(Schema):
  """
  Needy Schema
  """
  id = fields.Int(dump_only=True)
  name = fields.Str()
  cnic = fields.Str(required=True)
  need = fields.Str()
  address = fields.Str()
  phone_number=fields.Str()
  created_at = fields.DateTime(dump_only=True)
  modified_at = fields.DateTime(dump_only=True)