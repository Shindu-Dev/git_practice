import re, datetime, pytz

from FightScheduler.models import StatusCode,AccountInfo,AccountType,Role,Address,Person,Organization,Service,AllowableService,Affiliation,PersonalInformation,Career,NonBoxerInfo,Waiver,WaiverRequirement,Signature,SignedWaiver,MedicalCert,ServiceEnrollment,MatchResultCode,Series,Show,Match,MatchRound,AvailabilitySchedule# @MODEL_IMPORTS@
from rest_framework import serializers
from datetime import datetime

localtz = pytz.timezone("America/Toronto")
#defaultDateTime = datetime.datetime(2010,1,1,0,0,0,0,localtz).isoformat()
defaultDateTime = datetime.now(localtz)
statusList = [str(StatusCode) for StatusCode in StatusCode.objects.values_list('StatusCode', flat=True)]

def validate_ip(ipAddress):
	if re.match("^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$", ipAddress) == None:
		raise serializers.ValidationError('This is not a valid IP.')

def validate_status(status):
	if not status in statusList:
		raise serializers.ValidationError('This is not a valid Status.')

############# Auto Generated Serializers follow #############################
class StatusCodeSerializer(serializers.HyperlinkedModelSerializer): #@DEFAULT@
	class Meta:
		model = StatusCode
		fields = ('StatusCode','statusCodeName','description')

class AccountTypeSerializer(serializers.HyperlinkedModelSerializer): #@DEFAULT@
	class Meta:
		model = AccountType
		fields = ('AccountTypeID','name','description')

class RoleSerializer(serializers.HyperlinkedModelSerializer): #@DEFAULT@
	class Meta:
		model = Role
		fields = ('RoleID','name','description')

class AddressSerializer(serializers.HyperlinkedModelSerializer): #@DEFAULT@
	class Meta:
		model = Address
		fields = ('AddressID','streetNumber','street','city','province','postalCode')

class PersonSerializer(serializers.HyperlinkedModelSerializer): #@DEFAULT@
	class Meta:
		model = Person
		fields = ('UserID','username','password','emailAddress','statusCode','accountTypeID','lastLoginDateTime')

class OrganizationSerializer(serializers.HyperlinkedModelSerializer): #@DEFAULT@
	class Meta:
		model = Organization
		fields = ('OrganizationID','organizationName','organizationShortName','physicalAddressID','mailingAddressID','clubOwnerUserID','clubPresidentUserID','clubCoachUserID','phoneNumber','website','email','additionalInsurees','clubMailRecipients','clubEmailRecipients')

class ServiceSerializer(serializers.HyperlinkedModelSerializer): #@DEFAULT@
	class Meta:
		model = Service
		fields = ('ServiceID','code','shortName','fullName','cost')

class AllowableServiceSerializer(serializers.HyperlinkedModelSerializer): #@DEFAULT@
	class Meta:
		model = AllowableService
		fields = ('AlowableServiceID','RoleID','ServiceID')

class AffiliationSerializer(serializers.HyperlinkedModelSerializer): #@DEFAULT@
	class Meta:
		model = Affiliation
		fields = ('AffiliationID','UserID','RoleID','affiliatedOrganizationID','affiliatedUserID')

class PersonalInformationSerializer(serializers.HyperlinkedModelSerializer): #@DEFAULT@
	class Meta:
		model = PersonalInformation
		fields = ('PersonInfoID','UserID','firstName','middleName','surname','addressID','businessPhone','phoneExtension','homePhone','cellPhone','fax','citizenship','clubName','genderCode','dateofBirth')

class CareerSerializer(serializers.HyperlinkedModelSerializer): #@DEFAULT@
	class Meta:
		model = Career
		fields = ('CareerID','UserID','amateurBouts','amateurWins','previousProfessionalCombatSportInvolvement','professionalYears','professionalBouts','professionalWins','previousCombatSportInvolvementInOtherCountry','previousYearsOutofCountry','previousBoutsOutofCountry','previousWinsOutofCountry','previousAmateurCombatSportInvolvement','previousAmateurBouts','previousAmateurWins','previousAmateurKOs','previousAmateurTKOs')

class NonBoxerInfoSerializer(serializers.HyperlinkedModelSerializer): #@DEFAULT@
	class Meta:
		model = NonBoxerInfo
		fields = ('NonBoxerInfoID','UserID','nccpNum','coachLevel','officialLevel','judgeOnlyPreference','policeRecordsCheckPerformed','policeRecordsCheckExpiry')

class WaiverSerializer(serializers.HyperlinkedModelSerializer): #@DEFAULT@
	class Meta:
		model = Waiver
		fields = ('WaiverID','name','description')

class WaiverRequirementSerializer(serializers.HyperlinkedModelSerializer): #@DEFAULT@
	class Meta:
		model = WaiverRequirement
		fields = ('WaiverRequirementID','roleID','annualRenewalRequired')

class SignatureSerializer(serializers.HyperlinkedModelSerializer): #@DEFAULT@
	class Meta:
		model = Signature
		fields = ('SignatureID','image','electronicSignature')

class SignedWaiverSerializer(serializers.HyperlinkedModelSerializer): #@DEFAULT@
	class Meta:
		model = SignedWaiver
		fields = ('SignedWaiverID','waiverID','waiverFormUserID','signatoryUserID','signatoryRole','signatureID','signatureDate','signatureLocation')

class MedicalCertSerializer(serializers.HyperlinkedModelSerializer): #@DEFAULT@
	class Meta:
		model = MedicalCert
		fields = ('MedicalCertID','UserID','date','image')

class ServiceEnrollmentSerializer(serializers.HyperlinkedModelSerializer): #@DEFAULT@
	class Meta:
		model = ServiceEnrollment
		fields = ('ServiceEnrollmentID','personID','serviceID','startDate','endDate')

class MatchResultCodeSerializer(serializers.HyperlinkedModelSerializer): #@DEFAULT@
	class Meta:
		model = MatchResultCode
		fields = ('MatchResultCode','description')

class SeriesSerializer(serializers.HyperlinkedModelSerializer): #@DEFAULT@
	class Meta:
		model = Series
		fields = ('SeriesID','name','organizationID')

class ShowSerializer(serializers.HyperlinkedModelSerializer): #@DEFAULT@
	class Meta:
		model = Show
		fields = ('ShowID','seriesID','organizingOrganizationID','addressID')

class MatchSerializer(serializers.HyperlinkedModelSerializer): #@DEFAULT@
	class Meta:
		model = Match
		fields = ('MatchID','refereeUserID','cornerJudge1UserID','cornerJudge2UserID','cornerJudge3UserID','cornerJudge4UserID','redBoxerUserID','blueBoxerUserID','numberOfRounds','wentToFinalRound','refereeRuling','cornerJudge1Ruling','cornerJudge2Ruling','cornerJudge3Ruling','cornerJudge4Ruling','matchResultCode','winnerUserID')

class MatchRoundSerializer(serializers.HyperlinkedModelSerializer): #@DEFAULT@
	class Meta:
		model = MatchRound
		fields = ('MatchRoundID','matchID','roundNumber','redBoxerScore','blueBoxerScore')


class StatusCodeSerializer(serializers.HyperlinkedModelSerializer): #@DEFAULT@
	class Meta:
		model = StatusCode
		fields = ('StatusCode','statusCodeName','description')

class AccountTypeSerializer(serializers.HyperlinkedModelSerializer): #@DEFAULT@
	class Meta:
		model = AccountType
		fields = ('AccountTypeID','name','description')

class RoleSerializer(serializers.HyperlinkedModelSerializer): #@DEFAULT@
	class Meta:
		model = Role
		fields = ('RoleID','name','description')

class AddressSerializer(serializers.HyperlinkedModelSerializer): #@DEFAULT@
	class Meta:
		model = Address
		fields = ('AddressID','streetNumber','street','city','province','postalCode')

class PersonSerializer(serializers.HyperlinkedModelSerializer): #@DEFAULT@
	class Meta:
		model = Person
		fields = ('UserID','username','password','emailAddress','statusCode','accountTypeID','lastLoginDateTime')

class OrganizationSerializer(serializers.HyperlinkedModelSerializer): #@DEFAULT@
	class Meta:
		model = Organization
		fields = ('OrganizationID','organizationName','organizationShortName','physicalAddressID','mailingAddressID','clubOwnerUserID','clubPresidentUserID','clubCoachUserID','phoneNumber','website','email','additionalInsurees','clubMailRecipients','clubEmailRecipients')

class ServiceSerializer(serializers.HyperlinkedModelSerializer): #@DEFAULT@
	class Meta:
		model = Service
		fields = ('ServiceID','code','shortName','fullName','cost')

class AllowableServiceSerializer(serializers.HyperlinkedModelSerializer): #@DEFAULT@
	class Meta:
		model = AllowableService
		fields = ('AlowableServiceID','RoleID','ServiceID')

class AffiliationSerializer(serializers.HyperlinkedModelSerializer): #@DEFAULT@
	class Meta:
		model = Affiliation
		fields = ('AffiliationID','UserID','RoleID','affiliatedOrganizationID','affiliatedUserID')

class PersonalInformationSerializer(serializers.HyperlinkedModelSerializer): #@DEFAULT@
	class Meta:
		model = PersonalInformation
		fields = ('PersonInfoID','UserID','firstName','middleName','surname','addressID','businessPhone','phoneExtension','homePhone','cellPhone','fax','citizenship','clubName','genderCode','dateofBirth')

class CareerSerializer(serializers.HyperlinkedModelSerializer): #@DEFAULT@
	class Meta:
		model = Career
		fields = ('CareerID','UserID','amateurBouts','amateurWins','previousProfessionalCombatSportInvolvement','professionalYears','professionalBouts','professionalWins','previousCombatSportInvolvementInOtherCountry','previousYearsOutofCountry','previousBoutsOutofCountry','previousWinsOutofCountry','previousAmateurCombatSportInvolvement','previousAmateurBouts','previousAmateurWins','previousAmateurKOs','previousAmateurTKOs')

class NonBoxerInfoSerializer(serializers.HyperlinkedModelSerializer): #@DEFAULT@
	class Meta:
		model = NonBoxerInfo
		fields = ('NonBoxerInfoID','UserID','nccpNum','coachLevel','officialLevel','judgeOnlyPreference','policeRecordsCheckPerformed','policeRecordsCheckExpiry')

class WaiverSerializer(serializers.HyperlinkedModelSerializer): #@DEFAULT@
	class Meta:
		model = Waiver
		fields = ('WaiverID','name','description')

class WaiverRequirementSerializer(serializers.HyperlinkedModelSerializer): #@DEFAULT@
	class Meta:
		model = WaiverRequirement
		fields = ('WaiverRequirementID','roleID','annualRenewalRequired')

class SignatureSerializer(serializers.HyperlinkedModelSerializer): #@DEFAULT@
	class Meta:
		model = Signature
		fields = ('SignatureID','image','electronicSignature')

class SignedWaiverSerializer(serializers.HyperlinkedModelSerializer): #@DEFAULT@
	class Meta:
		model = SignedWaiver
		fields = ('SignedWaiverID','waiverID','waiverFormUserID','signatoryUserID','signatoryRole','signatureID','signatureDate','signatureLocation')

class MedicalCertSerializer(serializers.HyperlinkedModelSerializer): #@DEFAULT@
	class Meta:
		model = MedicalCert
		fields = ('MedicalCertID','UserID','date','image')

class ServiceEnrollmentSerializer(serializers.HyperlinkedModelSerializer): #@DEFAULT@
	class Meta:
		model = ServiceEnrollment
		fields = ('ServiceEnrollmentID','personID','serviceID','startDate','endDate')

class MatchResultCodeSerializer(serializers.HyperlinkedModelSerializer): #@DEFAULT@
	class Meta:
		model = MatchResultCode
		fields = ('MatchResultCode','description')

class SeriesSerializer(serializers.HyperlinkedModelSerializer): #@DEFAULT@
	class Meta:
		model = Series
		fields = ('SeriesID','name','organizationID')

class ShowSerializer(serializers.HyperlinkedModelSerializer): #@DEFAULT@
	class Meta:
		model = Show
		fields = ('ShowID','seriesID','organizingOrganizationID','addressID')

class MatchSerializer(serializers.HyperlinkedModelSerializer): #@DEFAULT@
	class Meta:
		model = Match
		fields = ('MatchID','refereeUserID','cornerJudge1UserID','cornerJudge2UserID','cornerJudge3UserID','cornerJudge4UserID','redBoxerUserID','blueBoxerUserID','numberOfRounds','wentToFinalRound','refereeRuling','cornerJudge1Ruling','cornerJudge2Ruling','cornerJudge3Ruling','cornerJudge4Ruling','matchResultCode','winnerUserID')

class MatchRoundSerializer(serializers.HyperlinkedModelSerializer): #@DEFAULT@
	class Meta:
		model = MatchRound
		fields = ('MatchRoundID','matchID','roundNumber','redBoxerScore','blueBoxerScore')


class StatusCodeSerializer(serializers.HyperlinkedModelSerializer): #@DEFAULT@
	class Meta:
		model = StatusCode
		fields = ('StatusCode','statusCodeName','description')

class AccountInfoSerializer(serializers.HyperlinkedModelSerializer): #@DEFAULT@
	class Meta:
		model = AccountInfo
		fields = ('AccountInfoID','username','registrationStage','isBoxer','isCoach','isOwner','isOfficial','isBoxingOntarioAdmin')

class AccountTypeSerializer(serializers.HyperlinkedModelSerializer): #@DEFAULT@
	class Meta:
		model = AccountType
		fields = ('AccountTypeID','name','description')

class RoleSerializer(serializers.HyperlinkedModelSerializer): #@DEFAULT@
	class Meta:
		model = Role
		fields = ('RoleID','name','description')

class AddressSerializer(serializers.HyperlinkedModelSerializer): #@DEFAULT@
	class Meta:
		model = Address
		fields = ('AddressID','streetNumber','street','city','province','postalCode','createdOn','lastModified')

class PersonSerializer(serializers.HyperlinkedModelSerializer): #@DEFAULT@
	class Meta:
		model = Person
		fields = ('PersonID','username','password','emailAddress','statusCode','accountTypeID','lastLoginDateTime','createdOn','lastModified')

class OrganizationSerializer(serializers.HyperlinkedModelSerializer): #@DEFAULT@
	class Meta:
		model = Organization
		fields = ('OrganizationID','organizationName','organizationShortName','physicalAddressID','mailingAddressID','clubOwnerUserID','clubPresidentUserID','clubCoachUserID','phoneNumber','website','email','additionalInsurees','clubMailRecipients','clubEmailRecipients','createdOn','lastModified')

class ServiceSerializer(serializers.HyperlinkedModelSerializer): #@DEFAULT@
	class Meta:
		model = Service
		fields = ('ServiceID','code','shortName','fullName','cost','createdOn','lastModified')

class AllowableServiceSerializer(serializers.HyperlinkedModelSerializer): #@DEFAULT@
	class Meta:
		model = AllowableService
		fields = ('AlowableServiceID','RoleID','ServiceID')

class AffiliationSerializer(serializers.HyperlinkedModelSerializer): #@DEFAULT@
	class Meta:
		model = Affiliation
		fields = ('AffiliationID','UserID','RoleID','affiliatedOrganizationID','affiliatedUserID')

class PersonalInformationSerializer(serializers.HyperlinkedModelSerializer): #@DEFAULT@
	class Meta:
		model = PersonalInformation
		fields = ('PersonInfoID','UserID','addressID','businessPhone','phoneExtension','homePhone','cellPhone','fax','citizenship','clubName','genderCode','height','dateofBirth','createdOn','lastModified')

class CareerSerializer(serializers.HyperlinkedModelSerializer): #@DEFAULT@
	class Meta:
		model = Career
		fields = ('CareerID','UserID','currentWeight','amateurBouts','amateurWins','previousProfessionalCombatSportInvolvement','professionalYears','professionalBouts','professionalWins','previousCombatSportInvolvementInOtherCountry','previousYearsOutofCountry','previousBoutsOutofCountry','previousWinsOutofCountry','previousAmateurCombatSportInvolvement','previousAmateurBouts','previousAmateurWins','previousAmateurKOs','previousAmateurTKOs','createdOn','lastModified')

class NonBoxerInfoSerializer(serializers.HyperlinkedModelSerializer): #@DEFAULT@
	class Meta:
		model = NonBoxerInfo
		fields = ('NonBoxerInfoID','UserID','nccpNum','coachLevel','officialLevel','judgeOnlyPreference','policeRecordsCheckPerformed','policeRecordsCheckExpiry')

class WaiverSerializer(serializers.HyperlinkedModelSerializer): #@DEFAULT@
	class Meta:
		model = Waiver
		fields = ('WaiverID','name','description')

class WaiverRequirementSerializer(serializers.HyperlinkedModelSerializer): #@DEFAULT@
	class Meta:
		model = WaiverRequirement
		fields = ('WaiverRequirementID','roleID','annualRenewalRequired')

class SignatureSerializer(serializers.HyperlinkedModelSerializer): #@DEFAULT@
	class Meta:
		model = Signature
		fields = ('SignatureID','image','electronicSignature')

class SignedWaiverSerializer(serializers.HyperlinkedModelSerializer): #@DEFAULT@
	class Meta:
		model = SignedWaiver
		fields = ('SignedWaiverID','waiverID','waiverFormUserID','signatoryUserID','signatoryRole','signatureID','signatureDate','signatureLocation')

class MedicalCertSerializer(serializers.HyperlinkedModelSerializer): #@DEFAULT@
	class Meta:
		model = MedicalCert
		fields = ('MedicalCertID','UserID','date','image')

class ServiceEnrollmentSerializer(serializers.HyperlinkedModelSerializer): #@DEFAULT@
	class Meta:
		model = ServiceEnrollment
		fields = ('ServiceEnrollmentID','UserID','serviceID','startDate','endDate')

class MatchResultCodeSerializer(serializers.HyperlinkedModelSerializer): #@DEFAULT@
	class Meta:
		model = MatchResultCode
		fields = ('MatchResultCode','description')

class SeriesSerializer(serializers.HyperlinkedModelSerializer): #@DEFAULT@
	class Meta:
		model = Series
		fields = ('SeriesID','name','organizationID')

class ShowSerializer(serializers.HyperlinkedModelSerializer): #@DEFAULT@
	class Meta:
		model = Show
		fields = ('ShowID','seriesID','organizingOrganizationID','addressID')

class MatchSerializer(serializers.HyperlinkedModelSerializer): #@DEFAULT@
	class Meta:
		model = Match
		fields = ('MatchID','refereeUserID','cornerJudge1UserID','cornerJudge2UserID','cornerJudge3UserID','cornerJudge4UserID','redBoxerUserID','blueBoxerUserID','numberOfRounds','wentToFinalRound','refereeRuling','cornerJudge1Ruling','cornerJudge2Ruling','cornerJudge3Ruling','cornerJudge4Ruling','matchResultCode','winnerUserID')

class MatchRoundSerializer(serializers.HyperlinkedModelSerializer): #@DEFAULT@
	class Meta:
		model = MatchRound
		fields = ('MatchRoundID','matchID','roundNumber','redBoxerScore','blueBoxerScore')

class AvailabilityScheduleSerializer(serializers.HyperlinkedModelSerializer): #@DEFAULT@
	class Meta:
		model = AvailabilitySchedule
		fields = ('AvailabilityScheduleID','user','callToConfirmAvailability','sundayAMAvailability','mondayAMAvailability','tuesdayAMAvailability','wednesdayAMAvailability','thursdayAMAvailability','fridayAMAvailability','saturdayAMAvailability','sundayPMAvailability','mondayPMAvailability','tuesdayPMAvailability','wednesdayPMAvailability','thursdayPMAvailability','fridayPMAvailability','saturdayPMAvailability','availableJanuary','availableFebruary','availableMarch','availableApril','availableMay','availableJune','availableJuly','availableAugust','availableSeptember','availableOctober','availableNovember','availableDecember')

