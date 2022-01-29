import os

import serial
from datetime import datetime
import openpyxl

Workbook = openpyxl.Workbook()
WorkSheet = Workbook.active
num_line = 1
sheet_file = f'dados_ard_at_{datetime.now()}.xlsx'


def find_arduino():
    port = os.popen('ls /dev/ttyACM*').readlines()[0].replace('\n', '')
    ser = serial.Serial(port=port, baudrate=9600, timeout=1)  # Serial port configuration
    return ser


def read_serial(file, label):
    global num_line
    num_column = 3
    ser = find_arduino()

    x = ser.readline().decode('ascii')
    serial_reading = x.split(',')
    while serial_reading[0] != '<' or serial_reading[-1] != '>\r\n':
        x = ser.readline().decode('ascii')
        serial_reading = x.split(',')
    try:
        if serial_reading[0] == '<' and serial_reading[-1] == '>\r\n':
            serial_reading.remove('<')
            serial_reading.remove('>\r\n')

            for i in range(1, num_column+1):
                WorkSheet.cell(row=num_line, column=i, value=serial_reading[i-1])
                file.write(f'{serial_reading[i-1]},')

                if i == num_column:
                    num_line += 1
            Workbook.save(sheet_file)
            file.write('\n')
        else:
            read_serial(file)
    except:
        read_serial(file)

    print(serial_reading)
    label.config(text=f'Empuxo: {serial_reading[0]} g ---- Tensão: {serial_reading[1]} V ---- Corrente: {serial_reading[2]} A')
    return serial_reading


def data_points(label):
    file = open('data.txt', 'w')
    for i in range(10):
        read_serial(file, label)
    file.close()

    f = open('data.txt', 'r')
    data = f.readlines()
    f.close()
    new_data = []
    for i in range(len(data)):
        new_list = data[i].split(',')
        new_list.remove('\n')
        new_data.append(new_list)

    return new_data


def get_data_column(column_number: int, data):
    column_data = []
    for i in data:
        try:
            if len(i) >= column_number:
                column_data.append(i[column_number-1])
            else:
                print('Invalid Column number!')
        except:
            get_data_column(column_number, data)
            break
    return column_data
