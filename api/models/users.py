from datetime import datetime, timezone
from api.utils.database import db
from passlib.hash import pbkdf2_sha256 as sha256
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields, validates, ValidationError
import re

class User(db.Model):
  __tablename__ = "users"
  

  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(50),unique=True, nullable=False)
  email = db.Column(db.String(120), unique=True, nullable=False)
  password = db.Column(db.String(255), nullable=False)
  is_active = db.Column(db.Boolean, default=True)
  created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
  updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
  last_login = db.Column(db.DateTime)

#TODO: Learn how to perform validations
  # @validates("email")
  # def validate_email(self, key, email):
  #   if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
  #     raise ValidationError('Invalid email address')
  #   return email
  
  # @validates("username")
  # def validate_username(self, key, username):
  #   if not 3 <= len(username) <= 50:
  #     raise ValidationError('Username must be between 3 and 50 characters')
  #   return username
  
  def create(self):
    db.session.add(self)
    db.session.commit()
    return self
  
  @classmethod
  def find_by_username(cls, username):
    return cls.query.filter_by(username = username, is_active=True).first()
  
  @classmethod
  def find_by_email(cls, email):
    return cls.query.filter_by(email=email, is_active=True).first()
  
  @staticmethod
  def generate_hash(password):
    return sha256.hash(password)
  
  @staticmethod
  def verify_hash(password, hash):
    return sha256.verify(password, hash)
  
  def update_last_login(self):
    self.last_login = datetime.now(timezone.utc)
    db.session.commit()

  def __repr__(self):
    return f'<User {self.username}'
  

class UserSchema(SQLAlchemyAutoSchema):
  class Meta:
    model = User
    sqla_session = db.session
    load_instance = True

  id = fields.Number(dump_only=True) 
  username = fields.String(required=True)
  email = fields.Email(required=True)
  password = fields.String(required=True, load_only=True)
  is_active = fields.Boolean(dump_only=True)
  created_at = fields.DateTime(dump_only=True)
  updated_at = fields.DateTime(dump_only=True)
  last_login = fields.DateTime(dump_only=True)

