from api.utils.database import db
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
from datetime import datetime,timezone

class Book(db.Model):
  __tablename__ = 'books'

  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  title = db.Column(db.String(50), nullable=False)
  year = db.Column(db.Integer, nullable=False)
  author_id = db.Column(db.Integer, db.ForeignKey("authors.id"))
  created_at = db.Column(db.DateTime,  default=lambda: datetime.now(timezone.utc))
  updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

  # author = db.relationship("Author", back_populates="Book")

  def __repr__(self):
    return f'<Book {self.title}'
  
  def create(self):
    db.session.add(self)
    db.session.commit()
    return self
  
  def update(self):
    db.session.commit()
    return self
  
  def delete(self):
    db.session.delete(self)
    db.session.commit()
    return self
  
class BookSchema(SQLAlchemyAutoSchema):
  class Meta:
    model = Book
    sqla_session = db.session
    load_instance = True
    include_relationships = True
    include_fk = True

  id = fields.Number(dump_only=True)
  title = fields.String(required=True)
  year = fields.Integer(required=True)
  author_id = fields.Integer(required=True)
  created_at = fields.DateTime(dump_only=True)
  updated_at = fields.DateTime(dump_only=True)