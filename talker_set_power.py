import os
import socket
import sys 
import time

SOCKET_FILE_SET_BIKE_POWER = '/tmp/bike_power_level'

power_list= [80,180]

# wait for the listener to create socket
while not os.path.exists(SOCKET_FILE_SET_BIKE_POWER):
    time.sleep(1)

# iterate through values
for power_level in power_list:

# pass the value to the socket
    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as talker:
        talker.connect(SOCKET_FILE_SET_BIKE_POWER)
        print("Setting power level to :" + str(power_level) + "w")
        message=power_level.to_bytes()
        talker.send(message)
        talker.close()

# wait a while before next value
        print("Waiting 10 secs")
        time.sleep(10)
