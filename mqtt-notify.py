#!/usr/bin/python
import sys
import time
import os
import string
import random
import dbus
import paho.mqtt.client as mqtt

def read_credentials_file(filename):
    f = open(filename)
    return f.readline().strip(), f.readline().strip()

mqtt_name = "sailfish_iot_"+''.join(random.choice(string.ascii_lowercase + string.digits) for i in xrange(8))
mqtt_server = "yourserver.com"
mqtt_port = 1883
mqtt_keepalive = 210
# Note: getting the will wrong will make your connection fail authentication!
mqtt_set_will = False
mqtt_credentials = os.path.expanduser("~/.mqtt_auth")
mqtt_user, mqtt_password = read_credentials_file(mqtt_credentials)
mqtt_topic_base = "nemopush/"+mqtt_user+"/"

print "starting MQTT notification client!"
print "Press CTRL + C to exit"

def on_log(mosq, obj, level, string):
    print(string)

def on_connect(mosq, userdata, rc):
    if rc == 0:
        print("Connected to: "+mqtt_server)
        for file in os.listdir("/usr/share/lipstick/notificationcategories"):
            if file.startswith("x-nemopush."):
                category = file.replace('.conf','')
                mqttc.subscribe(mqtt_topic_base+category+"/notifications", 2)
                mqttc.publish(mqtt_topic_base+category+"/receiver_state", "connected", 0, True)
    else:
        print("Connection failed with error code: "+str(rc))

# Note: In case you are connecting to an older version of Mosquitto, you'll need to set this to mqtt.MQTTv31!
mqttc = mqtt.Client(mqtt_name, False, None, mqtt.MQTTv311 )

mqttc.username_pw_set(mqtt_user, mqtt_password)
mqttc.on_log = on_log
mqttc.on_connect = on_connect
if mqtt_set_will: mqttc.will_set(mqtt_topic_base+"irssi/receiver_state", None, 0, True)
# Setting reconnect delay is currently not supported by paho
#mqttc.reconnect_delay_set(1, 300, True)
mqttc.connect(mqtt_server, mqtt_port, mqtt_keepalive)

def on_message(mosq, obj, msg):
    print("Message received on topic "+msg.topic+" with QoS "+str(msg.qos)+" and payload "+msg.payload)
    topic = msg.topic.split('/')
    notification = msg.payload.split('\n')
    category = topic[2].split('.')
    try:
        interface.Notify(category[2],
                 0,
                 "",
                 notification[0],
                 notification[1],
                 dbus.Array(["default", ""]),
                 dbus.Dictionary({"category": topic[2],
                             "x-nemo-preview-body": notification[1],
                             "x-nemo-preview-summary": notification[0]},
                             signature='sv'),
                 0)
    except dbus.exceptions.DBusException:
        print("Failed sending DBus notification.")

mqttc.on_message = on_message

bus = dbus.SessionBus()
object = bus.get_object('org.freedesktop.Notifications','/org/freedesktop/Notifications')
interface = dbus.Interface(object,'org.freedesktop.Notifications')


mqttc.loop_forever()

