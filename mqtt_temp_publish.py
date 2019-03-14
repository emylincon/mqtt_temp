import os
import glob
import time
import paho.mqtt.client as mqtt


os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

client = mqtt.Client()

os.system('clear')
print('--------------------------------------')
print('Welcome to MQTT Temperature Publisher')
print('--------------------------------------')
username = input('Username of Broker: ').strip()
password = input('Password of Broker: ').strip()
broker_ip = input("Broker's IP: ").strip()
broker_port_no = int(input("Broker's Port no: ").strip())
topic_ = input("Topic: ").strip()
print('--------------------------------------')

client.username_pw_set(username, password)
client.connect(broker_ip, broker_port_no, 60)


def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines


def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos + 2:]
        temp_c = float(temp_string) / 1000.0
        # temp_f = temp_c * 9.0 / 5.0 + 32.0
        print("Temp: {}C".format(temp_c))
        publish_temp(temp_c)


def publish_temp(temp):
    client.publish(topic_, 'Temp: {}'.format(temp))
    time.sleep(1)


def main():
    read_temp()


while True:
    try:
        main()
    except KeyboardInterrupt:
        print('\nProgramme terminated')
        break
