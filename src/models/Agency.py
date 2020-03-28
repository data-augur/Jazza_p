from marshmallow import fields, Schema
from ..app import db
import datetime

class AgencyModel(db.Model):
  """
  Agency Model
  """

  __tablename__ = 'agency'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(128), nullable=False)
  url = db.Column(db.String(256))
  logo_path = db.Column(db.String(256))
  description=db.Column(db.Text)
  created_at = db.Column(db.DateTime)
  modified_at = db.Column(db.DateTime)

  def __init__(self, data):
    self.name = data.get('name')
    self.url = data.get('url')
    self.logo_path = data.get('logo_path')
    self.description=data.get('description')
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
  def get_all_Agencies():
    return AgencyModel.query.all()
  
  @staticmethod
  def get_one_Donation(id):
    return AgencyModel.query.get(id)

  def __repr__(self):
    return '<id {}>'.format(self.id)


class AgencySchema(Schema):
  """
  Agency Schema
  """
  id = fields.Int(dump_only=True)
  name = fields.Str(required=True)
  url = fields.Str(required=True)
  logo_path = fields.Str()
  description = fields.Str()
  created_at = fields.DateTime(dump_only=True)
  modified_at = fields.DateTime(dump_only=True)