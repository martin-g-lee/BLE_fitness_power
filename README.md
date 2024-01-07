# BLE_fitness_power
Setting the power setting on a fitness machine via bluetooth and a socket

Proof of concept Python code to write bike power setting to a fitness machine object.

The listener establishes a UNIX Domain Socket to receive power setting values and establishes a Bluetooth Low Energy (BLE) Generic Attribute Profile (GATT) connection to the Fitness Machine Control Point service. 
The listener waits for a value to be sent to the socket, then uses this value to set the power level required (in watts) on the fitness machine.

Example
python3 listener_change_power.py &
python3 talker_set_power.py &

Caveats
This is proof of concept code. It works with my Wahoo Kick Core, it may not work with any other device. 
There is little in the way of error checking and no sanity checking. Out of bounds values may damage your device or harm someone using it.
Use at your own risk and discretion.
