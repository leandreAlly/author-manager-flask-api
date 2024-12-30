from api.utils.database import db
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
from datetime import datetime,timezone
from sqlalchemy.orm import validates
from api.models.books import BookSchema

class Author(db.Model):
  __tablename__ = 'authors'

  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  first_name = db.Column(db.String(20))
  last_name = db.Column(db.String(20), nullable=False)
  avatar = db.Column(db.String(100), nullable=True)
  created_at = db.Column(db.DateTime,  default=lambda: datetime.now(timezone.utc)) 
  updated_at = db.Column(db.DateTime,  default=lambda: datetime.now(timezone.utc))
  
  books = db.relationship('Book', backref='Author', cascade="all, delete-orphan")

  @validates("first_name", "last_name")
  def validate_name(self, key, name):
    if not name or not name.strip():
      raise ValueError(f"{key} cannot be empty")
    if len(name) > 20:
      raise ValueError(f"{key} cannot be longer than 20 characters")
    return name.strip()

  def __repr__(self):
    return f'<Author {self.first_name}'
  
  def create(self):
    db.session.add(self)
    db.session.commit()
    return self
  
  def update(self):
    self.updated_at = datetime.now(timezone.utc)
    db.session.commit()
    return self
  
  def delete(self):
    db.session.delete(self)
    db.session.commit()
    return self
  
class AuthorSchema(SQLAlchemyAutoSchema):
  class Meta:
    model = Author 
    sqla_session = db.session
    load_instance = True
    include_relationships = True
    include_fk = True

  id = fields.Number(dump_only=True)
  first_name = fields.String(required=True)
  last_name = fields.String(required=True)
  avatar = fields.String(dump_only=True)
  created_at = fields.DateTime(dump_only=True)
  updated_at = fields.DateTime(dump_only=True)
  books = fields.Nested('BookSchema', many=True, exclude=('author_id',))

