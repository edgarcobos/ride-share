var app=new Vue({
	el: '#app',
	data: {
		login: false,
		rides: [],
		user_id: '',
		user_first: '',
		user_last: '',
		users: [],
		rides_title: 'Rides Received',
		ride_editing: {}
	},

	created: function () {
		this.check_login();
		this.get_users();
	},

	methods:{
		check_login: function() {
			let app = this;
			axios.get('https://info3103.cs.unb.ca:8019/signin')
			.then(function (response) {
				app.login = true;
				app.user_id = response.data.user.user_id;
				app.user_first = response.data.user.first_name;
				app.user_last = response.data.user.last_name;
			})
			.catch(function(error) {
				console.log('user not logged in');
				app.login = false;
			});
		},
		login_user: function() {
			let app = this;
			let data = {
				username: $('#login-input').val(),
				password: $('#pw-input').val()
			}

			axios.post('https://info3103.cs.unb.ca:8019/signin', data)
			.then(function (response) {
				app.login = true;
				let u = response.data.user;
				app.user_id = u.user_id;
				app.user_first = u.first_name;
				app.user_last = u.last_name;
				app.show_main_menu();
			})
			.catch(function(error) {
				$('#login-input + .invalid-feedback').show();
				$('#pw-input + .invalid-feedback').show();
			});
		},
		show_main_menu: function() {
			this.clear_elements();
			this.clear_buttons();
			$('#main-menu').removeClass('d-none');
		},
		logout_user: function() {
			axios.delete('https://info3103.cs.unb.ca:8019/signin')
			.then(function (response) {
				app.login = false;
				app.rides = [];
				app.user_id = '';
			});
		},
		show_register_form: function() {
			this.clear_elements();
			$('#register-form').removeClass('d-none');
		},
		register_user: function() {
			let app = this;
			let data = {
				first_name: $('#firstname-input').val(),
				last_name: $('#lastname-input').val(),
				username: $('#login-input-2').val(),
				password: $('#pw-input-2').val()
			}

			axios.post('https://info3103.cs.unb.ca:8019/users', data)
			.then(function (response) {
				app.login = true;
				$('#register-form').addClass('d-none');
			})
			.catch(function(error) {
				$('#login-input-2 + .invalid-feedback').show();
				$('#pw-input-2 + .invalid-feedback').show();
			});
		},
		show_rides: function(sent, user_id='') {
			let app = this;
			if (app.login) {
				q = sent ? '?sent=true' : '';
				axios.get('https://info3103.cs.unb.ca:8019/users/' + user_id + '/ridesoffered' + q)
				.then(function (response) {
					app.rides = response.data.rides;
					app.clear_elements();
					$('#rides').removeClass('d-none');
				})
				.catch(function(error) {
					console.log('an error occurred');
				});
			}
		},
		show_rides2: function(sent, user_id='') {
			let app = this;
			if (app.login) {
				q = sent ? '?sent=true' : '';
				axios.get('https://info3103.cs.unb.ca:8019/users/' + user_id + '/ridestaken' + q)
				.then(function (response) {
					app.rides = response.data.rides;
					app.clear_elements();
					$('#rides').removeClass('d-none');
				})
				.catch(function(error) {
					console.log('an error occurred');
				});
			}
		},
		show_rides_offered: function(user_id, name) {
			let app = this;
			app.rides_title = 'Rides Offered by ' + name;
			app.show_rides(true, user_id);
		},
		show_rides_taken: function(user_id, name) {
			let app = this;
			app.rides_title = 'Rides Taken by ' + name;
			app.show_rides2(false, user_id);
		},
		show_ride_form: function() {
			this.clear_elements();
			this.clear_buttons();
			$('#ride-form').removeClass('d-none');
		},
		get_users: function() {
			let app = this;
			axios.get('https://info3103.cs.unb.ca:8019/users')
			.then(function (response) {
				app.users = response.data.users;
			})
			.catch(function(error) {
				$('#login-input-2 + .invalid-feedback').show();
				$('#pw-input-2 + .invalid-feedback').show();
				return [];
			});
		},
		register_ride: function() {
			let app = this;
			let ride_form = $('#ride-form');

			let data = {
				from_location: ride_form.find('#from-input').val(),
				to_location: ride_form.find('#to-input').val(),
				make_model: ride_form.find('#make-input').val(),
				license_plate: ride_form.find('#license-input').val(),
				departure_time: ride_form.find('#time-input').val(),
			}

			axios.post('https://info3103.cs.unb.ca:8019/users/'+app.user_id+'/ridesoffered', data)
			.then(function (response) {
				$('#ride-form').addClass('d-none');
			})
			.catch(function(error) {
				$('#price_input + .invalid-feedback').show();
			});
		},
		clear_elements: function() {
			$('div[id$="-form"]').addClass('d-none');
			$('div[id$="-list"]').addClass('d-none');
		},
		clear_buttons: function() {
			$('label.active').removeClass('active');
		},
		confirm_ride_taken: function(ride) {
			let app = this;
			data = { ride_id: ride.ride_id,
					driver_id: ride.driver_id}
			
			axios.post(`https://info3103.cs.unb.ca:8019/users/${app.user_id}/ridestaken`, data)
			.then(function (response) {
				ride.taken = true;
			})
			.catch(function(error) {
				console.log('an error occurred');
			});
		},
		show_users_list: function() {
			this.clear_elements();
			this.clear_buttons();
			$('#user-list').removeClass('d-none');
		},
		/*offer_ride: function(ride) {
			let app = this;
			data = { ride_id: ride.ride_id }
			
			axios.post(`https://info3103.cs.unb.ca:8014/users/${app.user_id}/ridesoffered`, data)
			.then(function (response) {
				ride.from_user = app.user_id;
			})
			.catch(function(error) {
				console.log('an error occurred');
			});
		},*/
		edit_name: function() {
			let app = this;
			let first_name = $('#edit-firstname-input').val();
			let last_name = $('#edit-lastname-input').val();
			let data = {
				username: app.user_id,
				first_name: first_name,
				last_name: last_name
			}

			axios.put(`https://info3103.cs.unb.ca:8019/users/${app.user_id}`, data)
			.then(function(response) {
				let user = response.data.user;
				app.user_first = `${user.first_name}`;
				app.user_last = `${user.last_name}`;
			})
			.catch(function(error) {
				console.log('an error occurred');
			});
		},
		delete_user: function() {
			axios.delete(`https://info3103.cs.unb.ca:8019/users/${app.user_id}`)
			.then(function(response) {
				app.login = false;
				app.rides = [];
				app.user_id = '';
				$('#edit-ride-dialog').addClass('d-none');
			})
			.catch(function(error) {
				console.log('an error occurred');
			});
		},
		edit_ride: function() {
			let app = this;
			let departure_time = $('#edit-ride-time-input').val();
			
			let data = {
				departure_time: departure_time,
				ride_id: app.ride_editing.ride_id
			}

			console.log(data);

			axios.put(`https://info3103.cs.unb.ca:8019/users/${app.user_id}/ridesoffered/${app.ride_editing.ride_id}`, data)
			.then(function(response) {
				app.ride_editing.departure_time = departure_time;
			})
			.catch(function(error) {
				console.log('an error occurred');
			})
		},
		set_editing_ride: function(ride) {
			let app = this;
			app.ride_editing = ride;
		},
		delete_ride: function(ride) {
			let app = this;
			axios.delete(`https://info3103.cs.unb.ca:8019/users/${app.user_id}/ridesoffered/${ride.ride_id}`)
			.then(function(response) {
				$(`#ride-${ride.ride_id}`).parent().remove();
			})
			.catch(function(error) {
				console.log('an error occurred');
			});
		}
	}

});
