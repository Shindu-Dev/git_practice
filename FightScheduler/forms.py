
import datetime
import re
from datetime import datetime, timedelta

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.forms.models import model_to_dict

from FightScheduler.models import StatusCode,AccountType,Role,Address,Person,Organization,Service,AllowableService,Affiliation,PersonalInformation,Career,NonBoxerInfo,Waiver,WaiverRequirement,Signature,SignedWaiver,MedicalCert,ServiceEnrollment,MatchResultCode,Series,Show,Match,MatchRound, AccountInfo, AdminInvitationCode# @MODEL_IMPORTS@

from django.forms import ModelForm
from django import forms

def validatePhoneNumber(phoneNumber):
	if re.search("^(\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}$", str(phoneNumber)) == None:
# re.search("^(((?=.*[a-z])(?=.*[A-Z]))|((?=.*[a-z])(?=.*[0-9]))|((?=.*[A-Z])(?=.*[0-9])))(?=.{6,})", data) == None:
		return False
	else:
		return True

class PersonForm(ModelForm):
	class Meta:
		model = Person
		fields = ['PersonID', 'username', 'password', 'emailAddress', 'statusCode', 'accountTypeID']

class PersonCreateFormOriginal(ModelForm):
	class Meta:
		model = Person
		fields = ['username', 'password', 'emailAddress']
	error_css_class = 'alert alert-danger'

	def clean_username(self):
		data = self.cleaned_data['username']
		#data = form.username
		if Person.objects.filter(username=data).exists():
			raise forms.ValidationError(_('Invalid username - already exists, please try another'), code='invalid', )

		if (data == "admin"):
			raise ValidationError(_('Invalid username - can\'t be admin'), code='invalid')

		# Check if a date is in the allowed range (+4 weeks from today).
#		if data > datetime.date.today() + datetime.timedelta(weeks=4):
		if len(data) < 2:
			raise ValidationError(_('Invalid username - too short'))

#		if Person.objects.filter(username=data).count() > 0 and PersonID != '':
#			print ('Duplicate username:' + data)
#			raise ValidationError(_('Username exists, please choose another'), code='invalid')

		# Remember to always return the cleaned data.
		return data		
	
	username = forms.CharField(
		max_length=100,
		widget=forms.TextInput(attrs={
			"class": "form-control",
			"placeholder": ""
		})
	)
	
	def clean_password(self):
		data = self.cleaned_data['password']
		# Check if a date is not in the past. 
#		if data < datetime.date.today():
		if re.search("^(((?=.*[a-z])(?=.*[A-Z]))|((?=.*[a-z])(?=.*[0-9]))|((?=.*[A-Z])(?=.*[0-9])))(?=.{6,})", data) == None:
			raise ValidationError(_('Invalid password - must contain 1 uppercase, 1 lowercase, 1 number, 1 special character and be more than 8 characters long'), code='invalid')

		if re.search("((password)|(abc)|(123)|(qwert))", data.lower()):
			raise ValidationError(_('Invalid password - can\'t be password, abc, 123, qwert'), code='invalid')
			
		# Remember to always return the cleaned data.

		return data	

	password = forms.CharField(
		max_length=100,
		widget=forms.PasswordInput(attrs={
			"class": "form-control",
			"placeholder": ""
		})
	)

	def clean_emailAddress(self):
		data = self.cleaned_data['emailAddress']

		# Check if a date is not in the past. 
#		if data < datetime.date.today():
		if re.search("^[a-zA-Z0-9]+[\._]?[a-zA-Z0-9]+[@]\w+[.]\w{2,3}$", data) == None:
			raise ValidationError(_('Invalid email format'), code='invalid')
			
		# Remember to always return the cleaned data.
		return data	

	emailAddress = forms.EmailField(
		widget=forms.EmailInput(attrs={
			"class": "form-control",
			"placeholder": ""
		})
	)

	lastLoginDateTime = datetime.now()
	createdOn = datetime.now()
	lastModified = datetime.now()

class PersonCreateForm(ModelForm):
	class Meta:
		model = User
		fields = ['username', 'password', 'email', 'first_name', 'last_name']
	error_css_class = 'alert alert-danger'

	def clean_username(self):
		data = self.cleaned_data['username']

		#data = form.username
		if User.objects.filter(username=data).exists():
			raise forms.ValidationError(_('Invalid username - already exists, please try another'), code='invalid', )

		if (data == "admin"):
			raise ValidationError(_('Invalid username - can\'t be admin'), code='invalid')

		if len(data) < 2:
			raise ValidationError(_('Invalid username - too short'))

		return data

	username = forms.CharField(
		required=False,
		max_length=50,
		widget=forms.TextInput(attrs={
			"class": "form-control",
			"placeholder": ""
		})
	)
	
	def clean_password(self):
		data = self.cleaned_data['password']
		# Check if a date is not in the past. 
#		if data < datetime.date.today():
		if re.search("^(((?=.*[a-z])(?=.*[A-Z]))|((?=.*[a-z])(?=.*[0-9]))|((?=.*[A-Z])(?=.*[0-9])))(?=.{6,})", data) == None:
			raise ValidationError(_('Invalid password - must contain 1 uppercase, 1 lowercase, 1 number, 1 special character and be more than 8 characters long'), code='invalid')

		if re.search("((password)|(abc)|(123)|(qwert))", data.lower()):
			raise ValidationError(_('Invalid password - can\'t be password, abc, 123, qwert'), code='invalid')
			
		# Remember to always return the cleaned data.

		return data	

	password = forms.CharField(
		max_length=100,
		widget=forms.PasswordInput(attrs={
			"class": "form-control",
			"placeholder": ""
		})
	)

	def clean_email(self):
		data = self.cleaned_data['email']

		# Check if a date is not in the past. 
#		if data < datetime.date.today():
		if re.search("^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$", data) == None:
			raise ValidationError(_('Invalid email format'), code='invalid')
			
		# Remember to always return the cleaned data.
		return data	

	email = forms.EmailField(
		widget=forms.EmailInput(attrs={
			"class": "form-control",
			"placeholder": ""
		})
	)

	first_name = forms.CharField(
		max_length=100,
		widget=forms.TextInput(attrs={
			"class": "form-control",
			"placeholder": ""
		})
	)
	last_name = forms.CharField(
		max_length=100,
		widget=forms.TextInput(attrs={
			"class": "form-control",
			"placeholder": ""
		})
	)

	isBoxer = forms.BooleanField(required=False,
		widget=forms.CheckboxInput(attrs={
			"class": "form-check-input",
		})
	)

	isCoach = forms.BooleanField(required=False,
		widget=forms.CheckboxInput(attrs={
			"class": "form-check-input",
		})
	)

	isOwner = forms.BooleanField(required=False,
		widget=forms.CheckboxInput(attrs={
			"class": "form-check-input",
		})
	)

	isOfficial = forms.BooleanField(required=False,
		widget=forms.CheckboxInput(attrs={
			"class": "form-check-input",
		})
	)

	isBoxingOntarioAdmin = forms.BooleanField(required=False,
		widget=forms.CheckboxInput(attrs={
			"class": "form-check-input",
		})
	)
		
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		
		if (hasattr(self.instance,'username')):
			self.initial['username'] = self.instance.username


class PersonUpdateForm(ModelForm):
	class Meta:
		model = User
		fields = ['email', 'first_name', 'last_name']
	error_css_class = 'alert alert-danger'

	def get_readonly_fields(self, request, obj=None):
		if obj:
			return ["username"]
		else:
			return []	
	username = forms.CharField(
		max_length=100,
		widget=forms.TextInput(attrs={
			"class": "form-control",
			"placeholder": ""
		})
	)

	def clean_email(self):
		data = self.cleaned_data['email']

		# Check if a date is not in the past. 
#		if data < datetime.date.today():
		if re.search("^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$", data) == None:
			raise ValidationError(_('Invalid email format'), code='invalid')
			
		# Remember to always return the cleaned data.
		return data	

	email = forms.EmailField(
		widget=forms.EmailInput(attrs={
			"class": "form-control",
			"placeholder": ""
		})
	)

	first_name = forms.CharField(
		max_length=100,
		widget=forms.TextInput(attrs={
			"class": "form-control",
			"placeholder": ""
		})
	)
	last_name = forms.CharField(
		max_length=100,
		widget=forms.TextInput(attrs={
			"class": "form-control",
			"placeholder": ""
		})
	)
	
	isBoxer = forms.BooleanField(required=False,
		widget=forms.CheckboxInput(attrs={
			"class": "form-check-input",
		})
	)

	isCoach = forms.BooleanField(required=False,
		widget=forms.CheckboxInput(attrs={
			"class": "form-check-input",
		})
	)

	isOwner = forms.BooleanField(required=False,
		widget=forms.CheckboxInput(attrs={
			"class": "form-check-input",
		})
	)

	isOfficial = forms.BooleanField(required=False,
		widget=forms.CheckboxInput(attrs={
			"class": "form-check-input",
		})
	)

	isBoxingOntarioAdmin = forms.BooleanField(required=False,
		widget=forms.CheckboxInput(attrs={
			"class": "form-check-input",
		})
	)
	
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		if (hasattr(self.instance,'username')):
			self.initial['username'] = self.instance.username
#			self.initial['isBoxer'] = request.session['accountInfo'].get('isBoxer')
#			self.initial['isCoach'] = request.session['accountInfo'].get('isCoach')
#			self.initial['isOwner'] = request.session['accountInfo'].get('isOwner')
#			self.initial['isOfficial'] = request.session['accountInfo'].get('isOfficial')
#			self.initial['isBoxingOntarioAdmin'] = request.session['accountInfo'].get('isBoxingOntarioAdmin')



class PersonalInformationForm(ModelForm):

	class Meta:
		model = PersonalInformation
		exclude = ['PersonInfoID', 'createdOn', 'lastModified', 'UserID']

	error_css_class = 'alert alert-danger'

	addressID = forms.CharField(required=False,
		widget=forms.HiddenInput(attrs={
			"class": "form-control",
		})
	)

	streetNumber = forms.CharField(
		max_length=5,
		widget=forms.TextInput(attrs={
			"class": "form-control",
			"placeholder": ""
		})
	)
	street = forms.CharField(
		max_length=100,
		widget=forms.TextInput(attrs={
			"class": "form-control",
			"placeholder": ""
		})
	)
	city = forms.CharField(
		max_length=100,
		widget=forms.TextInput(attrs={
			"class": "form-control",
			"placeholder": ""
		})
	)
	province = forms.CharField(
		max_length=50,
		widget=forms.TextInput(attrs={
			"class": "form-control",
			"placeholder": ""
		})
	)
	postalCode = forms.CharField(
		max_length=10,
		widget=forms.TextInput(attrs={
			"class": "form-control",
			"placeholder": ""
		})
	)
	def clean_businessPhone(self):
		data = self.cleaned_data['businessPhone']
		if (not validatePhoneNumber(data)):
			raise ValidationError(_('Invalid Business Phone number'), code='invalid')
		return data
		
	businessPhone = forms.IntegerField(
		widget=forms.TextInput(attrs={
			"class": "form-control",
			"placeholder": ""
		})
	)
	phoneExtension = forms.IntegerField(
		widget=forms.TextInput(attrs={
			"class": "form-control",
			"placeholder": ""
		}), required=False
	)
	def clean_homePhone(self):
		data = self.cleaned_data['homePhone']
		if (not validatePhoneNumber(data)):
			raise ValidationError(_('Invalid Home Phone number'), code='invalid')

		return data

	homePhone = forms.IntegerField(
		widget=forms.TextInput(attrs={
			"class": "form-control",
			"placeholder": ""
		})
	)

	def clean_cellPhone(self):
		data = self.cleaned_data['cellPhone']
		if (not validatePhoneNumber(data)):
			raise ValidationError(_('Invalid Cell Phone number'), code='invalid')
		return data

	cellPhone = forms.IntegerField(
		widget=forms.TextInput(attrs={
			"class": "form-control",
			"placeholder": ""
		})
	)

	def clean_fax(self):
		data = self.cleaned_data['fax']
		if (not validatePhoneNumber(data)):
			raise ValidationError(_('Invalid Fax number'), code='invalid')
		return data

	fax = forms.IntegerField(
		widget=forms.TextInput(attrs={
			"class": "form-control",
			"placeholder": ""
		}), required=False
	)
	citizenship = forms.CharField(
		max_length=30,
		widget=forms.TextInput(attrs={
			"class": "form-control",
			"placeholder": ""
		})
	)
	organizationID = forms.ModelChoiceField(
		queryset=Organization.objects.all(),
		widget=forms.Select(attrs={
			"class": "form-control"
		})
	)

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		if (hasattr(self.instance,'addressID') and self.instance.addressID != None):

			self.initial['streetNumber'] = self.instance.addressID.streetNumber
			self.initial['street'] = self.instance.addressID.street
			self.initial['city'] = self.instance.addressID.city
			self.initial['province'] = self.instance.addressID.province
			self.initial['postalCode'] = self.instance.addressID.postalCode
			self.initial['organizationID'] = self.instance.organizationID
#		else:
#			self.initial['addressID'] = -1

	#self.fields['clubName'].queryset = Organization.objects.all()


class CareerForm(ModelForm):

	class Meta:
		model = Career
		exclude = ['createdOn', 'lastModified', 'UserID']
	error_css_class = 'alert alert-danger'

	CareerID = forms.IntegerField(required=False,
		widget=forms.HiddenInput(attrs={
			"class": "form-control",
		})
	)

	genderCode = forms.ChoiceField(
		choices=Career.GENDER_CHOICES,
		widget=forms.Select(attrs={
			"class": "form-control",
		})
	)

	def clean_dateofBirth(self):
		print("validating date of birth")
		data = self.cleaned_data['dateofBirth']
		earliestDate = (datetime.now() - timedelta(days=120*365.25)).date()
		if (data < earliestDate):
			raise ValidationError(_('Year of birth is too early!'), code='invalid')

		latestDate = (datetime.now() - timedelta(days=7*365.25)).date()
		if (data > latestDate):
			raise ValidationError(_('Registrant is too young!'), code='invalid')
		#data = datetime.strptime(data,"%m/%d/%Y")
		return data

	dateofBirth = forms.DateField(
		widget=forms.TextInput(attrs={
			"class": "form-control",
		})
	)

	def clean_height(self):
		data = self.cleaned_data['height']
		if (data < 50):
			raise ValidationError(_('Height is too short!'), code='invalid')

		if (data > 275):
			raise ValidationError(_('Height is too tall!'), code='invalid')

		return data

	height = forms.DecimalField(
		widget=forms.TextInput(attrs={
			"class": "form-control",
			"placeholder": ""
		})
	)

	def clean_currentWeight(self):
		data = self.cleaned_data['currentWeight']
		if (data < 30):
			raise ValidationError(_('Weight seems a little light!'), code='invalid')

		if (data > 999):
			raise ValidationError(_('Weight seems a little heavy!'), code='invalid')

		return data

	currentWeight = forms.DecimalField(
		widget=forms.TextInput(attrs={
			"class": "form-control",
			"placeholder": ""
		})
	)

#	boxerType = forms.CharField(required=False,
#		widget=forms.TextInput(attrs={
#			"class": "form-control",
#			"readonly": "readonly",
#		})
#	)

	amateurBouts = forms.IntegerField(
		widget=forms.TextInput(attrs={
			"class": "form-control",
			"placeholder": ""
		})
	)
	amateurWins = forms.IntegerField(
		widget=forms.TextInput(attrs={
			"class": "form-control",
			"placeholder": ""
		})
	)

	previousProfessionalCombatSportInvolvement = forms.BooleanField(
		required=False,
		widget=forms.CheckboxInput(attrs={
			"class": "form-check-input",
			"data-toggle": "collapse",
			"data-target": "#professionalExperience"
		})
	)

	def clean_professionalYears(self):
		data = self.cleaned_data['professionalYears']
		age = self.cleaned_data['dateofBirth']

		previousProfessionalCombatSportInvolvement = self.cleaned_data['previousProfessionalCombatSportInvolvement']

		if (previousProfessionalCombatSportInvolvement == True):
			if (data == None):
				raise ValidationError(_('Please provide number of professional years'), code='invalid')

			if (data < 1 ):
				raise ValidationError(_('Please provide a valid number of years greater than 0'), code='invalid')

			if (age > (datetime.now() - timedelta(days=data*365.25)).date()):
				raise ValidationError(_('Please provide a valid number of professional years'), code='invalid')

		return data

	professionalYears = forms.IntegerField(
		required=False,
		widget=forms.TextInput(attrs={
			"class": "form-control",
			"placeholder": ""
		})
	)
	professionalBouts = forms.IntegerField(
		required=False,
		widget=forms.TextInput(attrs={
			"class": "form-control",
			"placeholder": ""
		})
	)
	professionalWins = forms.IntegerField(
		required=False,
		widget=forms.TextInput(attrs={
			"class": "form-control",
			"placeholder": ""
		})
	)
	previousCombatSportInvolvementInOtherCountry = forms.BooleanField(
		required=False,
		widget=forms.CheckboxInput(attrs={
			"class": "form-check-input",
			"data-toggle": "collapse",
			"data-target": "#foreignExperience"
		})
	)
	previousYearsOutofCountry = forms.IntegerField(
		required=False,
		widget=forms.TextInput(attrs={
			"class": "form-control",
			"placeholder": ""
		})
	)
	previousBoutsOutofCountry = forms.IntegerField(
		required=False,
		widget=forms.TextInput(attrs={
			"class": "form-control",
			"placeholder": ""
		})
	)
	previousWinsOutofCountry = forms.IntegerField(
		required=False,
		widget=forms.TextInput(attrs={
			"class": "form-control",
			"placeholder": ""
		})
	)
	previousAmateurCombatSportInvolvement = forms.BooleanField(
		required=False,
		widget=forms.CheckboxInput(attrs={
			"class": "form-check-input",
			"data-toggle": "collapse",
			"data-target": "#previousNonBoxingOntarioExperience"
		})
	)
	previousAmateurBouts = forms.IntegerField(
		required=False,
		widget=forms.TextInput(attrs={
			"class": "form-control",
			"placeholder": ""
		})
	)
	previousAmateurWins = forms.IntegerField(
		required=False,
		widget=forms.TextInput(attrs={
			"class": "form-control",
			"placeholder": ""
		})
	)
	previousAmateurKOs = forms.IntegerField(
		required=False,
		widget=forms.TextInput(attrs={
			"class": "form-control",
			"placeholder": ""
		})
	)
	previousAmateurTKOs = forms.IntegerField(
		required=False,
		widget=forms.TextInput(attrs={
			"class": "form-control",
			"placeholder": ""
		})
	)

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		print ("enters form init")
		print (str(self.instance.height))
		if (hasattr(self.instance,'dateofBirth') and self.instance.dateofBirth != None):
			print ("attempts to initialize dob")
			self.initial['dateofBirth'] = self.instance.dateofBirth.strftime("%m/%d/%Y")

class StatusCodeForm(forms.Form): #@DEFAULT@
	StatusCode = forms.CharField(
		widget=forms.TextInput(attrs={
			"class": "form-control",
			"placeholder": ""
		})
	)
	statusCodeName = forms.CharField(
		max_length=30,
		widget=forms.TextInput(attrs={
			"class": "form-control",
			"placeholder": ""
		})
	)
	description = forms.CharField(
		max_length=100,
		widget=forms.TextInput(attrs={
			"class": "form-control",
			"placeholder": ""
		})
	)

class AccountTypeForm(forms.Form): #@DEFAULT@
	AccountTypeID = forms.IntegerField(
		widget=forms.TextInput(attrs={
			"class": "form-control",
			"placeholder": ""
		})
	)
	name = forms.CharField(
		max_length=100,
		widget=forms.TextInput(attrs={
			"class": "form-control",
			"placeholder": ""
		})
	)
	description = forms.CharField(
		max_length=100,
		widget=forms.TextInput(attrs={
			"class": "form-control",
			"placeholder": ""
		})
	)

class RoleForm(forms.Form): #@DEFAULT@
	RoleID = forms.IntegerField(
		widget=forms.TextInput(attrs={
			"class": "form-control",
			"placeholder": ""
		})
	)
	name = forms.CharField(
		max_length=30,
		widget=forms.TextInput(attrs={
			"class": "form-control",
			"placeholder": ""
		})
	)
	description = forms.CharField(
		max_length=100,
		widget=forms.TextInput(attrs={
			"class": "form-control",
			"placeholder": ""
		})
	)

class AddressForm(forms.Form): #@DEFAULT@
	AddressID = forms.IntegerField(
		widget=forms.TextInput(attrs={
			"class": "form-control",
			"placeholder": ""
		})
	)
	streetNumber = forms.CharField(
		max_length=5,
		widget=forms.TextInput(attrs={
			"class": "form-control",
			"placeholder": ""
		})
	)
	street = forms.CharField(
		max_length=100,
		widget=forms.TextInput(attrs={
			"class": "form-control",
			"placeholder": ""
		})
	)
	city = forms.CharField(
		max_length=100,
		widget=forms.TextInput(attrs={
			"class": "form-control",
			"placeholder": ""
		})
	)
	province = forms.CharField(
		max_length=50,
		widget=forms.TextInput(attrs={
			"class": "form-control",
			"placeholder": ""
		})
	)
	postalCode = forms.CharField(
		max_length=10,
		widget=forms.TextInput(attrs={
			"class": "form-control",
			"placeholder": ""
		})
	)
	createdOn = forms.DateTimeField(
		widget=forms.TextInput(attrs={
			"class": "form-control",
			"placeholder": ""
		})
	)
	lastModified = forms.DateTimeField(
		widget=forms.TextInput(attrs={
			"class": "form-control",
			"placeholder": ""
		})
	)

class PersonModelForm(forms.Form):
    class Meta:
        model = Person
        fields = '__all__'


	

class OrganizationForm(forms.Form): #@DEFAULT@
	OrganizationID = forms.IntegerField(
		widget=forms.TextInput(attrs={
			"class": "form-control",
			"placeholder": ""
		})
	)
	organizationName = forms.CharField(
		max_length=100,
		widget=forms.TextInput(attrs={
			"class": "form-control",
			"placeholder": ""
		})
	)
	organizationShortName = forms.CharField(
		max_length=100,
		widget=forms.TextInput(attrs={
			"class": "form-control",
			"placeholder": ""
		})
	)
	physicalAddressID = forms.CharField(
		widget=forms.TextInput(attrs={
			"class": "form-control",
			"placeholder": ""
		})
	)
	mailingAddressID = forms.CharField(
		widget=forms.TextInput(attrs={
			"class": "form-control",
			"placeholder": ""
		})
	)
	clubOwnerPersonID = forms.CharField(
		widget=forms.TextInput(attrs={
			"class": "form-control",
			"placeholder": ""
		})
	)
	clubPresidentPersonID = forms.CharField(
		widget=forms.TextInput(attrs={
			"class": "form-control",
			"placeholder": ""
		})
	)
	clubCoachPersonID = forms.CharField(
		widget=forms.TextInput(attrs={
			"class": "form-control",
			"placeholder": ""
		})
	)
	phoneNumber = forms.IntegerField(
		widget=forms.TextInput(attrs={
			"class": "form-control",
			"placeholder": ""
		})
	)
	website = forms.CharField(
		max_length=200,
		widget=forms.Textarea(attrs={
			"class": "form-control",
			"placeholder": ""
		})
	)
	email = forms.EmailField(
		widget=forms.TextInput(attrs={
			"class": "form-control",
			"placeholder": ""
		})
	)
	additionalInsurees = forms.CharField(
		max_length=1000,
		widget=forms.Textarea(attrs={
			"class": "form-control",
			"placeholder": ""
		})
	)
	clubMailRecipients = forms.CharField(
		max_length=100,
		widget=forms.TextInput(attrs={
			"class": "form-control",
			"placeholder": ""
		})
	)
	clubEmailRecipients = forms.CharField(
		max_length=100,
		widget=forms.TextInput(attrs={
			"class": "form-control",
			"placeholder": ""
		})
	)
	createdOn = forms.DateTimeField(
		widget=forms.TextInput(attrs={
			"class": "form-control",
			"placeholder": ""
		})
	)
	lastModified = forms.DateTimeField(
		widget=forms.TextInput(attrs={
			"class": "form-control",
			"placeholder": ""
		})
	)

class ServiceForm(forms.Form): #@DEFAULT@
	ServiceID = forms.IntegerField(
		widget=forms.TextInput(attrs={
			"class": "form-control",
			"placeholder": ""
		})
	)
	code = forms.CharField(
		max_length=30,
		widget=forms.TextInput(attrs={
			"class": "form-control",
			"placeholder": ""
		})
	)
	shortName = forms.CharField(
		max_length=30,
		widget=forms.TextInput(attrs={
			"class": "form-control",
			"placeholder": ""
		})
	)
	fullName = forms.CharField(
		max_length=100,
		widget=forms.TextInput(attrs={
			"class": "form-control",
			"placeholder": ""
		})
	)
	cost = forms.DecimalField(
		widget=forms.TextInput(attrs={
			"class": "form-control",
			"placeholder": ""
		})
	)
	createdOn = forms.DateTimeField(
		widget=forms.TextInput(attrs={
			"class": "form-control",
			"placeholder": ""
		})
	)
	lastModified = forms.DateTimeField(
		widget=forms.TextInput(attrs={
			"class": "form-control",
			"placeholder": ""
		})
	)

class AllowableServiceForm(forms.Form): #@DEFAULT@
	AlowableServiceID = forms.IntegerField(
		widget=forms.TextInput(attrs={
			"class": "form-control",
			"placeholder": ""
		})
	)
	RoleID = forms.CharField(
		widget=forms.TextInput(attrs={
			"class": "form-control",
			"placeholder": ""
		})
	)
	ServiceID = forms.CharField(
		widget=forms.TextInput(attrs={
			"class": "form-control",
			"placeholder": ""
		})
	)

class AffiliationForm(forms.Form): #@DEFAULT@
	AffiliationID = forms.IntegerField(
		widget=forms.TextInput(attrs={
			"class": "form-control",
			"placeholder": ""
		})
	)
	PersonID = forms.CharField(
		widget=forms.TextInput(attrs={
			"class": "form-control",
			"placeholder": ""
		})
	)
	RoleID = forms.CharField(
		widget=forms.TextInput(attrs={
			"class": "form-control",
			"placeholder": ""
		})
	)
	affiliatedOrganizationID = forms.CharField(
		widget=forms.TextInput(attrs={
			"class": "form-control",
			"placeholder": ""
		})
	)
	affiliatedPersonID = forms.CharField(
		widget=forms.TextInput(attrs={
			"class": "form-control",
			"placeholder": ""
		})
	)



class NonBoxerInfoForm(ModelForm):

	class Meta:
		model = NonBoxerInfo
		exclude = ['UserID']
	error_css_class = 'alert alert-danger'

	NonBoxerInfoID = forms.IntegerField(required=False,
		widget=forms.HiddenInput(attrs={
			"class": "form-control",
		})
	)

	isCoach = forms.BooleanField(required=False,widget=forms.HiddenInput())
	isOwner = forms.BooleanField(required=False,widget=forms.HiddenInput())
	isOfficial = forms.BooleanField(required=False,widget=forms.HiddenInput())
	isBoxingOntarioAdmin = forms.BooleanField(required=False,widget=forms.HiddenInput())

	clubOwnership = forms.ModelChoiceField(required=False,
		queryset=Organization.objects.all(),
		widget=forms.Select(attrs={
			"class": "form-control",
			"placeholder": "<Select a club>"
		})
	)

	clubOwnershipProofDocument = forms.FileField(required=False,
#		widget=forms.TextInput(attrs={
#			"class": "form-control",
#		})
	)

	nccpNum = forms.IntegerField(required=False,
		widget=forms.TextInput(attrs={
			"class": "form-control",
		})
	)
	
	coachLevel = forms.ChoiceField(required=False,
		choices=NonBoxerInfo.COACH_LEVELS,
		widget=forms.Select(attrs={
			"class": "form-control",
			"placeholder": "<Select a coach level>"
		})
	)

	officialLevel = forms.ChoiceField(required=False,
		choices=NonBoxerInfo.OFFICIAL_LEVELS,
		widget=forms.Select(attrs={
			"class": "form-control",
			"placeholder": "<Select an official level>"
		})
	)

	judgeOnlyPreference = forms.BooleanField(required=False,
		widget=forms.CheckboxInput(attrs={
			"class": "form-check-input",
		})
	)

	boxingOntarioEmployeeNum = forms.CharField(required=False,
		widget=forms.TextInput(attrs={
			"class": "form-control",
		})
	)

	
	boxingOntarioAdminInvitationCode = forms.CharField(required=False,
		widget=forms.TextInput(attrs={
			"class": "form-control",
		})
	)
	
	policeRecordsCheckPerformed = forms.BooleanField(required=False,
		widget=forms.CheckboxInput(attrs={
			"class": "form-check-input",
		})
	)

	def clean_policeRecordsCheckExpiry(self):
		data = self.cleaned_data['policeRecordsCheckExpiry']
		earliestDate = (datetime.now() - timedelta(days=1*365.25)).date()
		if (data != None and data < earliestDate):
			raise ValidationError(_('Police Check expired over a year ago!'), code='invalid')

		return data

	policeRecordsCheckExpiry = forms.DateField(required=False,
		widget=forms.TextInput(attrs={
			"class": "form-control",
			"placeholder": ""
		})
	)

	def __init__(self, *args, **kwargs):
		self.request = kwargs.pop("request", None)
		super(NonBoxerInfoForm, self).__init__(*args, **kwargs)
		if (hasattr(self.instance,'policeRecordsCheckExpiry') and self.instance.policeRecordsCheckExpiry != None):
			self.initial['policeRecordsCheckExpiry'] = self.instance.policeRecordsCheckExpiry.strftime("%m/%d/%Y")

class WaiverForm(forms.Form): #@DEFAULT@
	WaiverID = forms.IntegerField(
		widget=forms.TextInput(attrs={
			"class": "form-control",
			"placeholder": ""
		})
	)
	name = forms.CharField(
		max_length=100,
		widget=forms.TextInput(attrs={
			"class": "form-control",
			"placeholder": ""
		})
	)
	description = forms.CharField(
		max_length=500,
		widget=forms.Textarea(attrs={
			"class": "form-control",
			"placeholder": ""
		})
	)

class WaiverRequirementForm(forms.Form): #@DEFAULT@
	WaiverRequirementID = forms.IntegerField(
		widget=forms.TextInput(attrs={
			"class": "form-control",
			"placeholder": ""
		})
	)
	roleID = forms.CharField(
		widget=forms.TextInput(attrs={
			"class": "form-control",
			"placeholder": ""
		})
	)
	annualRenewalRequired = forms.BooleanField(
		widget=forms.TextInput(attrs={
			"class": "form-control",
			"placeholder": ""
		})
	)

class SignatureForm(forms.Form): #@DEFAULT@
	SignatureID = forms.IntegerField(
		widget=forms.TextInput(attrs={
			"class": "form-control",
			"placeholder": ""
		})
	)
	image = forms.ImageField(
		max_length=5000000,
		widget=forms.Textarea(attrs={
			"class": "form-control",
			"placeholder": ""
		})
	)
	electronicSignature = forms.CharField(
		max_length=300,
		widget=forms.Textarea(attrs={
			"class": "form-control",
			"placeholder": ""
		})
	)

class SignedWaiverForm(forms.Form): #@DEFAULT@
	SignedWaiverID = forms.IntegerField(
		widget=forms.TextInput(attrs={
			"class": "form-control",
			"placeholder": ""
		})
	)
	waiverID = forms.IntegerField(
		widget=forms.TextInput(attrs={
			"class": "form-control",
			"placeholder": ""
		})
	)
	waiverFormPersonID = forms.CharField(
		widget=forms.TextInput(attrs={
			"class": "form-control",
			"placeholder": ""
		})
	)
	signatoryPersonID = forms.CharField(
		widget=forms.TextInput(attrs={
			"class": "form-control",
			"placeholder": ""
		})
	)
	signatoryRole = forms.CharField(
		max_length=100,
		widget=forms.TextInput(attrs={
			"class": "form-control",
			"placeholder": ""
		})
	)
	signatureID = forms.CharField(
		widget=forms.TextInput(attrs={
			"class": "form-control",
			"placeholder": ""
		})
	)
	signatureDate = forms.DateTimeField(
		widget=forms.TextInput(attrs={
			"class": "form-control",
			"placeholder": ""
		})
	)
	signatureLocation = forms.CharField(
		max_length=100,
		widget=forms.TextInput(attrs={
			"class": "form-control",
			"placeholder": ""
		})
	)

class MedicalCertForm(forms.Form): #@DEFAULT@
	MedicalCertID = forms.IntegerField(
		widget=forms.TextInput(attrs={
			"class": "form-control",
			"placeholder": ""
		})
	)
	PersonID = forms.CharField(
		widget=forms.TextInput(attrs={
			"class": "form-control",
			"placeholder": ""
		})
	)
	date = forms.DateField(
		widget=forms.TextInput(attrs={
			"class": "form-control",
			"placeholder": ""
		})
	)
	image = forms.ImageField(
		max_length=5000000,
		widget=forms.Textarea(attrs={
			"class": "form-control",
			"placeholder": ""
		})
	)

class ServiceEnrollmentForm(forms.Form): #@DEFAULT@
	ServiceEnrollmentID = forms.IntegerField(
		widget=forms.TextInput(attrs={
			"class": "form-control",
			"placeholder": ""
		})
	)
	personID = forms.CharField(
		widget=forms.TextInput(attrs={
			"class": "form-control",
			"placeholder": ""
		})
	)
	serviceID = forms.CharField(
		widget=forms.TextInput(attrs={
			"class": "form-control",
			"placeholder": ""
		})
	)
	startDate = forms.DateField(
		widget=forms.TextInput(attrs={
			"class": "form-control",
			"placeholder": ""
		})
	)
	endDate = forms.DateField(
		widget=forms.TextInput(attrs={
			"class": "form-control",
			"placeholder": ""
		})
	)

class MatchResultCodeForm(forms.Form): #@DEFAULT@
	MatchResultCode = forms.CharField(
		widget=forms.TextInput(attrs={
			"class": "form-control",
			"placeholder": ""
		})
	)
	description = forms.CharField(
		max_length=100,
		widget=forms.TextInput(attrs={
			"class": "form-control",
			"placeholder": ""
		})
	)

class SeriesForm(forms.Form): #@DEFAULT@
	SeriesID = forms.IntegerField(
		widget=forms.TextInput(attrs={
			"class": "form-control",
			"placeholder": ""
		})
	)
	name = forms.CharField(
		max_length=100,
		widget=forms.TextInput(attrs={
			"class": "form-control",
			"placeholder": ""
		})
	)
	organizationID = forms.CharField(
		widget=forms.TextInput(attrs={
			"class": "form-control",
			"placeholder": ""
		})
	)

class ShowForm(forms.ModelForm): #@DEFAULT@
	def __init__(self, *args, **kwargs):
		super(ShowForm, self).__init__(*args, ** kwargs)
		self.request = kwargs.pop('request', None)
		
	class Meta:
		model = Show
		fields = [organizingOrganizationID]
		#exclude = []
	error_css_class = 'alert alert-danger'
	#officialsUsers = []
	#boxersUsers = []

	showDate = forms.DateTimeField(
		widget=forms.DateTimeInput(attrs={
			"class": "form-control",
		})
	)

	showTime = forms.TimeField (
		widget=forms.TimeInput(attrs={
			"class": "form-control",
		})
	)

	clubRedID = forms.ModelChoiceField(
		queryset=Organization.objects.filter(isOrganization=True),
		widget=forms.Select(attrs={
			"class":"form-control",
		})
	)

	clubRedFighterID = forms.ModelChoiceField(
		queryset=AccountInfo.objects.filter(isBoxer=True),
		widget=forms.Select(attrs={
			"class":"form-control",
		})
	)

	clubRedFighterWeight = forms.ModelChoiceField(
		queryset=AccountInfo.objects.filter(isBoxer=True),
		widget=forms.Select(attrs={
			"class":"form-control",
		})
	)

	clubRedFighterAge = forms.ModelChoiceField(
		queryset=AccountInfo.objects.filter(isBoxer=True),
		widget=forms.Select(attrs={
			"class":"form-control",
		})
	)

	clubRedFighterExp = forms.ModelChoiceField(
		queryset=AccountInfo.objects.filter(isBoxer=True),
		widget=forms.Select(attrs={
			"class":"form-control",
		})
	)

	clubBlueID = forms.ModelChoiceField(
		queryset=Organization.objects.filter(isOrganization=True),
		widget=forms.Select(attrs={
			"class":"form-control",
		})
	)

	clubBlueFighterID = forms.ModelChoiceField(
		queryset=AccountInfo.objects.filter(isBoxer=True),
		widget=forms.Select(attrs={
			"class":"form-control",
		})
	)

	clubBlueFighterWeight = forms.ModelChoiceField(
		queryset=AccountInfo.objects.filter(isBoxer=True),
		widget=forms.Select(attrs={
			"class":"form-control",
		})
	)

	clubBlueFighterAge = forms.ModelChoiceField(
		queryset=AccountInfo.objects.filter(isBoxer=True),
		widget=forms.Select(attrs={
			"class":"form-control",
		})
	)

	clubBlueFighterExp = forms.ModelChoiceField(
		queryset=AccountInfo.objects.filter(isBoxer=True),
		widget=forms.Select(attrs={
			"class":"form-control",
		})
	)
	ShowID = forms.IntegerField(
		widget=forms.TextInput(attrs={
			"class": "form-control",
			"placeholder": ""
		})
	)
	seriesID = forms.CharField(
		widget=forms.TextInput(attrs={
			"class": "form-control",
			"placeholder": ""
		})
	)
	organizingOrganizationID = forms.CharField(
		widget=forms.TextInput(attrs={
			"class": "form-control",
			"placeholder": ""
		})
	)
	addressID = forms.CharField(
		widget=forms.TextInput(attrs={
			"class": "form-control",
			"placeholder": ""
		})
	)

class MatchForm(ModelForm):
	def __init__(self, *args, **kwargs):
		super(MatchForm, self).__init__(*args, ** kwargs)
		self.request = kwargs.pop('request', None)
#		self.setOfficialsLists()
		
	def setOfficialsLists(self):
		officialsList = AccountInfo.objects.filter(isOfficial=True)
#		officialsUsers = User.objects.filter(username__in=officialsList.values('username'))
		print ("LIST:" + str(officialsList))
#		self.fields['refereeUserID'].queryset = officialsList

	def setBoxersLists(self):
		boxersList = AccountInfo.objects.filter(isBoxer=True)
#		boxersUsers = User.objects.filter(username__in=boxersList.values('username'))
#		self.fields['blueBoxerUserID'].queryset = boxersList


	class Meta:
		model = Match
		exclude = []
	error_css_class = 'alert alert-danger'
	officialsUsers = []
	boxersUsers = []
	MatchID = forms.IntegerField(
		widget=forms.HiddenInput(attrs={
			"class": "form-control",
		})
	)
	
	boutNumber = forms.IntegerField(
		widget=forms.TextInput(attrs={
			"class": "form-control",
			"placeholder": ""
		})
	)
	
	refereeUserID = forms.ModelChoiceField(
		queryset=AccountInfo.objects.filter(isOfficial=True,isJudgeOnly=False),
		widget=forms.Select(attrs={
			"class": "form-control",
		})
	)

	cornerJudge1UserID = forms.ModelChoiceField(
		queryset=AccountInfo.objects.filter(isOfficial=True),
		widget=forms.Select(attrs={
			"class": "form-control"
		})
	)
	cornerJudge2UserID = forms.ModelChoiceField(
		queryset=AccountInfo.objects.filter(isOfficial=True),
		widget=forms.Select(attrs={
			"class": "form-control"
		})
	)
	cornerJudge3UserID = forms.ModelChoiceField(
		queryset=AccountInfo.objects.filter(isOfficial=True),
		widget=forms.Select(attrs={
			"class": "form-control"
		})
	)
	cornerJudge4UserID = forms.ModelChoiceField(
		queryset=AccountInfo.objects.filter(isOfficial=True),
		widget=forms.Select(attrs={
			"class": "form-control"
		})
	)
	redBoxerUserID = forms.ModelChoiceField(
		queryset=AccountInfo.objects.filter(isBoxer=True),
		widget=forms.Select(attrs={
			"class": "form-control"
		})
	)
	blueBoxerUserID = forms.ModelChoiceField(
		queryset=AccountInfo.objects.filter(isBoxer=True),
		widget=forms.Select(attrs={
			"class": "form-control"
		})
	)
	def clean_numberOfRounds(self):
		data = self.cleaned_data['numberOfRounds']
		
		if (data > 12):
			raise ValidationError(_('Please enter a number of rounds less than 12'), code='invalid')
		return data
		
		if (data < 1):
			raise ValidationError(_('Please enter a number of rounds greater than 0'), code='invalid')
	
	numberOfRounds = forms.IntegerField(
		widget=forms.TextInput(attrs={
			"class": "form-control",
			"placeholder": ""
		})
	)
	wentToFinalRound = forms.BooleanField(
		widget=forms.CheckboxInput(attrs={
			"class": "form-check-input",
			"placeholder": ""
		})
	)
	cornerJudge1Ruling = forms.CharField(
		widget=forms.TextInput(attrs={
			"class": "form-control",
			"placeholder": ""
		})
	)
	cornerJudge2Ruling = forms.CharField(
		widget=forms.TextInput(attrs={
			"class": "form-control",
			"placeholder": ""
		})
	)
	cornerJudge3Ruling = forms.CharField(
		widget=forms.TextInput(attrs={
			"class": "form-control",
			"placeholder": ""
		})
	)
	cornerJudge4Ruling = forms.CharField(
		widget=forms.TextInput(attrs={
			"class": "form-control",
			"placeholder": ""
		})
	)
	matchResultCode = forms.CharField(
		widget=forms.TextInput(attrs={
			"class": "form-control",
			"placeholder": ""
		})
	)
	winnerUserID = forms.ModelChoiceField(required=False,
		queryset=AccountInfo.objects.filter(isBoxer=True),
		widget=forms.TextInput(attrs={
			"class": "form-control",
			"placeholder": ""
		})
	)

class MatchRoundForm(forms.Form): #@DEFAULT@
	MatchRoundID = forms.IntegerField(
		widget=forms.TextInput(attrs={
			"class": "form-control",
			"placeholder": ""
		})
	)
	matchID = forms.CharField(
		widget=forms.TextInput(attrs={
			"class": "form-control",
			"placeholder": ""
		})
	)
	roundNumber = forms.IntegerField(
		widget=forms.TextInput(attrs={
			"class": "form-control",
			"placeholder": ""
		})
	)
	redBoxerScore = forms.IntegerField(
		widget=forms.TextInput(attrs={
			"class": "form-control",
			"placeholder": ""
		})
	)
	blueBoxerScore = forms.IntegerField(
		widget=forms.TextInput(attrs={
			"class": "form-control",
			"placeholder": ""
		})
	)

class AvailabilityScheduleForm(forms.Form): #@DEFAULT@
	AvailabilityScheduleID = forms.IntegerField(
		widget=forms.HiddenInput(attrs={
			"class": "form-control"
		})
	)
	user = forms.IntegerField(
		widget=forms.TextInput(attrs={
			"class": "form-control",
			"placeholder": ""
		})
	)
	callToConfirmAvailability = forms.BooleanField(required=False,
		widget=forms.CheckboxInput(attrs={
			"class": "form-check-input",
		})
	)
	sundayAMAvailability = forms.BooleanField(required=False,
		widget=forms.CheckboxInput(attrs={
			"class": "form-check-input",
		})
	)
	mondayAMAvailability = forms.BooleanField(required=False,
		widget=forms.CheckboxInput(attrs={
			"class": "form-check-input",
		})
	)
	tuesdayAMAvailability = forms.BooleanField(required=False,
		widget=forms.CheckboxInput(attrs={
			"class": "form-check-input",
		})
	)
	wednesdayAMAvailability = forms.BooleanField(required=False,
		widget=forms.CheckboxInput(attrs={
			"class": "form-check-input",
		})
	)
	thursdayAMAvailability = forms.BooleanField(required=False,
		widget=forms.CheckboxInput(attrs={
			"class": "form-check-input",
		})
	)
	fridayAMAvailability = forms.BooleanField(required=False,
		widget=forms.CheckboxInput(attrs={
			"class": "form-check-input",
		})
	)
	saturdayAMAvailability = forms.BooleanField(required=False,
		widget=forms.CheckboxInput(attrs={
			"class": "form-check-input",
		})
	)
	sundayPMAvailability = forms.BooleanField(required=False,
		widget=forms.CheckboxInput(attrs={
			"class": "form-check-input",
		})
	)
	mondayPMAvailability = forms.BooleanField(required=False,
		widget=forms.CheckboxInput(attrs={
			"class": "form-check-input",
		})
	)
	tuesdayPMAvailability = forms.BooleanField(required=False,
		widget=forms.CheckboxInput(attrs={
			"class": "form-check-input",
		})
	)
	wednesdayPMAvailability = forms.BooleanField(required=False,
		widget=forms.CheckboxInput(attrs={
			"class": "form-check-input",
		})
	)
	thursdayPMAvailability = forms.BooleanField(required=False,
		widget=forms.CheckboxInput(attrs={
			"class": "form-check-input",
		})
	)
	fridayPMAvailability = forms.BooleanField(required=False,
		widget=forms.CheckboxInput(attrs={
			"class": "form-check-input",
		})
	)
	saturdayPMAvailability = forms.BooleanField(required=False,
		widget=forms.CheckboxInput(attrs={
			"class": "form-check-input",
		})
	)
	availableJanuary = forms.BooleanField(required=False,
		widget=forms.CheckboxInput(attrs={
			"class": "form-check-input",
		})
	)
	availableFebruary = forms.BooleanField(required=False,
		widget=forms.CheckboxInput(attrs={
			"class": "form-check-input",
		})
	)
	availableMarch = forms.BooleanField(required=False,
		widget=forms.CheckboxInput(attrs={
			"class": "form-check-input",
		})
	)
	availableApril = forms.BooleanField(required=False,
		widget=forms.CheckboxInput(attrs={
			"class": "form-check-input",
		})
	)
	availableMay = forms.BooleanField(required=False,
		widget=forms.CheckboxInput(attrs={
			"class": "form-check-input",
		})
	)
	availableJune = forms.BooleanField(required=False,
		widget=forms.CheckboxInput(attrs={
			"class": "form-check-input",
		})
	)
	availableJuly = forms.BooleanField(required=False,
		widget=forms.CheckboxInput(attrs={
			"class": "form-check-input",
		})
	)
	availableAugust = forms.BooleanField(required=False,
		widget=forms.CheckboxInput(attrs={
			"class": "form-check-input",
		})
	)
	availableSeptember = forms.BooleanField(required=False,
		widget=forms.CheckboxInput(attrs={
			"class": "form-check-input",
		})
	)
	availableOctober = forms.BooleanField(required=False,
		widget=forms.CheckboxInput(attrs={
			"class": "form-check-input",
		})
	)
	availableNovember = forms.BooleanField(required=False,
		widget=forms.CheckboxInput(attrs={
			"class": "form-check-input",
		})
	)
	availableDecember = forms.BooleanField(required=False,
		widget=forms.CheckboxInput(attrs={
			"class": "form-check-input",
		})
	)