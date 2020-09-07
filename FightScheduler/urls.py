from . import views #
from django.contrib import admin
from django.urls import include, path
from django.conf.urls import url, include
from django.conf.urls.i18n import i18n_patterns
#from .views home, home_files
from FightScheduler.models import StatusCode,AccountType,Role,Address,Person,Organization,Service,AllowableService,Affiliation,PersonalInformation,Career,NonBoxerInfo,Waiver,WaiverRequirement,Signature,SignedWaiver,MedicalCert,ServiceEnrollment,MatchResultCode,Series,Show,Match,MatchRound# @MODEL_IMPORTS@
from rest_framework import routers, serializers, viewsets



# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
# @START - REGISTER DEFAULT VIEWS@
router.register(r'StatusCode', views.StatusCodeViewSet)
router.register(r'AccountType', views.AccountTypeViewSet)
router.register(r'Role', views.RoleViewSet)
router.register(r'Address', views.AddressViewSet)
router.register(r'Person', views.PersonViewSet)
router.register(r'Organization', views.OrganizationViewSet)
router.register(r'Service', views.ServiceViewSet)
router.register(r'AllowableService', views.AllowableServiceViewSet)
router.register(r'Affiliation', views.AffiliationViewSet)
router.register(r'PersonalInformation', views.PersonalInformationViewSet)
router.register(r'Career', views.CareerViewSet)
router.register(r'NonBoxerInfo', views.NonBoxerInfoViewSet)
router.register(r'Waiver', views.WaiverViewSet)
router.register(r'WaiverRequirement', views.WaiverRequirementViewSet)
router.register(r'Signature', views.SignatureViewSet)
router.register(r'SignedWaiver', views.SignedWaiverViewSet)
router.register(r'MedicalCert', views.MedicalCertViewSet)
router.register(r'ServiceEnrollment', views.ServiceEnrollmentViewSet)
router.register(r'MatchResultCode', views.MatchResultCodeViewSet)
router.register(r'Series', views.SeriesViewSet)
router.register(r'Show', views.ShowViewSet)
router.register(r'Match', views.MatchViewSet)
router.register(r'MatchRound', views.MatchRoundViewSet)
# @END - REGISTER DEFAULT VIEWS@

app_name = 'fightscheduler'
urlpatterns = [
	path('i18n/', include('django.conf.urls.i18n')),
	path('', views.main, name='main'),
	path('main', views.main, name='main'),
	path('languageSelector/<str:langCode>/', views.languageSelector, name='languageSelector'),
    path('<int:pk>/personDetailView', views.PersonView.as_view(), name='personDetailView'),
    path('personCreate/', views.PersonCreate.as_view(), name='personCreate'),
    path('personUpdate/', views.PersonUpdate.as_view(), name='personUpdate'),
    path('personalInfoCreate/', views.PersonalInfoCreate.as_view(), name='personalInfoCreate'),
    path('personalInfoUpdate/', views.PersonalInfoUpdate.as_view(), name='personalInfoUpdate'),
    path('careerCreate/', views.CareerCreate.as_view(), name='careerCreate'),
    path('careerUpdate/', views.CareerUpdate.as_view(), name='careerUpdate'),
    path('otherInfoCreate/', views.OtherInfoCreate.as_view(), name='otherInfoCreate'),
    path('otherInfoUpdate/', views.OtherInfoUpdate.as_view(), name='otherInfoUpdate'),
    #path('showCreate/', views.ShowCreate.as_view(), name='showCreate'),
	path('matchCreate/', views.MatchCreate.as_view(), name='matchCreate'),
    path('matchUpdate/', views.MatchUpdate.as_view(), name='matchUpdate'),
	path('availabilityCreate/', views.AvailabilityScheduleCreate.as_view(), name='availabilityCreate'),
    path('availabilityUpdate/', views.AvailabilityScheduleUpdate.as_view(), name='availabilityUpdate'),

	path('<int:pk>/editPersonalInformation/', views.editPersonalInformation, name='editPersonalInformation'),
	path('registerClub/', views.clubRegistration, name='clubRegistration'),
	path('editProfile/<int:pk>/', views.editProfile, name='editProfile'),
	path('editClubDetails/<int:organizationID>/', views.editClubDetails, name='editClubDetails'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^', include(router.urls)),

    path('index/', views.IndexView.as_view(), name='index'),

    # ex: /polls/5/
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    # ex: /polls/5/results/
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    # ex: /polls/5/vote/
    path('<int:question_id>/vote/', views.vote, name='vote'),

]

#Add Django site authentication urls (for login, logout, password management)

urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
]
