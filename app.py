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
# AllRidesOffered
# /ridesoffered
class AllRidesOffered(Resource):

	@use_db
	def get(self, cursor):
		cursor.callproc('getOfferedRides')
		rides = cursor.fetchall() or []
		return make_response(jsonify({ 'rides': rides }), 200)

####################################################################################
#
# AllRidesOfferedID
# /ridesoffered/{id}
class AllRidesOfferedID(Resource):

	@use_db
	def get(self, ride_id, cursor):
		cursor.callproc('getOfferedRidesByID', (ride_id,))
		rides = cursor.fetchall() or []
		return make_response(jsonify({ 'rides': rides }), 200)

####################################################################################
#
# RidesOffered
# /users/{username}/ridesoffered
class RidesOffered(Resource):

	@use_db
	def get(self, user_id, cursor):
		cursor.callproc('getOfferedRidesByUser', (user_id,))
		rides = cursor.fetchall() or []
		return make_response(jsonify({ 'rides': rides }), 200)

	@use_db
	def post(self, user_id, cursor):
		if not request.json:
			abort(400)
		
		parser = reqparse.RequestParser()
		try:
			parser.add_argument('from_location', type=str, required=True)
			parser.add_argument('to_location', type=str, required=True)
			parser.add_argument('make_model', type=str, required=True)
			parser.add_argument('license_plate', type=str, required=True)
			parser.add_argument('departure_time', type=str, required=True)
			params = parser.parse_args()
		except:
			abort(400)

		response = { 'status': 'Access denied' }
		responseCode = 403
		if session['username'] == user_id:
			cursor.callproc('offerRide', (params['from_location'],params['to_location'],params['make_model'], params['license_plate'],user_id,params['departure_time'],))
			cursor.connection.commit()
			responseCode = 201
			rides = cursor.fetchall() or []
			response = { 'rides': rides }
		return make_response(jsonify(response), responseCode)

####################################################################################
#
# RideOffered
# /users/{username}/ridesoffered/{id}
class RideOffered(Resource):

	@use_db
	def get(self, ride_id, user_id, cursor):
		cursor.callproc('getOfferedRidesByIDAndDriver', (ride_id, user_id))
		rides = cursor.fetchall() or []
		return make_response(jsonify({ 'rides': rides }), 200)

	@use_db
	def delete(self, user_id, ride_id, cursor):
		response = { 'status': 'Access denied' }
		responseCode = 403

		######### it must have something to do with this uri
		######### it works without authentication as well as put
		######### will have working for final project submission
		#if session['username'] == user_id:
		cursor.callproc('deleteRide', (user_id, ride_id))
		cursor.connection.commit()
		response = { 'status': 'success' }
		responseCode = 200

		return make_response(jsonify(response), responseCode)

	@use_db
	def put(self, user_id, ride_id, cursor):
		if not request.json:
			abort(400)
		
		parser = reqparse.RequestParser()
		try:
			parser.add_argument('departure_time', type=str, required=True)
			params = parser.parse_args()
		except:
			abort(400)
		
		response = { 'status': 'Access denied' }
		responseCode = 403

		########## I don't know why the if statement isn't working
		########## it works for every other request but not this one
		########## for some godforsaken reason
		#if session['username'] == user_id:
		cursor.callproc('updateRide', (ride_id, params['departure_time']))
		ride = cursor.fetchall() or []
		cursor.connection.commit()
		response = { 'ride': ride }
		responseCode = 200

		return make_response(jsonify(response), responseCode)

####################################################################################
#
# RidesTaken
# /users/{username}/ridestaken
class RidesTaken(Resource):

	@use_db
	def get(self, user_id, cursor):
		response = { 'status': 'Access denied' }
		responseCode = 403

		#if session['username'] == user_id:
		cursor.callproc('getTakenRides', (user_id,))
		rides = cursor.fetchall() or []
		response = { 'rides': rides }
		responseCode = 200
		return make_response(jsonify(response), responseCode)

	@use_db
	def post(self, user_id, cursor):
		if not request.json:
			abort(400)
		
		parser = reqparse.RequestParser()
		try:
			parser.add_argument('ride_id', type=int, required=True)
			parser.add_argument('driver_id', type=str, required=True)
			params = parser.parse_args()
		except:
			abort(400)

		response = { 'status': 'Access denied' }
		responseCode = 403
		#if session['username'] == user_id:
		cursor.callproc('takeRide', (params['ride_id'],params['driver_id'],user_id))
		cursor.connection.commit()
		responseCode = 201
		rides = cursor.fetchall() or []
		response = { 'rides': rides }
		return make_response(jsonify(response), responseCode)

####################################################################################
#
# RideTaken
# /users/{username}/ridestaken/{id}
class RideTaken(Resource):

	@use_db
	def get(self, user_id, ride_id, cursor):
		response = { 'status': 'Access denied' }
		responseCode = 403

		#if session['username'] == user_id:
		cursor.callproc('getTakenRidesByID', (user_id, ride_id))
		rides = cursor.fetchall() or []
		response = { 'rides': rides }
		responseCode = 200
		return make_response(jsonify(response), responseCode)

	@use_db
	def delete(self, user_id, ride_id, cursor):
		response = { 'status': 'Access denied' }
		responseCode = 403
	
		#if session['username'] == user_id:
		cursor.callproc('deleteTakenRide', (user_id, ride_id))
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
api.add_resource(AllRidesOffered, '/ridesoffered')
api.add_resource(AllRidesOfferedID, '/ridesoffered/<int:ride_id>')
api.add_resource(RidesOffered, '/users/<string:user_id>/ridesoffered')
api.add_resource(RideOffered, '/users/<string:user_id>/ridesoffered/<int:ride_id>')
api.add_resource(RidesTaken, '/users/<string:user_id>/ridestaken')
api.add_resource(RideTaken, '/users/<string:user_id>/ridestaken/<int:ride_id>')


#############################################################################
if __name__ == "__main__":
	context = ('cert.pem', 'key.pem')
	app.run(
		host=settings.APP_HOST,
		port=settings.APP_PORT,
		ssl_context=context,
		debug=settings.APP_DEBUG)
