#!/usr/bin/env python3
import sys
from flask import Flask, jsonify, abort, request, make_response, session
from flask_restful import reqparse, Resource, Api
from flask_session import Session
import json
from ldap3 import Server, Connection, ALL
from ldap3.core.exceptions import *
import ssl
import settings
import pymysql.cursors
from utils import use_db, get_user, get_ldapConnection, get_vals, uri

app = Flask(__name__)
app.secret_key = settings.SECRET_KEY
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_COOKIE_NAME'] = 'peanutButter'
app.config['SESSION_COOKIE_DOMAIN'] = settings.APP_HOST
Session(app)


####################################################################################
#
# Error handlers
#
@app.errorhandler(400)
def bad_request(error):
	return make_response(jsonify( { 'status': 'Bad request' } ), 400)

@app.errorhandler(401)
def unauthorized(error):
	return make_response(jsonify( { 'status': 'Unauthorized' } ), 401)

@app.errorhandler(403)
def forbidden(error):
	return make_response(jsonify( { 'status': 'Access denied' } ), 403)

@app.errorhandler(404)
def not_found(error):
	return make_response(jsonify( { 'status': 'Resource not found' } ), 404)


####################################################################################
#
# SignIn
#
class SignIn(Resource):
	
	@use_db
	def post(self, cursor):
		if not request.json:
			abort(400)

		parser = reqparse.RequestParser()
		try:
			parser.add_argument('username', type=str, required=True)
			parser.add_argument('password', type=str, required=True)
			request_params = parser.parse_args()
		except:
			abort(400)

		if request_params['username'] in session:
			response = { 'user': { 'user_id': session.get('username') } }
			responseCode = 200
		else:
			user = get_user(cursor, request_params['username'])
			if user:
				try:
					ldapConnection = get_ldapConnection(request_params['username'], request_params['password'])
					ldapConnection.open()
					ldapConnection.start_tls()
					ldapConnection.bind()
                    
					session['username'] = request_params['username']
                    
					response = { 'user': user }
					responseCode = 201
				except LDAPException:
					response = { 'status': 'Access denied' }
					responseCode = 403
				finally:
					ldapConnection.unbind()

		return make_response(jsonify(response), responseCode)

	@use_db
	def get(self, cursor):
		if 'username' in session:
			response = { 'user': get_user(cursor, session['username']) }
			responseCode = 200
		else:
			response = { 'status': 'Access denied' }
			responseCode = 403

		return make_response(jsonify(response), responseCode)

	def delete(self):
		if 'username' in session:
			session.clear()
		else:
			abort(404)
		return make_response(jsonify({ 'status': 'success' }), 200)


####################################################################################
#
# Users
#
class Users(Resource):
	
	@use_db
	def post(self, cursor):
		if not request.json:
			abort(400)
		
		parser = reqparse.RequestParser()
		try:
			parser.add_argument('first_name', type=str, required=True)
			parser.add_argument('last_name', type=str, required=True)
			parser.add_argument('username', type=str, required=True)
			parser.add_argument('password', type=str, required=True)
			request_params = parser.parse_args()
		except:
			abort(400)
		
		user = get_user(cursor, request_params['username'])
		if user:
			response = {'status': 'Username already taken'}
			responseCode = 409
		else:
			try:
				ldapConnection = get_ldapConnection(request_params['username'], request_params['password'])
				ldapConnection.open()
				ldapConnection.start_tls()
				ldapConnection.bind()
								
				cursor.callproc('addUser', get_vals(request_params, 'username', 'first_name', 'last_name'))
				cursor.connection.commit()
				user = cursor.fetchone()
				user['uri'] = uri(request.url, user['user_id'])
				
				response = { 'user': user }
				responseCode = 200
			except LDAPException:
				abort(403)
			finally:
				ldapConnection.unbind()

		return make_response(jsonify(response), responseCode)
	
	@use_db
	def get(self, cursor):
		cursor.callproc('getUsers')
		users = cursor.fetchall() or []
		for user in users:
			user['uri'] = uri(request.url, user['user_id'])
		return make_response(jsonify({ 'users': users }), 200)


####################################################################################
#
# User
#
class User(Resource):

	@use_db
	def get(self, user_id, cursor):
		response = { 'status': 'User does not exist' }
		responseCode = 404

		user = get_user(cursor, user_id)
		if user:
			user['uri'] = request.url
			response = { 'user': user }
			responseCode = 200
		
		return make_response(jsonify(response), responseCode)

	@use_db
	def put(self, user_id, cursor):
		if not request.json:
			abort(400)
		
		parser = reqparse.RequestParser()
		try:
			parser.add_argument('username', type=str, required=True)
			parser.add_argument('first_name', type=str, required=True)
			parser.add_argument('last_name', type=str, required=True)
			request_params = parser.parse_args()
		except:
			abort(400)
		
		response = { 'status': 'Access denied' }
		responseCode = 403

		if session['username'] == user_id:
			cursor.callproc('updateUser', get_vals(request_params, 'username', 'first_name', 'last_name'))
			user = cursor.fetchone()
			cursor.connection.commit()
			user['uri'] = request.url
			response = { 'user': user }
			responseCode = 200

		return make_response(jsonify(response), responseCode)
	
	@use_db
	def delete(self, user_id, cursor):
		response = { 'status': 'Access denied' }
		responseCode = 403

		if session['username'] == user_id:
			cursor.callproc('deleteUser', (user_id,))
			cursor.connection.commit()
			session.clear()
			response = { 'status': 'success' }
			responseCode = 200

		return make_response(jsonify(response), responseCode)


####################################################################################
#
# Identify/create endpoints and endpoint objects
#
api = Api(app)
api.add_resource(SignIn, '/signin')
api.add_resource(Users, '/users')
api.add_resource(User, '/users/<string:user_id>')


#############################################################################
if __name__ == "__main__":
	context = ('cert.pem', 'key.pem')
	app.run(
		host=settings.APP_HOST,
		port=settings.APP_PORT,
		ssl_context=context,
		debug=settings.APP_DEBUG)
