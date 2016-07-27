
#!/usr/bin/env python

# Imports required for python
import RPi.GPIO as GPIO
import time
import json
import requests

# GPIO Pins
TRIG = 11
ECHO = 12

# M2X Variables
action='/streams/Tilt/value'   # Action for updating a stream with data
dev0ID='0822f9669e2e02b2d3d12d6dc373197f'
h1={'X-M2X-KEY': '5c38b1e5fea93bcbfa33d11ff292e81a'}
h2={'X-M2X-KEY': '5c38b1e5fea93bcbfa33d11ff292e81a', 'Content-Type': 'application/json'}
url='http://api-m2x.att.com/v2/devices/'
jsonp='?pretty=true'                         # Add this to request to force json response in pretty format

#Loop Variables
i=0
snooze=20                                    # Delay in seconds .

def setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(TRIG, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)

def distance():
    GPIO.output(TRIG, 0)
    time.sleep(0.000002)

    GPIO.output(TRIG, 1)
    time.sleep(0.00001)
    GPIO.output(TRIG, 0)

	
    while GPIO.input(ECHO) == 0:
        a = 0
        time1 = time.time()
    while GPIO.input(ECHO) == 1:
        a = 1
        time2 = time.time()

    during = time2 - time1
    return during * 340 / 2 * 100

def measureavg():
    dislist=[]
    count=0
    while count<10:
        dis = distance()
        time.sleep(0.1)
        count=count+1
        dislist.append(dis)
        avg=float(sum(dislist))/len(dislist)
        print 'avg: ',avg
        return avg



       
        
        
def destroy():
    GPIO.cleanup()



		#Next Sectionfocuses on POSTing to M2X Server
	#from API Cheatsheet
	#Updating a specific streams current value...
	#curl -i -X PUT http://api-m2x.att.com/v2/devices/0822f9669e2e02b2d3d12d6dc373197f/streams/Tilt/values-H "X-M2X-KEY: 5c38b1e5fea93bcbfa33d11ff292e81a" -H "Content-Type: application/json" -d '{ "value": "40" }'

def post(avg):
    


    data1={'value': avg }

    while True:       #establish a loop to attempt to POST data
        print 'post lopp'
        try:
            response = requests.put(url+dev0ID+action+jsonp, data=json.dumps(data1), headers=h2)
	
            if (response.status_code) == 202:
                print response.status_code
                print 'Posted new value=', avg ,'to stream.   Accepted.\n'
            else:
		        print 'Response not 202...Error!!!  \n'
                #print 'response.text gives:\n'
                #print response.text
        except:      #Error handling, such as wifi connection dropped
            print 'post Exception raised: '
	    time.sleep(20)    #give connection some time to reconnect
        else:
            break       #break the loop here since we believe data got posted correctly
 
 



if __name__ == "__main__":
    setup()
    for i in range(168):
        i=i+1
        avg=measureavg()
        post(avg)
        time.sleep(snooze)
