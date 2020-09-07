import datetime
import re
from django.shortcuts import get_object_or_404, render, redirect
from django.template import loader
from django.core import serializers
from django_tables2 import RequestConfig
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.views.generic.edit import FormMixin, CreateView
from django.contrib.auth.models import User, Group
from django.contrib import auth
from django.forms.models import model_to_dict
from django import forms
from django.shortcuts import render

from subprocess import check_output
from decimal import *
import os, datetime, pytz, requests, hashlib
from datetime import datetime, timedelta
import array as outputArray
from rest_framework import viewsets


# Create your views here.

from FightScheduler.models import Question, Choice, StatusCode,AccountType,Role,Address,Person,Organization,Service,AllowableService,Affiliation,PersonalInformation,Career,NonBoxerInfo,Waiver,WaiverRequirement,Signature,SignedWaiver,MedicalCert,ServiceEnrollment,MatchResultCode,Series,Show,Match,MatchRound,AccountInfo,AdminInvitationCode, AvailabilitySchedule# @MODEL_IMPORTS@
from FightScheduler.serializers import StatusCodeSerializer,AccountTypeSerializer,RoleSerializer,AddressSerializer,PersonSerializer,OrganizationSerializer,ServiceSerializer,AllowableServiceSerializer,AffiliationSerializer,PersonalInformationSerializer,CareerSerializer,NonBoxerInfoSerializer,WaiverSerializer,WaiverRequirementSerializer,SignatureSerializer,SignedWaiverSerializer,MedicalCertSerializer,ServiceEnrollmentSerializer,MatchResultCodeSerializer,SeriesSerializer,ShowSerializer,MatchSerializer,MatchRoundSerializer# @SERIALIZER_IMPORTS@
from FightScheduler.forms import PersonModelForm, PersonForm, PersonCreateForm, PersonUpdateForm, PersonalInformationForm, CareerForm, NonBoxerInfoForm, MatchForm, AvailabilityScheduleForm # @FORM_IMPORTS@

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('fightscheduler:results', args=(question.id,)))

class IndexView(generic.ListView):
    #template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]
	
class DetailView(generic.DetailView):
    model = Question
    template_name = 'detail.html'

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'results.html'

class PersonView(generic.DetailView):
	model = Person
	template_name = 'individualRegistration.html'

class PersonCreate(generic.CreateView):
	model = User
	template_name = 'individualRegistration.html'
	form_class = PersonCreateForm
		
	def form_valid(self, form):
		self.object = form.save(commit=False)
		
		self.object.is_superuser = False
		self.object.is_staff = False
		self.object.is_active = True
		self.object.date_joined = datetime.now()
		self.object.save()
		group = Group.objects.get(name='User')
		group.user_set.add(self.object)
		auth.login(self.request, self.object)

		accountInfo = AccountInfo()
		accountInfo.username = self.object
		accountInfo.isBoxer = form.cleaned_data.get('isBoxer')
		accountInfo.isCoach = form.cleaned_data.get('isCoach')
		accountInfo.isOwner = form.cleaned_data.get('isOwner')
		accountInfo.isOfficial = form.cleaned_data.get('isOfficial')
		accountInfo.isBoxingOntarioAdmin = form.cleaned_data.get('isBoxingOntarioAdmin')
		accountInfo.registrationComplete = False

		accountInfo.save()
		self.request.session['accountInfo'] = model_to_dict(accountInfo)

		return HttpResponseRedirect(reverse('fightscheduler:personalInfoCreate'))

	def get_initial(self, *args, **kwargs):
		initial = super(PersonCreate, self).get_initial(**kwargs)

#		initial['username'] = 'Enter a unique login name'
#		initial['password'] = 'Enter a complex password'
		
		return initial

	def get_form_kwargs(self, *args, **kwargs):
		kwargs = super(PersonCreate, self).get_form_kwargs(*args, **kwargs)
#		kwargs['username'] = self.request.username
		return kwargs

class PersonUpdate(generic.UpdateView):
	model = User
	template_name = 'individualRegistration.html'
	form_class = PersonUpdateForm

	def get_object(self):
		return get_object_or_404(User, pk=self.request.user.id)

	def get_initial(self, *args, **kwargs):
		initial = super(PersonUpdate, self).get_initial(**kwargs)
		initial['isBoxer'] = self.request.session['accountInfo'].get('isBoxer')
		initial['isCoach'] = self.request.session['accountInfo'].get('isCoach')
		initial['isOwner'] = self.request.session['accountInfo'].get('isOwner')
		initial['isOfficial'] = self.request.session['accountInfo'].get('isOfficial')
		initial['isBoxingOntarioAdmin'] = self.request.session['accountInfo'].get('isBoxingOntarioAdmin')
		
		return initial
		
	def form_valid(self, form):
		self.object = form.save(commit=False)

		accountInfo = AccountInfo()
		accountInfo = AccountInfo.objects.get(AccountInfoID=str(self.request.session['accountInfo'].get("AccountInfoID")))
		accountInfoChanged = False
		if (accountInfo.isBoxer != form.cleaned_data.get('isBoxer')):
			accountInfo.isBoxer = form.cleaned_data.get('isBoxer')
			accountInfoChanged = True
		elif (accountInfo.isCoach != form.cleaned_data.get('isCoach')):
			accountInfo.isCoach = form.cleaned_data.get('isCoach')
			accountInfoChanged = True
		elif (accountInfo.isOfficial != form.cleaned_data.get('isOfficial')):
			accountInfo.isOfficial = form.cleaned_data.get('isOfficial')
			accountInfoChanged = True
		elif (accountInfo.isOwner != form.cleaned_data.get('isOwner')):
			accountInfo.isOwner = form.cleaned_data.get('isOwner')
			accountInfoChanged = True
		elif (accountInfo.isBoxingOntarioAdmin != form.cleaned_data.get('isBoxingOntarioAdmin')):
			accountInfo.isBoxingOntarioAdmin = form.cleaned_data.get('isBoxingOntarioAdmin')
			accountInfoChanged = True
				
		if (accountInfoChanged == True): 
			print ("account info has changed, updating registrationComplete to False")
			accountInfo.registrationComplete = False
			accountInfo.save()
			self.request.session['accountInfo'] = model_to_dict(accountInfo)
	
		self.object.save()

		group = Group.objects.get(name='User')

		return HttpResponseRedirect(reverse('fightscheduler:personUpdate'))

class PersonalInfoCreate(generic.CreateView):
	model = PersonalInformation
	template_name = 'personalInformation.html'
	form_class = PersonalInformationForm
	def form_valid(self, form):

		a = Address()
		a.streetNumber = form.cleaned_data.get('streetNumber')
		a.street = form.cleaned_data.get('street')
		a.city = form.cleaned_data.get('city')
		a.province = form.cleaned_data.get('province')
		a.postalCode = form.cleaned_data.get('postalCode')
		a.save()
		self.object = form.save(commit=False)

		self.object.addressID = a
		self.object.UserID = self.request.user
		self.object.dateofBirth = form.cleaned_data.get('dateofBirth')
		self.object.save()
#		accountInfo = AccountInfo.objects.get(AccountInfoID=self.request.session.accountInfo.accountInfoID)
		
		accountInfo = AccountInfo.objects.get(AccountInfoID=str(self.request.session['accountInfo'].get("AccountInfoID")))
		accountInfo.personalInfoID = self.object.PersonInfoID
		accountInfo.save()
		self.request.session['accountInfo'] = model_to_dict(accountInfo)
		if (accountInfo.isBoxer == True):
			return HttpResponseRedirect(reverse('fightscheduler:careerCreate'))
		elif (accountInfo.isCoach == True or accountInfo.isOwner == True or accountInfo.isOfficial == True or accountInfo.isBoxingOntarioAdmin == True):
			return HttpResponseRedirect(reverse('fightscheduler:otherInfoCreate'))
		else:
			return HttpResponseRedirect(reverse('fightscheduler:main'))

	def get_initial(self, *args, **kwargs):
		initial = super(PersonalInfoCreate, self).get_initial(**kwargs)
#		initial['password'] = 'Enter a complex password'
		
		return initial

	def get_form_kwargs(self, *args, **kwargs):
		kwargs = super(PersonalInfoCreate, self).get_form_kwargs(*args, **kwargs)
#		kwargs['username'] = self.request.username
		return kwargs

class PersonalInfoUpdate(generic.UpdateView):
	model = PersonalInformation
#	model2 = Address
	template_name = 'personalInformation.html'
	form_class = PersonalInformationForm
	
	def get_object(self):
		try:
			personInfo = PersonalInformation.objects.get(UserID=self.request.user.id)
			return get_object_or_404(PersonalInformation, pk=(personInfo.PersonInfoID))
		except PersonalInformation.DoesNotExist:
			return HttpResponseRedirect(reverse('fightscheduler:personalInfoCreate'))
#		address = Address.objects.get(AddressID = personInfo.addressID)
#		personInfo.addressID = address
#		print (str(self.request.user.id))
		
		return get_object_or_404(PersonalInformation, pk=(personInfo.PersonInfoID))

	def form_valid(self, form):
		print ("in personal update")
		self.object = form.save(commit=False)
		a = Address()
		a.AddressID = form.cleaned_data.get('addressID')
		a.streetNumber = form.cleaned_data.get('streetNumber')
		a.street = form.cleaned_data.get('street')
		a.city = form.cleaned_data.get('city')
		a.province = form.cleaned_data.get('pruovince')
		a.postalCode = form.cleaned_data.get('postalCode')
		a.save()
		print (str(form.cleaned_data.get('dateofBirth')) + "\n")
		self.object.dateofBirth = form.cleaned_data.get('dateofBirth')
		print (self.object.dateofBirth)
#		self.object.dateofBirth = datetime.strptime(form.cleaned_data('dateOfBirth'),"%m/%d/%Y")
		self.object.save()
		return HttpResponseRedirect(reverse('fightscheduler:personalInfoUpdate'))

	def get_initial(self, *args, **kwargs):
		initial = super(PersonalInfoUpdate, self).get_initial(**kwargs)

#		initial['username'] = 'Enter a unique login name'
#		initial['password'] = 'Enter a complex password'
		
		return initial

	def get_form_kwargs(self, *args, **kwargs):
		kwargs = super(PersonalInfoUpdate, self).get_form_kwargs(*args, **kwargs)
#		kwargs['username'] = self.request.username
		return kwargs


class CareerCreate(generic.CreateView):
	model = Career
	template_name = 'career.html'
	form_class = CareerForm
	def form_valid(self, form):
		self.object = form.save(commit=False)
		self.object.UserID = self.request.user
		self.object.save()

		accountInfo = AccountInfo.objects.get(AccountInfoID=self.request.session['accountInfo'].get('AccountInfoID'))
		accountInfo.careerID = self.object.CareerID
		accountInfo.save()
		self.request.session['accountInfo'] = model_to_dict(accountInfo)

		if (accountInfo.isCoach == True or accountInfo.isOwner == True or accountInfo.isOfficial == True or accountInfo.isBoxingOntarioAdmin == True):
			return HttpResponseRedirect(reverse('fightscheduler:otherInfoCreate'))
		else:
			accountInfo.registrationComplete = True
			accountInfo.save()
			self.request.session['accountInfo'] = model_to_dict(accountInfo)
			return HttpResponseRedirect(reverse('fightscheduler:main'))

	def get_initial(self, *args, **kwargs):
		initial = super(CareerCreate, self).get_initial(**kwargs)

		print('initial data', initial)
		
#		initial['username'] = 'Enter a unique login name'
#		initial['password'] = 'Enter a complex password'
		
		return initial

	def get_form_kwargs(self, *args, **kwargs):
		kwargs = super(CareerCreate, self).get_form_kwargs(*args, **kwargs)
#		kwargs['username'] = self.request.username
		return kwargs

class CareerUpdate(generic.UpdateView):
	model = Career
	template_name = 'career.html'
	form_class = CareerForm

	def get_object(self):
		print ("USERID" + str(self.request.user.id))
		try:
			career = Career.objects.get(UserID=self.request.user.id)
			print ("found career" + str(career.CareerID))
			return get_object_or_404(Career, pk=(career.CareerID))
		except Career.DoesNotExist:
			return HttpResponseRedirect(reverse('fightscheduler:careerCreate'))
	def form_valid(self, form):
		accountInfo = AccountInfo.objects.get(AccountInfoID=self.request.session['accountInfo'].get('AccountInfoID'))
		self.object = form.save(commit=False)
		self.object.save()
		if (not(accountInfo.isCoach == True or accountInfo.isOwner == True or accountInfo.isOfficial == True or accountInfo.isBoxingOntarioAdmin == True)):
			accountInfo = AccountInfo.objects.get(AccountInfoID=self.request.session['accountInfo'].get('AccountInfoID'))
			accountInfo.registrationComplete = True
			accountInfo.save()
			self.request.session['accountInfo'] = model_to_dict(accountInfo)

		return HttpResponseRedirect(reverse('fightscheduler:careerUpdate'))


class CareerUpdateOld(generic.UpdateView):
	model = Career
	template_name = 'career.html'
	form_class = CareerForm
	
	def get_object(self):
		try:
			careerInfoID = Career.objects.get(UserID=self.request.user.id)
			career = get_object_or_404(Career, pk=(careerInfoID.CareerID))
			print("Found Career!!" + str(career))
			return career
		except Career.DoesNotExist:
			print("Problems getting!!" + self.request.user.id)
			return HttpResponseRedirect(reverse('fightscheduler:careerCreate'))
		return get_object_or_404(Career, pk=(careerInfoID.CareerID))

	def form_valid(self, form):
		print("TEST!!" + self.object)
		self.object = form.save(commit=False)
		self.object.save()
		if (not(accountInfo.isCoach == True or accountInfo.isOwner == True or accountInfo.isOfficial == True or accountInfo.isBoxingOntarioAdmin == True)):
			accountInfo = AccountInfo.objects.get(AccountInfoID=self.request.session['accountInfo'].get('AccountInfoID'))
			accountInfo.registrationComplete = True
			accountInfo.save()
			self.request.session['accountInfo'] = model_to_dict(accountInfo)

		return HttpResponseRedirect(reverse('fightscheduler:careerUpdate'))

	def get_initial(self, *args, **kwargs):
		initial = super(CareerUpdate, self).get_initial(**kwargs)

		print('initial data', initial)
        # So here you're initiazing you're form's data
		career = self.get_object(self)
		print ("Wait..." + str(career.height))
		initial['height'] = career.height
		
		return initial
#		initial['username'] = 'Enter a unique login name'
#		initial['password'] = 'Enter a complex password'
		
#		return initial

	def get_form_kwargs(self, *args, **kwargs):
#		kwargs['username'] = self.request.username
		return kwargs

class OtherInfoCreate(generic.CreateView):
	model = NonBoxerInfo
	template_name = 'otherInfo.html'
	form_class = NonBoxerInfoForm
	def form_valid(self, form):
		self.object = form.save(commit=False)

		errors = ErrorList = []

		if (form.cleaned_data.get('isOwner') == True):
			if (form.cleaned_data.get('clubOwnership') == None): 
				errors.append(
					u'You\'ve indicated you are a club owner, please select a valid club'
				)

			if (form.cleaned_data.get('clubOwnershipProofDocument')):
			
				print ("Form says" + form.cleaned_data.get('clubOwnershipProofDocument').name)
			else:
				errors.append(
					u'Error proof of club ownership documentation not found'
				)

		if (form.cleaned_data.get('isCoach') == True):
			print ("Okay we're at the is coach part")
			if (form.cleaned_data.get('nccpNum') == None):
				errors.append(
					u'You\'ve indicated you are a coach, please provide a valid NCCP#'
				)
			if (form.cleaned_data.get('coachLevel') == '0'):
				errors.append(
					u'You\'ve indicated you are a coach, please select a valid Coaching Level'
				)

		if (form.cleaned_data.get('isOfficial') == True and form.cleaned_data.get('officialLevel') == '0'):
			errors.append(
				u'You\'ve indicated you are a certified official, please select a valid Official Level'
			)

		if (form.cleaned_data.get('isBoxingOntarioAdmin') == True):
			foundAdminCode = AdminInvitationCode.objects.all().filter(code=form.cleaned_data.get('boxingOntarioAdminInvitationCode'), used = False).count()
			if (foundAdminCode != 0 and form.cleaned_data.get('boxingOntarioAdminInvitationCode') != 'secretpassword'):
				errors.append(
					u'You\'ve indicated you are a Boxing Ontario Admin, please provide a valid Invitation Code, if you don\'t have one, email selby@convergentlabs.co'
				)
			if (form.cleaned_data.get('boxingOntarioEmployeeNum') == None):
				errors.append(
					u'You\'ve indicated you are a Boxing Ontario Admin, please provide a valid Boxing Ontario Employee #'
				)


		if (len(errors) > 0):
			print ("returning errors")
			form._errors[forms.forms.NON_FIELD_ERRORS] = ErrorList
			return self.form_invalid(form)

		user = User.objects.get(id=self.request.user.id)
		self.object.UserID = user
		self.object.save()
		accountInfo = AccountInfo.objects.get(AccountInfoID=self.request.session['accountInfo'].get('AccountInfoID'))
		accountInfo.otherInfoID = self.object.pk
		if (accountInfo.isBoxer == True and accountInfo.careerID != None):
			accountInfo.registrationComplete = True
		accountInfo.save()
		print ("Okay did we pass the saving part?")

		self.request.session['accountInfo'] = model_to_dict(accountInfo)
		return HttpResponseRedirect(reverse('fightscheduler:main'))

	def get_initial(self, *args, **kwargs):
		initial = super(OtherInfoCreate, self).get_initial(**kwargs)

		accountInfo = AccountInfo.objects.get(AccountInfoID=self.request.session['accountInfo'].get('AccountInfoID'))
		initial['isCoach'] = accountInfo.isCoach
		initial['isOwner'] = accountInfo.isOwner
		initial['isOfficial'] = accountInfo.isOfficial
		initial['isBoxingOntarioAdmin'] = accountInfo.isBoxingOntarioAdmin
		
#		initial['username'] = 'Enter a unique login name'
#		initial['password'] = 'Enter a complex password'
		
		return initial

	def get_form_kwargs(self, *args, **kwargs):
		kwargs = super(OtherInfoCreate, self).get_form_kwargs(*args, **kwargs)
		kwargs["request"] = self.request
		return kwargs


class OtherInfoCreateOld(generic.CreateView):
	model = NonBoxerInfo
	template_name = 'otherInfo.html'
	form_class = NonBoxerInfoForm

	def form_valid(self, form):
		self.object = form.save(commit=False)

		errors = ErrorList = []

		if (form.cleaned_data.get('isOwner') == True):
			if (form.cleaned_data.get('clubOwnership') == None): 
				errors.append(
					u'You\'ve indicated you are a club owner, please select a valid club'
				)
#			if (form.cleaned_data.get('clubOwnershipProofDocument') == None): 
#				errors.append(
#					u'You\'ve indicated you are a club owner, please upload documentary proof'
#				)

		if (form.cleaned_data.get('isCoach') == True):
			print ("Okay we're at the is coach part")
			if (form.cleaned_data.get('nccpNum') == None):
				errors.append(
					u'You\'ve indicated you are a coach, please provide a valid NCCP#'
				)
			if (form.cleaned_data.get('coachLevel') == '0'):
				errors.append(
					u'You\'ve indicated you are a coach, please select a valid Coaching Level'
				)

		if (form.cleaned_data.get('isOfficial') == True and form.cleaned_data.get('officialLevel') == '0'):
			errors.append(
				u'You\'ve indicated you are a certified official, please select a valid Official Level'
			)

		if (form.cleaned_data.get('isBoxingOntarioAdmin') == True):
			foundAdminCode = AdminInvitationCode.objects.all().filter(code=form.cleaned_data.get('boxingOntarioAdminInvitationCode'), used = False).count()
			if (foundAdminCode != 0 and form.cleaned_data.get('boxingOntarioAdminInvitationCode') != 'secretpassword'):
				errors.append(
					u'You\'ve indicated you are a Boxing Ontario Admin, please provide a valid Invitation Code, if you don\'t have one, email selby@convergentlabs.co'
				)
			if (form.cleaned_data.get('boxingOntarioEmployeeNum') == None):
				errors.append(
					u'You\'ve indicated you are a Boxing Ontario Admin, please provide a valid Boxing Ontario Employee #'
				)

		if (len(errors) > 0):
			print ("returning errors")
			form._errors[forms.forms.NON_FIELD_ERRORS] = ErrorList
			return self.form_invalid(form)

		user = User.objects.get(id=self.request.user.id)
		self.object.UserID = user
		self.object.save()
		accountInfo = AccountInfo.objects.get(AccountInfoID=self.request.session['accountInfo'].get('AccountInfoID'))
		accountInfo.otherInfoID = self.object.pk
		if (accountInfo.isBoxer == True and accountInfo.careerID != None):
			accountInfo.registrationComplete = True
		accountInfo.save()

		self.request.session['accountInfo'] = model_to_dict(accountInfo)
		return HttpResponseRedirect(reverse('fightscheduler:main'))

	def get_initial(self, *args, **kwargs):
		initial = super(OtherInfoCreate, self).get_initial(**kwargs)

		accountInfo = AccountInfo.objects.get(AccountInfoID=self.request.session['accountInfo'].get('AccountInfoID'))
		initial['isCoach'] = accountInfo.isCoach
		initial['isOwner'] = accountInfo.isOwner
		initial['isOfficial'] = accountInfo.isOfficial
		initial['isBoxingOntarioAdmin'] = accountInfo.isBoxingOntarioAdmin
		
#		initial['username'] = 'Enter a unique login name'
#		initial['password'] = 'Enter a complex password'
		
		return initial

	def get_form_kwargs(self, *args, **kwargs):
		kwargs = super(OtherInfoCreate, self).get_form_kwargs(*args, **kwargs)
		kwargs["request"] = self.request
		return kwargs


class OtherInfoUpdate(generic.UpdateView):
	model = NonBoxerInfo
	template_name = 'otherInfo.html'
	form_class = NonBoxerInfoForm

	def get_object(self):
		try:
			nonBoxerInfo = NonBoxerInfo.objects.get(UserID=self.request.user.id)
			return get_object_or_404(NonBoxerInfo, pk=(nonBoxerInfo.NonBoxerInfoID))
		except NonBoxerInfo.DoesNotExist:
			return HttpResponseRedirect(reverse('fightscheduler:otherInfoCreate'))

	def form_valid(self, form):

		self.object = form.save(commit=False)
		
		errors = ErrorList = []		

		if (form.cleaned_data.get('isOwner') == True):
			if (form.cleaned_data.get('clubOwnership') == None): 
				errors.append(
					u'You\'ve indicated you are a club owner, please select a valid club'
				)
			if (form.cleaned_data.get('clubOwnershipProofDocument')):
			
				print ("Form says" + form.cleaned_data.get('clubOwnershipProofDocument').name)
			else:
				errors.append(
					u'Error proof of club ownership documentation not found'
				)

		if (form.cleaned_data.get('isCoach') == True):
			if (form.cleaned_data.get('nccpNum') == None):
				print("here in is coach")
				errors.append(
					u'You\'ve indicated you are a coach, please provide a valid NCCP#'
				)
			if (form.cleaned_data.get('coachLevel') == '0'):
				errors.append(
					u'You\'ve indicated you are a coach, please select a valid Coaching Level'
				)
		if (form.cleaned_data.get('isOfficial') == True and form.cleaned_data.get('official Level') == '0'):
			errors.append(
				u'You\'ve indicated you are a certified official, please select a valid Official Level'
			)

		if (form.cleaned_data.get('isBoxingOntarioAdmin') == True):
			inviteCode = form.cleaned_data.get('boxingOntarioAdminInvitationCode')
			inviteCodeValid = False
			if (inviteCode == 'secretpassword'):
				inviteCodeValid = True
			elif (inviteCode == ''):
				inviteCodeValid = False
			else:
				foundAdminCode = AdminInvitationCode.objects.all().filter(code=inviteCode, used = False).count()
				if (foundAdminCode > 0):
					inviteCodeValid = True
			
			if (inviteCodeValid == False):
				errors.append(
					u'You\'ve indicated you are a Boxing Ontario Admin, please provide a valid Invitation Code, if you don\'t have one, email selby@convergentlabs.co'
				)
			if (form.cleaned_data.get('boxingOntarioEmployeeNum') == None or form.cleaned_data.get('boxingOntarioEmployeeNum') == ''):
				errors.append(
					u'You\'ve indicated you are a Boxing Ontario Admin, please provide a valid Boxing Ontario Employee #'
				)

		if (len(errors) > 0):
			print ("returning errors")
			form._errors[forms.forms.NON_FIELD_ERRORS] = ErrorList
			return self.form_invalid(form)

		user = User.objects.get(id=self.request.user.id)
		self.object.UserID = user
		self.object.save()
		accountInfo = AccountInfo.objects.get(AccountInfoID=self.request.session['accountInfo'].get('AccountInfoID'))
		accountInfo.isJudgeOnly = form.cleaned_data.get('judgeOnlyPreference')
		accountInfo.otherInfoID = self.object.pk
		if (accountInfo.isBoxer == True and accountInfo.careerID != None):
			accountInfo.registrationComplete = True
		accountInfo.save()
		self.request.session['accountInfo'] = model_to_dict(accountInfo)

		return HttpResponseRedirect(reverse('fightscheduler:otherInfoUpdate'))

	def get_initial(self, *args, **kwargs):
		initial = super(OtherInfoUpdate, self).get_initial(**kwargs)
		accountInfo = AccountInfo.objects.get(AccountInfoID=self.request.session['accountInfo'].get('AccountInfoID'))
		initial['isCoach'] = accountInfo.isCoach
		initial['isOwner'] = accountInfo.isOwner
		initial['isOfficial'] = accountInfo.isOfficial
		initial['isBoxingOntarioAdmin'] = accountInfo.isBoxingOntarioAdmin
#		initial['username'] = 'Enter a unique login name'
#		initial['password'] = 'Enter a complex password'
		
		return initial

	def get_form_kwargs(self, *args, **kwargs):
		kwargs = super(OtherInfoUpdate, self).get_form_kwargs(*args, **kwargs)
#		kwargs['username'] = self.request.username
		return kwargs

# class for club shows
class ShowCreate(generic.CreateView):
	model = Show
	template_name = 'showCreate.html'
	form_class = ShowForm

	def form_valid(self, form):
		self.object = form.save(commit=false)

		return HttpResponseRedirect(reverse('fightscheduler:matchCreate'))

	def get_initial(self, *args, **kwargs):
		initial = super(ShowCreate, self).get_initial(**kwargs)
#		initial['password'] = 'Enter a complex password'
		
		return initial

	def get_form_kwargs(self, *args, **kwargs):
		kwargs = super(ShowCreate, self).get_form_kwargs(*args, **kwargs)
#		kwargs['username'] = self.request.username
		return kwargs

class MatchCreate(generic.CreateView):
	model = Match
	template_name = 'matchCreate.html'
	form_class = MatchForm
	def form_valid(self, form):

		a = Address()
		a.streetNumber = form.cleaned_data.get('streetNumber')
		a.street = form.cleaned_data.get('street')
		a.city = form.cleaned_data.get('city')
		a.province = form.cleaned_data.get('province')
		a.postalCode = form.cleaned_data.get('postalCode')
		a.save()
		self.object = form.save(commit=False)

		self.object.addressID = a
		self.object.UserID = self.request.user
		self.object.dateofBirth = form.cleaned_data.get('dateofBirth')
		self.object.save()
#		accountInfo = AccountInfo.objects.get(AccountInfoID=self.request.session.accountInfo.accountInfoID)
		
		accountInfo = AccountInfo.objects.get(AccountInfoID=str(self.request.session['accountInfo'].get("AccountInfoID")))
		accountInfo.personalInfoID = self.object.PersonInfoID
		accountInfo.save()
		self.request.session['accountInfo'] = model_to_dict(accountInfo)
		return HttpResponseRedirect(reverse('fightscheduler:careerCreate'))

	def get_initial(self, *args, **kwargs):
		initial = super(MatchCreate, self).get_initial(**kwargs)
#		initial['password'] = 'Enter a complex password'
		
		
		return initial

	def get_form_kwargs(self, *args, **kwargs):
		kwargs = super(MatchCreate, self).get_form_kwargs(*args, **kwargs)
#		kwargs['username'] = self.request.username
		return kwargs

class MatchUpdate(generic.UpdateView):
	model = Match
#	model2 = Address
	template_name = 'matchResults.html'
	form_class = MatchForm
	
	def form_valid(self, form):
		self.object = form.save(commit=False)
		a = Address()
		a.AddressID = form.cleaned_data.get('addressID')
		a.streetNumber = form.cleaned_data.get('streetNumber')
		a.street = form.cleaned_data.get('street')
		a.city = form.cleaned_data.get('city')
		a.province = form.cleaned_data.get('province')
		a.postalCode = form.cleaned_data.get('postalCode')
		a.save()
		print (str(form.cleaned_data.get('dateofBirth')) + "\n")
		self.object.dateofBirth = form.cleaned_data.get('dateofBirth')
		print (self.object.dateofBirth)
#		self.object.dateofBirth = datetime.strptime(form.cleaned_data('dateOfBirth'),"%m/%d/%Y")
		self.object.save()
		return HttpResponseRedirect(reverse('fightscheduler:personalInfoUpdate'))

	def get_initial(self, *args, **kwargs):
		initial = super(MatchUpdate, self).get_initial(**kwargs)

#		initial['username'] = 'Enter a unique login name'
#		initial['password'] = 'Enter a complex password'
		
		return initial

	def get_form_kwargs(self, *args, **kwargs):
		kwargs = super(MatchUpdate, self).get_form_kwargs(*args, **kwargs)
#		kwargs['username'] = self.request.username
		return kwargs

class AvailabilityScheduleCreate(generic.CreateView):
	model = AvailabilitySchedule
	template_name = 'availabilitySchedule.html'
	form_class = MatchForm

class AvailabilityScheduleUpdate(generic.UpdateView):
	model = AvailabilitySchedule
	template_name = 'availabilitySchedule.html'
	form_class = MatchForm

def load_cities(request):
    country_id = request.GET.get('country')
    cities = City.objects.filter(country_id=country_id).order_by('name')
    return render(request, 'hr/city_dropdown_list_options.html', {'cities': cities})

def main(request):
	try:
		if (request.user.username != ''):
			accountInfo = AccountInfo.objects.get(username=request.user)
			request.session['accountInfo'] = model_to_dict(accountInfo)
#		request.session['accountInfo'] = accountInfo
#		print (str(request.session['accountInfo']))
#		print (str(request.session['accountInfo'].get("username")))
	except AccountInfo.DoesNotExist:
		pass
	return render(request, 'main.html')

def languageSelector(request, langCode):
    return render(request, 'main.html')

def editPersonalInformation(request, pk):
	personalInformation = PersonalInformation()
	form = PersonalInformationForm()
	if request.method == 'POST':
		form = PersonalInformationForm(request.POST)
		if form.is_valid():
			personalInformation = PersonalInformation(
				firstName=form.cleaned_data["firstName"],
				middleName=form.cleaned_data["middleName"],
				surname=form.cleaned_data["surname"],
				addressID=form.cleaned_data["addressID"],
				businessPhone=form.cleaned_data["businessPhone"],
				phoneExtension=form.cleaned_data["phoneExtension"],
				homePhone=form.cleaned_data["homePhone"],
				cellPhone=form.cleaned_data["cellPhone"],
				fax=form.cleaned_data["fax"],
				citizenship=form.cleaned_data["citizenship"],
				clubName=form.cleaned_data["clubName"],
				genderCode=form.cleaned_data["genderCode"],
				height=form.cleaned_data["height"],
				dateofBirth=form.cleaned_data["dateofBirth"],
				createdOn=form.cleaned_data["createdOn"],
				lastModified=datetime.date.today()
			)
			
			person.create()
			return HttpResponseRedirect(reverse('contactInfo'), person.PersonID)
	else:
		form = PersonForm(initial={'username': '', 'password': ''})

	context = {
			"person": person,
			"form": form,
	}

	return render(request, 'individualRegistration.html',context)	

def editProfile(request, pk):
	person = Person.objects.get(pk=pk)
	context = {
		'person': person
	}
	return render(request, 'individualRegistration.html',{})	

def clubRegistration(request):
    return render(request, 'clubRegistration.html',{})

def editClubDetails(request, pk):
	organization = Organization.objects.get(pk=pk)
	context = {
		'organization': organization
	}
	return render(request, 'clubRegistration.html',{})
	
def login(request):
	return HttpResponse("")

	
############# Auto Generated Serializer views follow #############################
class StatusCodeViewSet(viewsets.ModelViewSet): #@DEFAULT@
	queryset = StatusCode.objects.all();
	serializer_class = StatusCodeSerializer

class AccountTypeViewSet(viewsets.ModelViewSet): #@DEFAULT@
	queryset = AccountType.objects.all();
	serializer_class = AccountTypeSerializer

class RoleViewSet(viewsets.ModelViewSet): #@DEFAULT@
	queryset = Role.objects.all();
	serializer_class = RoleSerializer

class AddressViewSet(viewsets.ModelViewSet): #@DEFAULT@
	queryset = Address.objects.all();
	serializer_class = AddressSerializer

class PersonViewSet(viewsets.ModelViewSet): #@DEFAULT@
	queryset = Person.objects.all();
	serializer_class = PersonSerializer

class OrganizationViewSet(viewsets.ModelViewSet): #@DEFAULT@
	queryset = Organization.objects.all();
	serializer_class = OrganizationSerializer

class ServiceViewSet(viewsets.ModelViewSet): #@DEFAULT@
	queryset = Service.objects.all();
	serializer_class = ServiceSerializer

class AllowableServiceViewSet(viewsets.ModelViewSet): #@DEFAULT@
	queryset = AllowableService.objects.all();
	serializer_class = AllowableServiceSerializer

class AffiliationViewSet(viewsets.ModelViewSet): #@DEFAULT@
	queryset = Affiliation.objects.all();
	serializer_class = AffiliationSerializer

class PersonalInformationViewSet(viewsets.ModelViewSet): #@DEFAULT@
	queryset = PersonalInformation.objects.all();
	serializer_class = PersonalInformationSerializer

class CareerViewSet(viewsets.ModelViewSet): #@DEFAULT@
	queryset = Career.objects.all();
	serializer_class = CareerSerializer

class NonBoxerInfoViewSet(viewsets.ModelViewSet): #@DEFAULT@
	queryset = NonBoxerInfo.objects.all();
	serializer_class = NonBoxerInfoSerializer

class WaiverViewSet(viewsets.ModelViewSet): #@DEFAULT@
	queryset = Waiver.objects.all();
	serializer_class = WaiverSerializer

class WaiverRequirementViewSet(viewsets.ModelViewSet): #@DEFAULT@
	queryset = WaiverRequirement.objects.all();
	serializer_class = WaiverRequirementSerializer

class SignatureViewSet(viewsets.ModelViewSet): #@DEFAULT@
	queryset = Signature.objects.all();
	serializer_class = SignatureSerializer

class SignedWaiverViewSet(viewsets.ModelViewSet): #@DEFAULT@
	queryset = SignedWaiver.objects.all();
	serializer_class = SignedWaiverSerializer

class MedicalCertViewSet(viewsets.ModelViewSet): #@DEFAULT@
	queryset = MedicalCert.objects.all();
	serializer_class = MedicalCertSerializer

class ServiceEnrollmentViewSet(viewsets.ModelViewSet): #@DEFAULT@
	queryset = ServiceEnrollment.objects.all();
	serializer_class = ServiceEnrollmentSerializer

class MatchResultCodeViewSet(viewsets.ModelViewSet): #@DEFAULT@
	queryset = MatchResultCode.objects.all();
	serializer_class = MatchResultCodeSerializer

class SeriesViewSet(viewsets.ModelViewSet): #@DEFAULT@
	queryset = Series.objects.all();
	serializer_class = SeriesSerializer

class ShowViewSet(viewsets.ModelViewSet): #@DEFAULT@
	queryset = Show.objects.all();
	serializer_class = ShowSerializer

class MatchViewSet(viewsets.ModelViewSet): #@DEFAULT@
	queryset = Match.objects.all();
	serializer_class = MatchSerializer

class MatchRoundViewSet(viewsets.ModelViewSet): #@DEFAULT@
	queryset = MatchRound.objects.all();
	serializer_class = MatchRoundSerializer


class StatusCodeViewSet(viewsets.ModelViewSet): #@DEFAULT@
	queryset = StatusCode.objects.all();
	serializer_class = StatusCodeSerializer

class AccountTypeViewSet(viewsets.ModelViewSet): #@DEFAULT@
	queryset = AccountType.objects.all();
	serializer_class = AccountTypeSerializer

class RoleViewSet(viewsets.ModelViewSet): #@DEFAULT@
	queryset = Role.objects.all();
	serializer_class = RoleSerializer

class AddressViewSet(viewsets.ModelViewSet): #@DEFAULT@
	queryset = Address.objects.all();
	serializer_class = AddressSerializer

class PersonViewSet(viewsets.ModelViewSet): #@DEFAULT@
	queryset = Person.objects.all();
	serializer_class = PersonSerializer

class OrganizationViewSet(viewsets.ModelViewSet): #@DEFAULT@
	queryset = Organization.objects.all();
	serializer_class = OrganizationSerializer

class ServiceViewSet(viewsets.ModelViewSet): #@DEFAULT@
	queryset = Service.objects.all();
	serializer_class = ServiceSerializer

class AllowableServiceViewSet(viewsets.ModelViewSet): #@DEFAULT@
	queryset = AllowableService.objects.all();
	serializer_class = AllowableServiceSerializer

class AffiliationViewSet(viewsets.ModelViewSet): #@DEFAULT@
	queryset = Affiliation.objects.all();
	serializer_class = AffiliationSerializer

class PersonalInformationViewSet(viewsets.ModelViewSet): #@DEFAULT@
	queryset = PersonalInformation.objects.all();
	serializer_class = PersonalInformationSerializer

class CareerViewSet(viewsets.ModelViewSet): #@DEFAULT@
	queryset = Career.objects.all();
	serializer_class = CareerSerializer

class NonBoxerInfoViewSet(viewsets.ModelViewSet): #@DEFAULT@
	queryset = NonBoxerInfo.objects.all();
	serializer_class = NonBoxerInfoSerializer

class WaiverViewSet(viewsets.ModelViewSet): #@DEFAULT@
	queryset = Waiver.objects.all();
	serializer_class = WaiverSerializer

class WaiverRequirementViewSet(viewsets.ModelViewSet): #@DEFAULT@
	queryset = WaiverRequirement.objects.all();
	serializer_class = WaiverRequirementSerializer

class SignatureViewSet(viewsets.ModelViewSet): #@DEFAULT@
	queryset = Signature.objects.all();
	serializer_class = SignatureSerializer

class SignedWaiverViewSet(viewsets.ModelViewSet): #@DEFAULT@
	queryset = SignedWaiver.objects.all();
	serializer_class = SignedWaiverSerializer

class MedicalCertViewSet(viewsets.ModelViewSet): #@DEFAULT@
	queryset = MedicalCert.objects.all();
	serializer_class = MedicalCertSerializer

class ServiceEnrollmentViewSet(viewsets.ModelViewSet): #@DEFAULT@
	queryset = ServiceEnrollment.objects.all();
	serializer_class = ServiceEnrollmentSerializer

class MatchResultCodeViewSet(viewsets.ModelViewSet): #@DEFAULT@
	queryset = MatchResultCode.objects.all();
	serializer_class = MatchResultCodeSerializer

class SeriesViewSet(viewsets.ModelViewSet): #@DEFAULT@
	queryset = Series.objects.all();
	serializer_class = SeriesSerializer

class ShowViewSet(viewsets.ModelViewSet): #@DEFAULT@
	queryset = Show.objects.all();
	serializer_class = ShowSerializer

class MatchViewSet(viewsets.ModelViewSet): #@DEFAULT@
	queryset = Match.objects.all();
	serializer_class = MatchSerializer

class MatchRoundViewSet(viewsets.ModelViewSet): #@DEFAULT@
	queryset = MatchRound.objects.all();
	serializer_class = MatchRoundSerializer


class StatusCodeViewSet(viewsets.ModelViewSet): #@DEFAULT@
	queryset = StatusCode.objects.all();
	serializer_class = StatusCodeSerializer

class AccountTypeViewSet(viewsets.ModelViewSet): #@DEFAULT@
	queryset = AccountType.objects.all();
	serializer_class = AccountTypeSerializer

class RoleViewSet(viewsets.ModelViewSet): #@DEFAULT@
	queryset = Role.objects.all();
	serializer_class = RoleSerializer

class AddressViewSet(viewsets.ModelViewSet): #@DEFAULT@
	queryset = Address.objects.all();
	serializer_class = AddressSerializer

class PersonViewSet(viewsets.ModelViewSet): #@DEFAULT@
	queryset = Person.objects.all();
	serializer_class = PersonSerializer

class OrganizationViewSet(viewsets.ModelViewSet): #@DEFAULT@
	queryset = Organization.objects.all();
	serializer_class = OrganizationSerializer

class ServiceViewSet(viewsets.ModelViewSet): #@DEFAULT@
	queryset = Service.objects.all();
	serializer_class = ServiceSerializer

class AllowableServiceViewSet(viewsets.ModelViewSet): #@DEFAULT@
	queryset = AllowableService.objects.all();
	serializer_class = AllowableServiceSerializer

class AffiliationViewSet(viewsets.ModelViewSet): #@DEFAULT@
	queryset = Affiliation.objects.all();
	serializer_class = AffiliationSerializer

class PersonalInformationViewSet(viewsets.ModelViewSet): #@DEFAULT@
	queryset = PersonalInformation.objects.all();
	serializer_class = PersonalInformationSerializer

class CareerViewSet(viewsets.ModelViewSet): #@DEFAULT@
	queryset = Career.objects.all();
	serializer_class = CareerSerializer

class NonBoxerInfoViewSet(viewsets.ModelViewSet): #@DEFAULT@
	queryset = NonBoxerInfo.objects.all();
	serializer_class = NonBoxerInfoSerializer

class WaiverViewSet(viewsets.ModelViewSet): #@DEFAULT@
	queryset = Waiver.objects.all();
	serializer_class = WaiverSerializer

class WaiverRequirementViewSet(viewsets.ModelViewSet): #@DEFAULT@
	queryset = WaiverRequirement.objects.all();
	serializer_class = WaiverRequirementSerializer

class SignatureViewSet(viewsets.ModelViewSet): #@DEFAULT@
	queryset = Signature.objects.all();
	serializer_class = SignatureSerializer

class SignedWaiverViewSet(viewsets.ModelViewSet): #@DEFAULT@
	queryset = SignedWaiver.objects.all();
	serializer_class = SignedWaiverSerializer

class MedicalCertViewSet(viewsets.ModelViewSet): #@DEFAULT@
	queryset = MedicalCert.objects.all();
	serializer_class = MedicalCertSerializer

class ServiceEnrollmentViewSet(viewsets.ModelViewSet): #@DEFAULT@
	queryset = ServiceEnrollment.objects.all();
	serializer_class = ServiceEnrollmentSerializer

class MatchResultCodeViewSet(viewsets.ModelViewSet): #@DEFAULT@
	queryset = MatchResultCode.objects.all();
	serializer_class = MatchResultCodeSerializer

class SeriesViewSet(viewsets.ModelViewSet): #@DEFAULT@
	queryset = Series.objects.all();
	serializer_class = SeriesSerializer

class ShowViewSet(viewsets.ModelViewSet): #@DEFAULT@
	queryset = Show.objects.all();
	serializer_class = ShowSerializer

class MatchViewSet(viewsets.ModelViewSet): #@DEFAULT@
	queryset = Match.objects.all();
	serializer_class = MatchSerializer

class MatchRoundViewSet(viewsets.ModelViewSet): #@DEFAULT@
	queryset = MatchRound.objects.all();
	serializer_class = MatchRoundSerializer

