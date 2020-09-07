import datetime,pytz
from django.db import models
from django_serializable_model import SerializableModel
from decimal import *
from django.contrib.auth.models import User, Group

localtz = pytz.timezone("America/Toronto")
defaultDateTime = datetime.datetime(2019,1,1,0,0,0,0,localtz)

ADULT = 'AD'
JUNIOR = 'JR'
NOT = 'NO'
BOXER_TYPE_CHOICES = (
	(ADULT, 'Adult Boxer'),
	(JUNIOR, 'Junior Boxer'),
	(NOT, 'Not a Boxer'),
)

class Question(models.Model):
    def __str__(self):
        return self.question_text
    question_text = models.CharField(max_length=200)
    pub_date = models.DateField('date published')
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

class Choice(models.Model):
    def __str__(self):
        return self.choice_text
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

class StatusCode(models.Model):
	def __str__(self):
		return self
	StatusCode = models.CharField(max_length=5,primary_key=True,)
	statusCodeName = models.CharField(max_length=30,)
	description = models.CharField(max_length=100,)

class AccountType(models.Model):
	def __str__(self):
		return self
	AccountTypeID = models.AutoField(primary_key=True,)
	name = models.CharField(max_length=100,)
	description = models.CharField(max_length=100,)

class Role(models.Model):
	def __str__(self):
		return self
	RoleID = models.AutoField(primary_key=True,)
	name = models.CharField(max_length=30,)
	description = models.CharField(max_length=100,)

class Address(models.Model):
	def __str__(self):
		return str(self.AddressID) + "," + str(self.streetNumber) + "," +  self.street + "," + self.city + "," + self.province + "," + self.postalCode
	AddressID = models.AutoField(primary_key=True,)
	streetNumber = models.CharField(max_length=5,)
	street = models.CharField(max_length=100,)
	city = models.CharField(max_length=100,)
	province = models.CharField(max_length=50,)
	postalCode = models.CharField(max_length=10,)
	createdOn = models.DateTimeField(auto_now_add=True,null=True,)
	lastModified = models.DateTimeField(auto_now=True,null=True,)

class Person(models.Model):
	def __str__(self):
		return self
	PersonID = models.AutoField(primary_key=True,)
	username = models.CharField(max_length=100,)
	password = models.CharField(max_length=100,)
	emailAddress = models.EmailField()
	statusCode = models.ForeignKey(StatusCode,on_delete=models.PROTECT,verbose_name="Person System Status",related_name="Person_System_Status",)
	accountTypeID = models.ForeignKey(AccountType,on_delete=models.PROTECT,verbose_name="Person Account Type",related_name="Person_Account_Type",)
	lastLoginDateTime = models.DateTimeField(auto_now=True,null=True,)
	createdOn = models.DateTimeField(auto_now_add=True,null=True,)
	lastModified = models.DateTimeField(auto_now=True,null=True,)

class Organization(models.Model):
	def __str__(self):
		return self.organizationName
	OrganizationID = models.AutoField(primary_key=True,)
	organizationName = models.CharField(max_length=100,unique=True)
	organizationShortName = models.CharField(max_length=100,null=True,)
	physicalAddressID = models.ForeignKey(Address,on_delete=models.PROTECT,verbose_name="Physical Address of Organization",related_name="Physical_Address_of_Organization",)
	mailingAddressID = models.ForeignKey(Address,on_delete=models.PROTECT,verbose_name="Mailing Address of Organization",related_name="Mailing_Address_of_Organization",)
	clubOwnerUserID = models.ForeignKey(User,on_delete=models.PROTECT,verbose_name="Club Owner User",related_name="Club_Owner_User",null=True)
	clubPresidentUserID = models.ForeignKey(User,on_delete=models.PROTECT,verbose_name="President User",related_name="President_User",null=True)
	clubCoachUserID = models.ForeignKey(User,on_delete=models.PROTECT,verbose_name="Club Coach User",related_name="Club_Coach_User",null=True)
	phoneNumber = models.IntegerField(null=True,)
	website = models.CharField(max_length=200,null=True,)
	email = models.EmailField(null=True,)
	additionalInsurees = models.CharField(max_length=1000,null=True,)
	clubMailRecipients = models.CharField(max_length=100,null=True,)
	clubEmailRecipients = models.CharField(max_length=100,null=True,)
	createdOn = models.DateTimeField(auto_now_add=True,null=True,)
	lastModified = models.DateTimeField(auto_now=True,null=True,)
	isOrganization = models.BooleanField(default=False)
	
class Service(models.Model):
	def __str__(self):
		return self
	ServiceID = models.AutoField(primary_key=True,)
	code = models.CharField(max_length=30,)
	shortName = models.CharField(max_length=30,)
	fullName = models.CharField(max_length=100,)
	cost = models.DecimalField(max_digits=6, decimal_places=2)
	createdOn = models.DateTimeField(auto_now_add=True,null=True,)
	lastModified = models.DateTimeField(auto_now=True,null=True,)

class AllowableService(models.Model):
	def __str__(self):
		return self
	AlowableServiceID = models.AutoField(primary_key=True,)
	RoleID = models.ForeignKey(Role,on_delete=models.PROTECT,verbose_name="Role Associated to Allowed Service",related_name="Role_Associated_to_Allowed_Service",)
	ServiceID = models.ForeignKey(Service,on_delete=models.PROTECT,verbose_name="Service Associated to Allowed Service",related_name="Service_Associated_to_Allowed_Service",)

class Affiliation(models.Model):
	def __str__(self):
		return self
	AffiliationID = models.AutoField(primary_key=True,)
	UserID = models.ForeignKey(User,on_delete=models.PROTECT,verbose_name="User Affiliation to Organization",related_name="User_Affiliation_to_Organization",)
	RoleID = models.ForeignKey(Role,on_delete=models.PROTECT,verbose_name="Role ID",related_name="Role_ID",null=True)
	affiliatedOrganizationID = models.ForeignKey(Organization,on_delete=models.PROTECT,verbose_name="Affiliated Organiation",related_name="Affiliated_Organiation",null=True)
	affiliatedUserID = models.ForeignKey(User,on_delete=models.PROTECT,verbose_name="User Affiliated to Other User in Organization",related_name="User_Affiliated_to_Other_User_in_Organization",)

class PersonalInformation(models.Model):
	def __str__(self):
		return str(self.PersonInfoID) + ",uid:" + str(self.UserID) + ",addressID:" + str(self.addressID) + ",businessPhone:" + str(self.businessPhone) + ",club: " + str(self.organizationID)
	PersonInfoID = models.AutoField(primary_key=True,)
	UserID = models.OneToOneField(User,on_delete=models.PROTECT,verbose_name="User ID for Personal Information",related_name="User_ID_for_Personal_Information",)
	addressID = models.OneToOneField(Address,on_delete=models.SET_NULL,verbose_name="Address of User",related_name="Address_of_User",null=True)
	businessPhone = models.IntegerField(null=True)
	phoneExtension = models.CharField(max_length=10 ,null=True)
	homePhone = models.IntegerField(null=True)
	cellPhone = models.IntegerField(null=True)
	fax = models.IntegerField(null=True)
	citizenship = models.CharField(max_length=30,)
	organizationID = models.ForeignKey(Organization,on_delete=models.SET_NULL,verbose_name="Club of the User",related_name="Club_of_User",null=True)
	createdOn = models.DateTimeField(auto_now_add=True,null=True,)
	lastModified = models.DateTimeField(auto_now=True,null=True,)

class Career(models.Model):
	def __str__(self):
		return str(self.CareerID) + ",uid:" + str(self.UserID)
	CareerID = models.AutoField(primary_key=True,)
	UserID = models.OneToOneField(User,on_delete=models.CASCADE,verbose_name="User ID for Career Info",related_name="User_ID_for_Career_Info",)


	F = 'Female'
	M = 'Male'
	O = 'Other'
	GENDER_CHOICES = (
		(M, 'Male'),
		(F, 'Female'),
		(O, 'Other'),
	)

	genderCode = models.CharField(max_length=10,choices=GENDER_CHOICES,default=M)
	dateofBirth = models.DateField(null=True,)

	height = models.DecimalField(max_digits=5, decimal_places=2)
	currentWeight = models.DecimalField(max_digits=6, decimal_places=2)

#	boxerType = models.CharField(max_length=2,choices=BOXER_TYPE_CHOICES,null=True)

	amateurBouts = models.IntegerField(null=True,)
	amateurWins = models.IntegerField(null=True,)
	previousProfessionalCombatSportInvolvement = models.BooleanField(null=True,default=False)
	professionalYears = models.IntegerField(null=True,)
	professionalBouts = models.IntegerField(null=True,)
	professionalWins = models.IntegerField(null=True,)
	previousCombatSportInvolvementInOtherCountry = models.BooleanField(null=True,)
	previousYearsOutofCountry = models.IntegerField(null=True,)
	previousBoutsOutofCountry = models.IntegerField(null=True,)
	previousWinsOutofCountry = models.IntegerField(null=True,)
	previousAmateurCombatSportInvolvement = models.BooleanField(null=True,)
	previousAmateurBouts = models.IntegerField(null=True,)
	previousAmateurWins = models.IntegerField(null=True,)
	previousAmateurKOs = models.IntegerField(null=True,)
	previousAmateurTKOs = models.IntegerField(null=True,)
	createdOn = models.DateTimeField(auto_now_add=True,null=True,)
	lastModified = models.DateTimeField(auto_now=True,null=True,)

class AccountInfo(models.Model):
	def __str__(self):
		return str(self.AccountInfoID) + "," + self.username.username + "," + str(self.isCoach) + "," +str(self.isOwner) + "," + str(self.isOfficial) + "," + str(self.isBoxingOntarioAdmin)

	AccountInfoID = models.AutoField(primary_key=True)
	username = models.OneToOneField(User,on_delete=models.CASCADE,verbose_name="User ID for Account Info",related_name="User_ID_for_Account_Info",)
	personalInfoID = models.IntegerField(null=True)
	careerID = models.IntegerField(null=True)
	otherInfoID = models.IntegerField(null=True)
	
#	boxerType = models.CharField(max_length=20)
	isBoxer = models.BooleanField(default=False)
	isCoach = models.BooleanField(default=False)
	isOwner = models.BooleanField(default=False)
	isOfficial = models.BooleanField(default=False)
	isJudgeOnly = models.BooleanField(default=False)
	isBoxingOntarioAdmin = models.BooleanField(default=False)
	
	registrationComplete = models.BooleanField(default=False)
	
class NonBoxerInfo(models.Model):
	def __str__(self):
		return self

	COACH_LEVELS = (
		('1', '1 - Certified Apprentice Coach'),
		('2', '2 - Certified Club Coach'),
		('3', '3 - Competition Coach'),
		('4', '4 - Advanced Coaching Diploma I'),
		('5', '5 - Advanced Coaching Diploma II'),
	)

	OFFICIAL_LEVELS = (
		('1', '1 - Regional I'),
		('2', '2 - Regional II'),
		('3', '3 - Provincial'),
		('4', '4 - National'),
	)

	NonBoxerInfoID = models.AutoField(primary_key=True,)
	UserID = models.OneToOneField(User,on_delete=models.CASCADE,verbose_name="User ID for Additional Non Boxer Info",related_name="User_ID_for_Additional_Non_Boxer_Info",)
	nccpNum = models.IntegerField(null=True)
	coachLevel = models.CharField(max_length=30,choices=COACH_LEVELS,default='1')
	officialLevel = models.CharField(max_length=30,choices=OFFICIAL_LEVELS,default='1')
	judgeOnlyPreference = models.BooleanField()
	clubOwnership = models.ForeignKey(Organization,on_delete=models.SET_NULL,verbose_name="Club of the Owner",related_name="Club_of_Owner",null=True)
	clubOwnershipProofDocument = models.FileField(max_length=5000000,null=True)
	boxingOntarioAdminInvitationCode = models.CharField(max_length=20,null=True)
	boxingOntarioEmployeeNum = models.CharField(max_length=30, null=True)
	policeRecordsCheckPerformed = models.BooleanField()
	policeRecordsCheckExpiry = models.DateField(null=True,)

class AdminInvitationCode(models.Model):
	def __str__(self):
		return code + "," + emailAddress + "," + str(used)
	AdminInvitationCodeID = models.AutoField(primary_key=True,)
	code = models.CharField(max_length=20, unique=True)
	emailAddress = models.EmailField()
	used = models.BooleanField()

class Waiver(models.Model):
	def __str__(self):
		return self
	WaiverID = models.AutoField(primary_key=True,)
	name = models.CharField(max_length=100,)
	description = models.CharField(max_length=500,)

class WaiverRequirement(models.Model):
	def __str__(self):
		return self
	WaiverRequirementID = models.AutoField(primary_key=True,)
	roleID = models.ForeignKey(Role,on_delete=models.CASCADE,verbose_name="Role Requiring a Waiver",related_name="Role_Requiring_a_Waiver",)
	annualRenewalRequired = models.BooleanField()

class Signature(models.Model):
	def __str__(self):
		return self
	SignatureID = models.AutoField(primary_key=True,)
	image = models.FileField(max_length=5000000,)
	electronicSignature = models.CharField(max_length=300,)

class SignedWaiver(models.Model):
	def __str__(self):
		return self
	SignedWaiverID = models.AutoField(primary_key=True,)
	waiverID = models.IntegerField()
	waiverFormUserID = models.ForeignKey(User,on_delete=models.PROTECT,verbose_name="Waiver Form User",related_name="Waiver_Form_User",)
	signatoryUserID = models.ForeignKey(User,on_delete=models.PROTECT,verbose_name="Signatory on Behalf Of",related_name="Signatory_on_Behalf_Of",)
	signatoryRole = models.CharField(max_length=100,)
	signatureID = models.ForeignKey(Signature,on_delete=models.PROTECT,verbose_name="Signature ID",related_name="Signature_ID",)
	signatureDate = models.DateTimeField(auto_now_add=True,null=True,)
	signatureLocation = models.CharField(max_length=100,)

class MedicalCert(models.Model):
	def __str__(self):
		return self
	MedicalCertID = models.AutoField(primary_key=True,)
	UserID = models.ForeignKey(User,on_delete=models.PROTECT,verbose_name="Medical Cert User ID",related_name="Medical_Cert_User_ID",)
	date = models.DateField(auto_now_add=True,null=True,)
	image = models.FileField(max_length=5000000,)

class ServiceEnrollment(models.Model):
	def __str__(self):
		return self
	ServiceEnrollmentID = models.AutoField(primary_key=True,)
	UserID = models.ForeignKey(User,on_delete=models.PROTECT,verbose_name="Enrolled User ID",related_name="Enrolled_User_ID",)
	serviceID = models.ForeignKey(Service,on_delete=models.PROTECT,verbose_name="Service ID",related_name="Service_ID",)
	startDate = models.DateField(auto_now_add=True,null=True,)
	endDate = models.DateField(auto_now_add=True,null=True,)

class MatchResultCode(models.Model):
	def __str__(self):
		return self
	MatchResultCode = models.CharField(max_length=4,primary_key=True,)
	description = models.CharField(max_length=100,)

class Series(models.Model):
	def __str__(self):
		return self
	SeriesID = models.AutoField(primary_key=True,)
	name = models.CharField(max_length=100,)
	organizationID = models.ForeignKey(Organization,on_delete=models.PROTECT,verbose_name="Organization ID",related_name="Organization_ID",)

class Show(models.Model):
	def __str__(self):
		return self
	ShowID = models.AutoField(primary_key=True,)
	seriesID = models.ForeignKey(Series,on_delete=models.PROTECT,verbose_name="Series ID",related_name="Series_ID",)
	organizingOrganizationID = models.ForeignKey(Organization,on_delete=models.PROTECT,verbose_name="Organizing Organization ID",related_name="Organizing_Organization_ID",)
	addressID = models.ForeignKey(Address,on_delete=models.PROTECT,verbose_name="Show Venue",related_name="Show_Venue",)

class Match(models.Model):
	def __str__(self):
		return self

	KO= 'KO'
	TKO= 'TKO'
	UD= 'UD'
	SD= 'SD'
	MD= 'MD'
	DR= 'DR'


	MATCH_RESULTS = (
		(KO, 'Knock Out'),
		(TKO, 'Technical Knock Out'),
		(UD, 'Unanimous Decision'),
		(SD, 'Split Decision'),
		(MD, 'Majority Decision'),
		(DR, 'Draw'),
	)
	MatchID = models.AutoField(primary_key=True,)
	refereeUserID = models.ForeignKey(User,on_delete=models.PROTECT,verbose_name="Referee User ID",related_name="Referee_User_ID",)
	cornerJudge1UserID = models.ForeignKey(User,on_delete=models.PROTECT,verbose_name="Corner Judge 1 User ID",related_name="Corner_Judge_1_User_ID",)
	cornerJudge2UserID = models.ForeignKey(User,on_delete=models.PROTECT,verbose_name="Corner Judge 2 User ID",related_name="Corner_Judge_2_User_ID",)
	cornerJudge3UserID = models.ForeignKey(User,on_delete=models.PROTECT,verbose_name="Corner Judge 3 User ID",related_name="Corner_Judge_3_User_ID",)
	cornerJudge4UserID = models.ForeignKey(User,on_delete=models.PROTECT,verbose_name="Corner Judge 4 User ID",related_name="Corner_Judge_4_User_ID",)
	redBoxerUserID = models.ForeignKey(User,on_delete=models.PROTECT,verbose_name="Red Corner Boxer",related_name="Red_Corner_Boxer",)
	blueBoxerUserID = models.ForeignKey(User,on_delete=models.PROTECT,verbose_name="Blue Corner Boxer",related_name="Blue_Corner_Boxer",)
	numberOfRounds = models.IntegerField()
	matchNumber = models.IntegerField()
	wentToFinalRound = models.BooleanField()
	cornerJudge1Ruling = models.ForeignKey(User,on_delete=models.PROTECT,verbose_name="Corner Judge 1 Winner Pick User ID",related_name="Corner_Judge_1_Winner_Pick_User_ID",)
	cornerJudge2Ruling = models.ForeignKey(User,on_delete=models.PROTECT,verbose_name="Corner Judge 2 Winner Pick User ID",related_name="Corner_Judge_2_Winner_Pick_User_ID",)
	cornerJudge3Ruling = models.ForeignKey(User,on_delete=models.PROTECT,verbose_name="Corner Judge 3 Winner Pick User ID",related_name="Corner_Judge_3_Winner_Pick_User_ID",)
	cornerJudge4Ruling = models.ForeignKey(User,on_delete=models.PROTECT,verbose_name="Corner Judge 4 Winner Pick User ID",related_name="Corner_Judge_4_Winner_Pick_User_ID",)
	matchResultCode = models.CharField(choices=MATCH_RESULTS,max_length=30)
	winnerUserID = models.ForeignKey(User,on_delete=models.PROTECT,verbose_name="Winning Boxer UserID",related_name="Winning_Boxer_UserID",)

class MatchRound(models.Model):
	def __str__(self):
		return self
	MatchRoundID = models.AutoField(primary_key=True,)
	matchID = models.ForeignKey(Match,on_delete=models.PROTECT,verbose_name="Match ID",related_name="Match_ID",)
	roundNumber = models.IntegerField()
	redBoxerScore = models.IntegerField()
	blueBoxerScore = models.IntegerField()

class AvailabilitySchedule(models.Model):
	def __str__(self):
		return self
#	AvailabilityScheduleID = models.AutoField(primary_key=True,)
	user = models.OneToOneField(User,on_delete=models.CASCADE,verbose_name="User for Availability Schedule",related_name="User_for_Availability_Schedule",)
	callToConfirmAvailability = models.BooleanField()
	sundayAMAvailability = models.BooleanField()
	mondayAMAvailability = models.BooleanField()
	tuesdayAMAvailability = models.BooleanField()
	wednesdayAMAvailability = models.BooleanField()
	thursdayAMAvailability = models.BooleanField()
	fridayAMAvailability = models.BooleanField()
	saturdayAMAvailability = models.BooleanField()
	sundayPMAvailability = models.BooleanField()
	mondayPMAvailability = models.BooleanField()
	tuesdayPMAvailability = models.BooleanField()
	wednesdayPMAvailability = models.BooleanField()
	thursdayPMAvailability = models.BooleanField()
	fridayPMAvailability = models.BooleanField()
	saturdayPMAvailability = models.BooleanField()
	availableJanuary = models.BooleanField()
	availableFebruary = models.BooleanField()
	availableMarch = models.BooleanField()
	availableApril = models.BooleanField()
	availableMay = models.BooleanField()
	availableJune = models.BooleanField()
	availableJuly = models.BooleanField()
	availableAugust = models.BooleanField()
	availableSeptember = models.BooleanField()
	availableOctober = models.BooleanField()
	availableNovember = models.BooleanField()
	availableDecember = models.BooleanField()
	createdOn = models.DateTimeField(auto_now_add=True,null=True,)
	lastModified = models.DateTimeField(auto_now=True,null=True,)
