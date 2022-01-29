from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import threading
import serial
import openpyxl
import datetime

port = '/dev/ttyACM0'  # define it to the port where the arduino is connected
ser = serial.Serial(port=port, baudrate=9600, timeout=1)  # Serial port configuration
Workbook = openpyxl.Workbook()
WorkSheet = Workbook.active

# receive the data from the serial port and save it in the worksheet
num_line = 1

continuePlotting = False
sheet_file = f'dados_ard_at_{datetime.datetime.now()}.xlsx'


def change_state():
    global continuePlotting
    if continuePlotting:
        continuePlotting = False
    else:
        continuePlotting = True


def read_serial(file, label):
    global num_line
    num_column = 3

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


def app():
    root = Tk()
    root.config(background='white')
    root.geometry('1000x700')
    label_readings = Label(root, text=f'Empuxo {0} ---- Tensão {0} ---- Corrente {0}', height=2)
    label_readings.pack()

    fig = Figure()

    ax = fig.add_subplot(131)
    ax.set_xlabel('Tempo (s)')
    ax.set_ylabel('Empuxo (g)')

    bx = fig.add_subplot(132)
    bx.set_xlabel('Tempo (s)')
    bx.set_ylabel('Tensão (V)')

    cx = fig.add_subplot(133)
    cx.set_xlabel('Tempo (s)')
    cx.set_ylabel('Corrente (A)')

    ax.grid()
    bx.grid()
    cx.grid()

    graph = FigureCanvasTkAgg(fig, master=root)
    graph.get_tk_widget().pack(expand=True, ipady=30, fill='both')

    def plotter():
        while continuePlotting:
            data = data_points(label_readings)
            ax.cla()
            ax.grid()
            ax.set_xlabel('Tempo (s)')
            ax.set_ylabel('Empuxo (g)')
            dpts = get_data_column(1, data)
            ax.plot(range(10), dpts, marker='o', color='orange')


            bx.cla()
            bx.grid()
            bx.set_xlabel('Tempo (s)')
            bx.set_ylabel('Tensão (V)')
            dpts2 = get_data_column(2, data)
            bx.plot(range(10), dpts2, marker='o', color='orange')


            cx.cla()
            cx.grid()
            cx.set_xlabel('Tempo (s)')
            cx.set_ylabel('Corrente (A)')
            dpts3 = get_data_column(3, data)
            cx.plot(range(10), dpts3, marker='o', color='orange')


            graph.draw()

    def gui_handler():
        change_state()
        if continuePlotting:
            b.config(text='Stop', bg='red')
        else:
            b.config(text='Start', bg='green')
        threading.Thread(target=plotter).start()

    b = Button(root, text='Start', command=gui_handler, bg='green', fg='white')
    b.pack()


    root.mainloop()


if __name__ == '__main__':
    app()
