from marshmallow import fields, Schema
from ..app import db
import datetime
from .Need import NeedySchema
from .User import UserSchema

class DonationModel(db.Model):
  """
  Donation Model
  """

  __tablename__ = 'donation'

  id = db.Column(db.Integer, primary_key=True)
  doner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
  item = db.Column(db.String(128))
  quantity = db.Column(db.String(128))
  needy_id = db.Column(db.Integer, db.ForeignKey('needy.id'), nullable=False)
  created_at = db.Column(db.DateTime)
  modified_at = db.Column(db.DateTime)

  def __init__(self, data):
    self.doner_id = data.get('doner_id')
    self.item = data.get('item')
    self.quantity = data.get('quantity')
    self.needy_id=data.get('needy_id')
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
  def get_all_Donations():
    return DonationModel.query.all()
  
  @staticmethod
  def get_one_Donation(id):
    return DonationModel.query.get(id)

  @staticmethod
  def get_one_needys_Donation(nid):
    return DonationModel.query.filter_by(needy_id=nid).all()

  def __repr__(self):
    return '<id {}>'.format(self.id)


class DonationSchema(Schema):
  """
  Donation Schema
  """
  id = fields.Int(dump_only=True)
  doner_id = fields.Int(required=True)
  item = fields.Str(required=True)
  quantity = fields.Str(required=True)
  needy_id = fields.Int(required=True)
  created_at = fields.DateTime(dump_only=True)
  modified_at = fields.DateTime(dump_only=True)