from flask import Blueprint, request
from api.utils.responses import response_with
from api.utils import responses as resp
from api.models.books import Book, BookSchema
from api.models.authors import Author
from api.utils.database import db
from datetime import datetime,timezone
from sqlalchemy.orm.exc import StaleDataError
import logging

logger = logging.getLogger(__name__)
book_routes = Blueprint("book_routes", __name__)

@book_routes.route("/", methods = ['POST'])
def create_book():
  try:
    data = request.get_json()
    
    #TODO: Move this into middleware soon
    author_id = data.get('author_id')
    if not author_id:
      return response_with(resp.BAD_REQUEST_400, message="author_id is required")
    
     #TODO: Move this into middleware soon
    author = db.session.get(Author, author_id)
    if not author:
      return response_with(
        resp.SERVER_ERROR_404,
        message=f"Author with id {author_id} not found"
      )

    book_schema = BookSchema()
    book = book_schema.load(data)
    result = book_schema.dump(book.create())

    return response_with(
      resp.SUCCESS_201,
      value={"book": result}
    )
  except Exception as e:
    logger.error(f"Error while creating book: {str(e)}")
    return response_with(resp.INVALID_INPUT_422)
  
@book_routes.route("/", methods = ['GET'])
def get_all_books():
  books = Book.query.all()
  book_schema = BookSchema(many=True)

  result = book_schema.dump(books)
  return response_with(
    resp.SUCCESS_200,
    value={"books": result}
  )
  

@book_routes.route("/<int:id>", methods = ["GET"])
def get_book_by_id(id):
  try:
    # book = Book.query.get_or_404(id)
    book = db.session.get(Book, id)
    if not book:
      return response_with(
        resp.SERVER_ERROR_404,
        message=f"Book with id {id} not found!"
        )
    
    book_schema = BookSchema()
    result = book_schema.dump(book)

    return response_with(resp.SUCCESS_200, value={"book": result})
  
  except Exception as e:
    logger.error(f"Error while creating book: {str(e)}")
    return response_with(resp.SERVER_ERROR_500)
  
@book_routes.route("/<int:book_id>", methods = ['PUT'])
def update_book_by_id(book_id):
  try:
    data= request.get_json()
    if not data:
      return response_with(
        resp.BAD_REQUEST_400,
        message="No input provided"
      )
  
    book = db.session.query(Book).with_for_update().get(book_id)
    if not book:
      return response_with(
        resp.SERVER_ERROR_404,
        message=f"Book with id {book_id} not found"
      )
    
    try:
      book_schema = BookSchema(partial=True)
      updated_book = book_schema.load(data, instance=book)
      updated_book.updated_at = datetime.now(timezone)

      db.session.add(updated_book)
      db.session.commit()

      result = book_schema.dump(updated_book)
      return response_with(
        resp.SUCCESS_200,
        value={"author": result},
        message="Author updated successfuly"
      )
    
    except StaleDataError:
      db.session.rollback()
      return response_with(
        resp.INVALID_INPUT_422,
        message="Data was updated by another user. Please refresh and try again"
      )
    except Exception as e:
      db.session.rollback()
      raise e
    
  except Exception as e:
    logger.error(f"Error while updating book")
    return response_with(resp.INVALID_INPUT_422)
