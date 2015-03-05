from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from controller.forms import UserForm, UserProfileForm
from django.contrib.auth import authenticate, login, logout
# Test interaction with model dispatcher
import dispatcher
hostname = 'PSRC3827'  # hard code this for now, eventually we might want to make a subprocess to run the dispatcher directly

# def index(request):
# 	return HttpResponse("This is the model controller app!")

def index(request):
    # Obtain the context from the HTTP request
    context = RequestContext(request)

    username = None 

    # Find the user's name
    if request.user.is_authenticated():
    	username = {'logged_name': request.user.username}
    
    return render_to_response('controller/index.html', username, context)

def about(request):
	context = RequestContext(request)

	return render_to_response('controller/about.html', context)

def register(request):
    ''' Register new site users '''
    context = RequestContext(request)
    
    # Boolean to indicate if registration was successful
    registered = False
    
    # Only execute this view if it's posted by the user
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)
        
        # If the two forms are valid
        if user_form.is_valid() and profile_form.is_valid():
            # Save user's form data to the database
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            
            # Sort out the UserProfile instance. Set commit to fasle to set user attribute manually.
            profile = profile_form.save(commit=False)
            profile.user = user
            # Save the UserProfile model instance
            profile.save()
            
            # Update our variable to tell the template registration was successful
            registered = True
            
        # Invalid form or forms?
        else:
            print user_form.errors, profile_form.errors
            
    # Not an HTTP POST, so render form using the ModelForm instance
    # These forms will be blank, ready for user input
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
        
    # Render the template depending on the context.
    return render_to_response(
        'controller/register.html',
	    {'user_form': user_form, 'profile_form': profile_form, 'registered': registered},
	    context)

def user_login(request):
	context = RequestContext(request)

	# If request is HTTP POST, try to extract user profile data
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']

		user = authenticate(username=username, password=password)

		# If we have a User object, the details are correct. 
		if user:
			# Is accoutn active? It could have been disabled by the admin
			if user.is_active:
				login(request, user)
				return HttpResponseRedirect('/controller/')
			else:
				return HttpResponse('Your account is disabled. Please contact an administrator.')
		else:
			# Invalid login details provided. 
			print "Invalid login details: {0}, {1}".format(username, password)
			return HttpResponse("Invalid login details supplied.")

	# Reguest is not HTTP POST, display the login form.
	else:
		return render_to_response('controller/login.html', {}, context)

def user_logout(request):
	logout(request)

	# Return to homepage
	return HttpResponseRedirect('/controller/')

def soundcast(request):
    ''' Initiate a new Soundcast run '''
    instance = dispatcher.StartModel()
    runid = instance.start_model(hostname)
    
    return HttpResponse('Order received, thank you come again!' + str(runid))