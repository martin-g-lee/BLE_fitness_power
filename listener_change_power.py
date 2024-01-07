import os
import socket
import asyncio
from bleak import BleakClient

MAC_ADDRESS = '4E40F0C6-DC5E-4A74-11F3-1119098E3BFA'
GATT_UUID = '00002ad9-0000-1000-8000-00805f9b34fb' # Fitness Machine Control Point

SOCKET_FILE_SET_BIKE_POWER = '/tmp/bike_power_level'

REQUEST_CONTROL_OP_CODE = 0x00
RESET_OP_CODE = 0x01
SET_TARGET_POWER_OP_CODE = 0x05


# remove old socket file if exists
if os.path.exists(SOCKET_FILE_SET_BIKE_POWER) :
  os.remove(SOCKET_FILE_SET_BIKE_POWER)
# create socket to listen for new power setting
listener = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
listener.bind(SOCKET_FILE_SET_BIKE_POWER)

async def run(address):
  async with BleakClient(address) as client:
    if (not client.is_connected):
      raise "client not connected"
    else:
      print ("Connected")

    def data_callback(handle, data):
      print(handle, data)

      
    await client.start_notify(GATT_UUID,data_callback)

# sit and wait until receive new message on socket
    while True:
      listener.listen()
      conn, addr = listener.accept()
      datagram = conn.recv(1024)
      if datagram:
        power_target = int.from_bytes(datagram)
        conn.close()

      print('Received new power target : ' + str(power_target) )

# go set new power setting on bike
      message = b"\x00"
      await client.write_gatt_char(GATT_UUID,message,response=True)
      await asyncio.sleep(0.5)

      message = b"\x01"
      await client.write_gatt_char(GATT_UUID,message,True)

      message = b"\x05"+ power_target.to_bytes(2, "little", signed=True)
      await client.write_gatt_char(GATT_UUID,message,True)

      

 ######                                                                                                                          
if __name__ == "__main__":
  loop = asyncio.get_event_loop()
  loop.run_until_complete(run(MAC_ADDRESS))
