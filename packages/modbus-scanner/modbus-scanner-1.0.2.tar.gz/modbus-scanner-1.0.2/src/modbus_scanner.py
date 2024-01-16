import sys
import getopt
from pymodbus.constants import Endian
from pymodbus.client import ModbusTcpClient, ModbusSerialClient
from pymodbus.payload import BinaryPayloadDecoder

# PARAMS in ARGS → device, baud, stop bit, data bit, parity, timeout, conn_type, port.

conn_type = ''
device = ''
port = 502
baud = 9600
stop = 1
data = 8
parity = 'N'
timeout = 60

config = {}
register = 0
start_id = 1
end_id = 254
function_code = 3


def get_arg():
    global conn_type, device, port, baud, stop, data, parity, timeout, register, start_id, end_id, function_code
    argv = sys.argv[1:]
    try:
        opts, args = getopt.getopt(argv, "r:f:i:e:c:h:l:b:s:d:p:t:",
                                   ["register=", "fc=", "start=", "end=", "conn_type=", "device=", "port=", "baud=",
                                    "stop=", "data=", "parity=", "timeout="])
    except getopt.GetoptError:
        print(
            'modbus_scanner.py (Required) -r <register> -fc <fc> -sid <start> -eid <end> -c <conn_type> -d <device> (For TCP) -p <port> (For RTU) -b <baud> -sb <stop> -db <data> -r <parity> -t <timeout>')
        sys.exit(2)

    print("opts: {}".format(opts))
    for opt, arg in opts:
        if opt == '-r':
            print("Register: {}".format(arg))
            register = int(arg)
        elif opt == '-f':
            print("Function Code: {}".format(arg))
            function_code = int(arg)
        elif opt == '-i':
            print("Start ID: {}".format(arg))
            start_id = int(arg)
        elif opt == '-e':
            print("End ID: {}".format(arg))
            end_id = int(arg)
        elif opt == '-c':
            print("Connection Type: {}".format(arg))
            conn_type = arg
        elif opt == '-h':
            print("Device: {}".format(arg))
            device = arg
        elif opt == '-l':
            print("Port: {}".format(arg))
            port = int(arg)
        elif opt == '-b':
            print("Baud: {}".format(arg))
            baud = int(arg)
        elif opt == '-s':
            print("Stop: {}".format(arg))
            stop = int(arg)
        elif opt == '-d':
            print("Data: {}".format(arg))
            data = int(arg)
        elif opt == '-p':
            print("Parity: {}".format(arg))
            parity = arg
        elif opt == '-t':
            print("Timeout: {}".format(arg))
            timeout = int(arg)


def scan():
    global start_id, end_id, register, function_code
    if register == '':
        print("Register is required")
        exit(1)
    if function_code == '':
        print("No Function Code provided, using default: 3")
    if start_id == '':
        print("No Start ID provided, using default: 1")
    if end_id == '':
        print("No End ID provided, using default: 254")
    if conn_type == '':
        print("Type is required")
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
        client = ModbusTcpClient(device, port)
    elif conn_type == 'rtu':
        print("Scanning {} device on {} baud, {} stop, {} data, {} parity".format(device, baud, stop, data, parity))
        client = ModbusSerialClient(method='rtu', port=device, baudrate=int(baud), stopbits=int(stop),
                                    bytesize=int(data),
                                    parity=parity, retries=1)
    else:
        print("Type not supported")
        exit(1)

    recognized_ids = []

    client.connect()

    print("Client Connected: {}".format(client.is_active()))
    print("Scanning IDs from {} to {}".format(start_id, end_id))
    print("register: {}".format(register))
    for i in range(start_id, end_id + 1):
        try:
            resp = ''
            print("Reading ID: {}".format(i))
            result = ''
            if function_code == 3:
                result = client.read_holding_registers(register, 2, i)
            elif function_code == 4:
                result = client.read_input_registers(register, 2, i)
            decoder = BinaryPayloadDecoder.fromRegisters(result.registers[0:2], byteorder=Endian.BIG,
                                                         wordorder=Endian.BIG)
            resp = decoder.decode_16bit_int()
            if resp != '':
                print("Recognized ID: {} - Value: {} at {}".format(i, decoder.decode_16bit_int(), register))
                recognized_ids.append(i)
        except Exception as e:
            print("ID: {} - Error: {}".format(i, e))
            continue
    print("Recognized IDs: {}".format(recognized_ids))


def main():
    get_arg()
    scan()


if __name__ == "__main__":
    main()

