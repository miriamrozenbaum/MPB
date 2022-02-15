from logging import exception
from src.constants.http_status_codes import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND, HTTP_409_CONFLICT, HTTP_500_INTERNAL_SERVER_ERROR
from flask import Blueprint, request
from flask.json import jsonify
import validators
from flask_jwt_extended import get_jwt_identity, jwt_required
from src.database import  Like, Post, db
from flasgger import swag_from

posts = Blueprint("posts", __name__, url_prefix="/api/posts")

@posts.get('/')
@jwt_required()
#@swag_from("./docs/blog/posts.yaml")
def get_posts():
    current_user = get_jwt_identity()

    posts = Post.query.all()

    data = []

    for post in posts:
        data.append({
            'id': post.id,
            'titel': post.titel,
            'description': post.description,
            'likes': post.likes,
            'created_at': post.created_at,
            'updated_at': post.updated_at,
            'user_id' : post.user_id,
        })


    return jsonify({'data': data}), HTTP_200_OK

@posts.post('/')
@jwt_required()
#@swag_from("./docs/blog/modify_post.yaml")
def add_post():

    try:
        current_user = get_jwt_identity()

        description = request.get_json().get('description', '').strip()
        titel = request.get_json().get('titel', '').strip()


        if not validators.length(titel, min=1, max=50):
            return jsonify({
                'error': 'Post titel is too long or empty'
            }), HTTP_400_BAD_REQUEST

        if not validators.length(description, min=1, max=1000):
            return jsonify({
                'error': 'Post description is too long or empty'
            }), HTTP_400_BAD_REQUEST

        if Post.query.filter_by(titel=titel).first():
            return jsonify({
                'error': 'Post titel already exists'
            }), HTTP_409_CONFLICT

        post = Post(titel=titel, description=description, user_id=current_user)
        db.session.add(post)
        db.session.commit()

        return jsonify({
            'id': post.id,
            'titel': post.titel,
            'likes': post.likes,
            'desciption': post.description,
            'created_at': post.created_at,
            'updated_at': post.updated_at,
        }), HTTP_201_CREATED

    except exception as e:
        return jsonify({
                    'error': "Internal Error"
                }), HTTP_500_INTERNAL_SERVER_ERROR



@posts.get("/<int:id>")
@jwt_required()
#@swag_from("./docs/blog/posts.yaml")
def get_post(id):

    try:
        current_user = get_jwt_identity()

        post = Post.query.filter_by(user_id=current_user, id=id).first()

        if not post:
            return jsonify({'message': 'Item not found'}), HTTP_404_NOT_FOUND

        return jsonify({
            'id': post.id,
            'titel': post.titel,
            'description': post.description,
            'likes': post.likes,
            'created_at': post.created_at,
            'updated_at': post.updated_at,
        }), HTTP_200_OK

    except exception as e:
        return jsonify({
                    'error': "Internal Error"
                }), HTTP_500_INTERNAL_SERVER_ERROR


@posts.delete("/<int:id>")
@jwt_required()
#@swag_from("./docs/blog/posts.yaml")
def delete_post(id):

    try:

        current_user = get_jwt_identity()

        post = Post.query.filter_by(id=id).first()
        if not post:
            return jsonify({'message': 'Post not found'}), HTTP_404_NOT_FOUND

        post = Post.query.filter_by(user_id=current_user, id=id).first()
        if not post:
            return jsonify({'message': 'Not authorized to delete someone else post'}), HTTP_401_UNAUTHORIZED


        db.session.delete(post)
        db.session.commit()

        return jsonify({'message': 'Post deleted successfully'}), HTTP_204_NO_CONTENT

    except exception as e:
        return jsonify({
                    'error': "Internal Error"
                }), HTTP_500_INTERNAL_SERVER_ERROR


@posts.put('/<int:id>')
@posts.patch('/<int:id>')
@jwt_required()
#@swag_from("./docs/blog/modify_post.yaml")
def edit_post(id):

    try:
        current_user = get_jwt_identity()

        post = Post.query.filter_by(id=id).first()
        if not post:
            return jsonify({'message': 'Post not found'}), HTTP_404_NOT_FOUND

        post = Post.query.filter_by(user_id=current_user, id=id).first()
        if not post:
            return jsonify({'message': 'Not authorized to edit someone else post'}), HTTP_401_UNAUTHORIZED

        description = request.get_json().get('description', '').strip()
        titel = request.get_json().get('titel', '').strip()

        if not validators.length(titel, min=1, max=50):
                return jsonify({
                    'error': 'Post titel is too long or empty'
                }), HTTP_400_BAD_REQUEST

        if not validators.length(description, min=1, max=1000):
                return jsonify({
                    'error': 'Post description is too long or empty'
                }), HTTP_400_BAD_REQUEST

        post.titel = titel
        post.description = description

        db.session.commit()

        return jsonify({
            'id': post.id,
            'titel': post.titel,
            'description': post.description,
            'likes': post.likes,
            'created_at': post.created_at,
            'updated_at': post.updated_at,
            'user_id' : post.user_id
        }), HTTP_200_OK

    except exception as e:
        return jsonify({
                    'error': "Internal Error"
                }), HTTP_500_INTERNAL_SERVER_ERROR

    
@posts.post('/like/<int:id>')
@jwt_required()
#@swag_from("./docs/blog/like.yaml")
def add_like(id):

    try:
        current_user = get_jwt_identity()

        post = Post.query.filter_by(id=id).first()
        if not post:
            return jsonify({'message': 'Post not found'}), HTTP_404_NOT_FOUND

        like = Like.query.filter_by(user_id=current_user, post_id=id).first()
        if like:
            return jsonify({'message': 'User already liked this post'}), HTTP_409_CONFLICT
        else:
            like = Like(post_id=id, user_id=current_user)
            db.session.add(like)
            db.session.commit()

        post.likes = post.likes+1
        db.session.commit()

        return jsonify({
            'post_id': like.post_id,
            'user_id': like.user_id,
            }), HTTP_201_CREATED

    except exception as e:
        return jsonify({
                    'error': "Internal Error"
                }), HTTP_500_INTERNAL_SERVER_ERROR


@posts.delete('/like/<int:id>')
@jwt_required()
#@swag_from("./docs/blog/like.yaml")
def remove_like(id):

    try:

        current_user = get_jwt_identity()

        like = Like.query.filter_by(user_id=current_user, post_id=id).first()
        if not like:
            return jsonify({'message': 'User do not liked this post'}), HTTP_401_UNAUTHORIZED

        post = Post.query.filter_by(id=id).first() 
        db.session.delete(like)
        db.session.commit()

        post.likes = post.likes-1
        db.session.commit()

        return jsonify({'message': 'Like removed successfully'}), HTTP_204_NO_CONTENT

    except exception as e:
        return jsonify({
                    'error': "Internal Error"
                }), HTTP_500_INTERNAL_SERVER_ERROR
        


