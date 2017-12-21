from __future__ import unicode_literals
from .models import User, Gallon
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.db.models import Sum

def index(request):
	context={
		'users': User.objects.all()
	}
	return render(request, "login_reg/index.html", context)

def registration(request):
	result = User.objects.validate_registration(request.POST)	
	if type(result) == list:
		for err in result:
			messages.error(request, err)
		return redirect('/')
	request.session['user_id'] = result.id
	messages.success(request, "Registration Successful!")
	return redirect('/success')

def login(request):
	print 'post', request.POST
	result = User.objects.validate_login(request.POST)
	if type(result) == list:
		for err in result:
			messages.error(request, err)
		return redirect('/')
	request.session['user_id'] = result.id
	messages.success(request, "Login Successful!")
	return redirect('/success')

def success(request):
	try:
		request.session['user_id']
	except Keyerror:
		return redirect('/')
	context = {
		'current_user': User.objects.get(id=request.session['user_id']),
		'users': User.objects.exclude(id = request.session['user_id']),
		# 'count': User.received.count()
		'gallons': Gallon.objects.values('recipient').annotate(count=Sum('counter'))
	}
	print context['gallons']
	print context['users']
	return render(request, 'login_reg/success.html', context)

	#for user in users
	 # if gallons.search('recipient') == user.id
	 # 	{{ gallons.count }}

def ship(request, user_id):
	user1 = User.objects.get(id=request.session['user_id'])
	user2 = User.objects.get(id = user_id)
	gallon = Gallon.objects.get(sender = user1, recipient = user2)
	if not gallon:
		print "new"
		Gallon.objects.create(sender = user1, recipient = user2, counter = 1)
	else:
		gallon.counter +=1
		gallon.save()
		print gallon.counter

	# user1.sent.add(user2).add(gallon)

	return redirect('/success')

def logout(request, user_id):
	del request.session
	return redirect('/')
