import sys
import getopt
import asyncio
import yaml
from pymodbus.constants import Endian
from pymodbus.client import ModbusTcpClient, ModbusSerialClient, AsyncModbusTcpClient, AsyncModbusSerialClient
from pymodbus.payload import BinaryPayloadDecoder, BinaryPayloadBuilder

# PARAMS in ARGS → device, baud, stop bit, data bit, parity, timeout, conn_type, port.

conn_type = ''
device = ''
port = 502
baud = ''
stop = ''
data = ''
parity = ''
timeout = 60
config = {}
register = 0
start_id = 1
end_id = 254
function_code = 3


def get_arg():
	global conn_type, device, port, baud, stop, data, parity, timeout , register , start_id , end_id , function_code
	argv = sys.argv[1:]
	try:
		opts, args = getopt.getopt(argv, "r:fc:sid:eid:c:d:p:b:sb:db:r:t:",
		                           ["register=","fc=","start=","end=","conn_type=", "device=", "port=", "baud=", "stop=", "data=", "parity=", "timeout="])
	except getopt.GetoptError:
		print(
			'modbus_scanner.py (Required) -r <register> -fc <fc> -sid <start> -eid <end> -c <conn_type> -d <device> (For TCP) -p <port> (For RTU) -b <baud> -sb <stop> -db <data> -r <parity> -t <timeout>')
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-r':
			register = int(arg)
		elif opt == '-fc':
			function_code = int(arg)
		elif opt == '-sid':
			start_id = int(arg)
		elif opt == '-eid':
			end_id = int(arg)
		elif opt == '-c':
			conn_type = arg
		elif opt == '-d':
			device = arg
		elif opt == '-p':
			port = int(arg)
		elif opt == '-b':
			baud = int(arg)
		elif opt == '-sb':
			stop = int(arg)
		elif opt == '-db':
			data = int(arg)
		elif opt == '-r':
			parity = arg
		elif opt == '-t':
			timeout = int(arg)

get_arg()

if register == '':
	print("Register is required")
	exit(1)
if function_code == '':
	print("Function Code is required")
	exit(1)
if start_id == '':
	print("No Start ID provided, using default: 1")
if end_id == '':
	print("No End ID provided, using default: 254")
if conn_type == '':
	print("Connection Type is required")
	exit(1)
if device == '':
	print("Device is required")
	exit(1)

if conn_type == 'rtu':
	if baud == '':
		print("Baud is required")
		exit(1)
	if stop == '':
		print("Stop is required")
		exit(1)
	if data == '':
		print("Data is required")
		exit(1)
	if parity == '':
		print("Parity is required")
		exit(1)

if conn_type == 'tcp':
	if port == '':
		print("Port is required")
		exit(1)

print("Starting Client For Connection Type: {}".format(conn_type))
if conn_type == 'tcp':
	print("Scanning {} device on {} port".format(device, port))
	client = AsyncModbusTcpClient(device, port)
elif conn_type == 'rtu':
	client = AsyncModbusSerialClient(method='rtu', port=device, baudrate=int(baud), stopbits=int(stop),
	                            bytesize=int(data),
	                            parity=parity,
	                            timeout=timeout)
else:
	print("Type not supported")
	exit(1)

recognized_ids = []


async def scan():
	global client, start_id, end_id, register, recognized_ids
	await client.connect()

	print("Client Connected: {}".format( client.is_active()))
	print("Scanning IDs from {} to {}".format(start_id, end_id))
	print("register: {}".format(register))
	for i in range(start_id, end_id):
		try:
			print("Reading ID: {}".format(i))
			result = await client.read_holding_registers(register, 2, i)
			decoder = BinaryPayloadDecoder.fromRegisters(result.registers[0:2], byteorder=Endian.BIG, wordorder=Endian.BIG)
			if decoder.decode_16bit_int():
				recognized_ids.append(i)
			print("ID: {} - Value: {} at {}".format(i, decoder.decode_16bit_int(), register))
		except Exception as e:
			print("ID: {} - Error: {}".format(i, e))
			continue

asyncio.run(scan())

print("Recognized IDs: {}".format(recognized_ids))