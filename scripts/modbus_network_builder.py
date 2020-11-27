import json

import requests

ip = "0.0.0.0"
port = 1515

url = f'http://{ip}:{port}/api'
network_url = f'{url}/modbus/networks'
devices_url = f'{url}/modbus/devices'
# devices = (1,2)
devices = (5, 6, 7, 8, 9, 10, 11, 12, 13, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31)
reg_type = "READ_HOLDING_REGISTERS"
data_type = "RAW"
points_url = f'{url}/modbus/points'
reg_address = [6, 7, 8, 10, 39]
reg_names = ['mode', 'fan_status', 'setpoint', 'temp', 'value_position']

# test device
# 7 - Mode
# 8 - Fan Status
# 9- Setpoint
# 11 - Temp
# 40 - Valve position

'''
make a device
get the UUID
make the points
start again
'''
network_obj = {
    "name": "mod_network_name hey",
    "type": "RTU",
    "enable": True,
    "timeout": 0.1,
    "device_timeout_global": 1,
    "point_timeout_global": 1,
    "rtu_port": "/dev/ttyUSB2",
    "rtu_speed": 9600,
    "rtu_stop_bits": 1,
    "rtu_parity": "N",
    "rtu_byte_size": 8
}

r_n = requests.post(f'{network_url}', data=network_obj)
print(r_n)
r_json = r_n.json()
print(r_json)
n_uuid = r_json['uuid']
network_uuid = n_uuid

for d in devices:

    devices_obj = {
        "name": f'device_{d}',
        "enable": True,
        "type": "RTU",
        "address": d,
        "ping_point_type": "mod_ping_point_type",
        "ping_point_address": 1,
        "zero_mode": False,
        "timeout": 123,
        "timeout_global": False,
        "network_uuid": network_uuid
    }

    r_d = requests.post(f'{devices_url}', data=devices_obj)
    r_json = r_d.json()
    print(r_json)
    d_uuid = r_json['uuid']
    for i, r in enumerate(reg_address):
        name = reg_names[i]
        point_obj = {
            "name": f'{name}_{d}_{r}',
            "register": r,
            "register_length": 2,
            "function_code": reg_type,
            "enable": True,
            "cov_threshold": 1,
            "write_value": 0,
            "data_type": data_type,
            "data_endian": "BEB_BEW",
            "device_uuid": d_uuid
        }
        # print(point_obj)
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        r_p = requests.post(f'{points_url}', data=json.dumps(point_obj), headers=headers)
        r_json = r_p.json()
        print(r_json)
