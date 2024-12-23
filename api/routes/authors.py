from flask import Blueprint, request, current_app
from api.utils.responses import response_with
from api.utils import responses as resp
from api.models.authors import Author, AuthorSchema
from api.utils.database import db
import logging
from sqlalchemy.orm.exc import StaleDataError
from datetime import datetime, timezone

logger = logging.getLogger(__name__)
author_routes = Blueprint("author_routes", __name__)

@author_routes.route("/", methods = ['POST'])
def create_author():
  try:
    data = request.get_json()
    if not data:
       response_with(resp.BAD_REQUEST_400)
    
    author_schema = AuthorSchema()
    author = author_schema.load(data)
    result = author_schema.dump(author.create())

    return response_with(
      resp.SUCCESS_201, 
      value={"author":result}
      )

  except Exception as e:
    print(e)
    return response_with(resp.INVALID_INPUT_422)

@author_routes.route("/", methods = ['GET'])
def get_all_authors():
  try:
    authors = Author.query.all()
    author_schema = AuthorSchema(many=True)

    result = author_schema.dump(authors)

    return response_with(resp.SUCCESS_200, value={"authors": result})
  
  except Exception as e:
    logger.error(f"Error fetching authors: {str(e)}")
    return response_with(resp.SERVER_ERROR_500)

@author_routes.route("/<int:author_id>", methods = ['GET'])
def get_author_by_id(author_id):
  try:
    author = db.session.get(Author, author_id)
    if not author:
      return response_with(resp.SERVER_ERROR_404)
    author_schema = AuthorSchema()

    result = author_schema.dump(author)

    return response_with(resp.SUCCESS_200, value={"author": result})
  
  except Exception as e:
    logger.error(f"Error fetching author: {str(e)}")
    return response_with(resp.SERVER_ERROR_500)
  
@author_routes.route("/<int:author_id>", methods = ['PUT'])
def update_author_by_id(author_id):
  try:
      data = request.get_json()
      if not data:
        return response_with(
          resp.BAD_REQUEST_400,
          message="No input provided"
        )
      
      author = db.session.query(Author).with_for_update().get(author_id)
      if not author:
        return response_with(
          resp.SERVER_ERROR_404,
          message=f"Author with id {author_id} not found"
        )
      
      
      try:
        author_schema = AuthorSchema(partial=True)
        updated_author = author_schema.load(data, instance=author)
        updated_author.updated_at = datetime.now(timezone.utc)

        db.session.add(updated_author)
        db.session.commit()

        current_app.logger.info(
            f"Author {author_id} updated by user at {datetime.now(timezone.utc)}"
        )

        result = author_schema.dump(updated_author)
        return response_with(
          resp.SUCCESS_200,
          value={"author": result},
          message="Author updated successfully"
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
    current_app.logger.error(f"Error updating author {author_id}: {str(e)}")
    return response_with(resp.INVALID_INPUT_422)

@author_routes.route("/<int:author_id>", methods = ['DELETE'])
def delete_author_by_id(author_id):
  try:
    with db.session.begin():
      author = db.session.query(Author)\
                     .with_for_update()\
                     .get(author_id)
      
      if not author:
        return response_with(
          resp.SERVER_ERROR_404,
          message=f"Author with id {author_id} not found"
        )
      
      if author.books:
        return response_with(
          resp.BAD_REQUEST_400,
          message="Cannot delete author with existing books"
        )
      
      try:
        db.session.delete(author)

        current_app.logger.info(
          f"Author {author_id} deleted by user at {datetime.now(timezone.utc)}"
        )

        return response_with(
          resp.SUCCESS_204,
          message="Author deleted successfully"
        )
      
      except Exception as e:
        db.session.rollback(),
        current_app.logger.error(
          f"Failed to delete author {author_id}: {str(e)}"
        )
        raise e

  except Exception as e:
    logger.error(f"Error deleting author: {str(e)}")
    return response_with(resp.SERVER_ERROR_500)