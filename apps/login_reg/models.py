from __future__ import unicode_literals
import re
import bcrypt
from django.db import models

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
NAME_REGEX = re.compile(r'^[A-Za-z]\w+$')

class UserManager(models.Manager):
	def validate_login(self, post_data):
		errors = []
		# check DB for post_data['email']
		print post_data
		if len(self.filter(email=post_data['email'])) > 0:
			# check this user's password
			user = self.filter(email=post_data['email'])[0]
			if not bcrypt.checkpw(post_data['password'].encode(), user.password.encode()):
				errors.append('email/password incorrect')
		else:
			errors.append('email/password incorrect')

		if errors:
			return errors
		return user

	def validate_registration(self, post_data):
		errors = []
		# check length of name fields
		if len(post_data['first_name']) < 2 or len(post_data['last_name']) < 2:
			errors.append("name fields must be at least 3 characters")
		# check length of name password
		if len(post_data['password']) <8:
			errors.append("password must be at least 8 characters")
		# check name fields for letter characters
		if not re.match(NAME_REGEX, post_data['first_name']) or not re.match(NAME_REGEX, post_data['last_name']):
			errors.append("name fields must be letter characters only")
		# check emailness of email
		if not re.match(EMAIL_REGEX, post_data['email']):
			errors.append("invalid email")
		# check uniquness of email
		if len(User.objects.filter(email=post_data['email'])) > 0:
			errors.append("email already in use")
		# check password == password confirm
		if post_data['password'] != post_data['confirm_password']:
			errors.append("passwords do not match")

		if not errors:
			# make our new user
			# hash password
			hashed = bcrypt.hashpw((post_data['password'].encode()), bcrypt.gensalt(5))

			new_user = self.create(
				first_name=post_data['first_name'],
				last_name=post_data['last_name'],
				email=post_data['email'],
				password = hashed,
				address=post_data['address'],
				credit_card=post_data['credit_card']
			)
			return new_user
		return errors

class User(models.Model):
	first_name = models.CharField(max_length=255)
	last_name = models.CharField(max_length=255)
	email = models.CharField(max_length=255)
	password = models.CharField(max_length=255)
	address = models.CharField(max_length=255)
	credit_card = models.CharField(max_length=30)
	# trader = models.ManyToManyField("User", through = "Gallon")
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	objects = UserManager()

	def __repr__(self):
		return "<User: {} {} {} {} {}>".format(self.id, self.first_name, self.last_name, self.address, self.email, self.password)


class Gallon(models.Model):
	sender = models.ForeignKey(User, related_name = "gallons_sent")
	recipient = models.ForeignKey(User, related_name = "gallons_received")
	counter = models.IntegerField(default = 1)
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)

	def __repr__(self):
		return "<Gallon: {}>".format(self.counter)


##################OTHER MODELS####################

# class Donator(models.Model):
# 	amount = models.IntegerField(default = 1)
# 	donator = models.ForeignKey(User, related_name = "jugs", default = 1)
# 	created_at = models.DateTimeField(auto_now_add = True)
# 	updated_at = models.DateTimeField(auto_now = True)