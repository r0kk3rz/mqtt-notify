# mqtt-notify
Push Notification Daemon for Lipstick based Mobile systems

Based upon [irssi-mqtt-sailfish](https://github.com/dm8tbr/irssi-mqtt-sailfish) and 
modified to allow multiple applications or types of notifications to be raised

The daemon will look for sailfish notification category definitions in 
/usr/share/lipstick/notificationcategories for any config starting with x-nemopush and 
subscribe to a MQTT channel based upon that name.

eg. if you had a x-nemopush.messaging.example.conf, the daemon will subscribe 
to nemopush/[user]/x-nemopush.messaging.example/notifications on the MQTT broker


To set up:
```
echo #myusername# > ~/.mqtt_auth
echo #password# >> ~/.mqtt_auth
```

edit mqtt-notify.py with your mqtt broker details

copy mqtt-notify.service to /home/nemo/.config/systemd/user
```
systemctl --user enable mqtt-notify
systemctl --user start mqtt-notify
``` 

