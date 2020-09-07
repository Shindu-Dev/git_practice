import requests, datetime, pytz, re, os, json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()

from django.shortcuts import render
from workerManager.models import RigType, Status

localtz = pytz.timezone("America/Toronto")
defDateTime = datetime.datetime(2016,1,1,0,0,0,0,localtz).isoformat()
#formatted = datetime.datetime.strftime(defaultDateTime, '%Y-%m-%dT%H:%M:%S')

#payload = {'name': 'testRig1', 'ip': '12.22.12.22', 'rigType': 'Unknown-Unknown', 'rigStatus': 'NEW-New', 'minerStatus': 'NEW-New', 'claymoreLogCreationDate': defaultDateTime, 'claymoreLogLastUpdate': defaultDateTime, 'claymoreLogOffset': 0, 'claymoreLogOffsetDate': defaultDateTime, 'speedfanLogCreationDate': defaultDateTime, 'speedfanLogLastUpdate': defaultDateTime, 'speedfanLogOffset': 0, 'speedfanLogOffsetDate': defaultDateTime}

#response = requests.post('http://127.0.0.1:8000/workerManager/rigs/', data=payload)

########### SAMPLE PUT
headers = {'Content-Type': 'application/json'}

#payload = {'name': 'testRig2', 'ip': '12.22.12.22', 'rigType': rigType, 'rigStatus': statusNew, 'rigStatus': statusNew, 'claymoreLogCreationDate': defaultDateTime, 'claymoreLogLastUpdate': defaultDateTime, 'claymoreLogOffset': 0, 'claymoreLogOffsetDate': defaultDateTime, 'speedfanLogCreationDate': defaultDateTime, 'speedfanLogLastUpdate': defaultDateTime, 'speedfanLogOffset': 0, 'speedfanLogOffsetDate': defaultDateTime}

statusNew = Status.objects.get(code='NEW')
rigType = RigType.objects.get(name='Unknown')
rigStatusNew = Status.objects.get(code='NEW')

#response = requests.get('http://127.0.0.1:8000/workerManager/rigType/')
#geodata = response.json()
#print(geodata)


payload = {
	'name': 'finalTest2', 
	'ip': '12.22.12.22', 
	'rigType': 'Unknown', 
	'rigStatus': 'NEW',
	'claymoreLogCreationDate': defDateTime, 
	'claymoreLogLastUpdate': defDateTime, 
	'claymoreLogOffset': 0, 
	'claymoreLogOffsetDate': defDateTime, 
	'speedfanLogCreationDate': defDateTime,
	'speedfanLogLastUpdate': defDateTime, 
	'speedfanLogOffset': 0, 
	'speedfanLogOffsetDate': defDateTime, 
}

#payload = {	"name": "testRig2", "ip": "12.22.12.22" }

print (payload)

response = requests.post('http://127.0.0.1:8000/workerManager/rigs/', json=payload, headers=headers)
#response = requests.get('http://127.0.0.1:8000/workerManager/rigs/')
print(response.json())

########### SAMPLE POST

#payload = {"name": "Test", "description": "Test"}
#response = requests.post('http://127.0.0.1:8000/workerManager/rigType/', json=payload, headers=headers)
#print(response.reason)

########### SAMPLE GET

#response = requests.get('http://127.0.0.1:8000/workerManager/rigs/')
#geodata = response.json()
#print(geodata)
