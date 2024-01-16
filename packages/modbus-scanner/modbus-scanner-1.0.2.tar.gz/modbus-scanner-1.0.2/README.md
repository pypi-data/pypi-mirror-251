# **Modbus Scanner**

### For RTU mode, you need to specify the serial port and baud rate.

    modbus_scanner -r 0 -f 3 -i 1 -e 10 -c rtu -h COM9 -b 9600 -s 1 -d 8 -p N -t 10

**OR**

### For TCP mode, you need to specify a host and port.

    modbus_scanner -r 0 -f 3 -i 1 -e 10 -c tcp -h 192.168.1.10 -l 502



- --register or -r : Register number to start scanning from. **Default is 0**.
- --fc or -f : Function code to use. **Default is 3**. 
- --start or -i : Starting address to scan from. **Default is 1**.
- --end or -e : Ending address to scan to. **Default is 254**.
- --conn_type or -c : Connection type to use. **Default is rtu**.
- --device or -h : Device to connect to. **(Required)**.

### Note: For RTU mode, this is the serial port. For TCP mode, this is the IP address.

- --port or -l : Port to connect to. **Default is 502**.
- --baud or -b : Baud rate to use. **Default is 9600**.
- --stop or -s : Stop bits to use. **Default is 1**.
- --data or -d : Data bits to use. **Default is 8**.
- --parity or -p : Parity to use. **Default is N**.
- --timeout or -t : Timeout to use. **Default is 60**.
