from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import threading

from get_data import data_points, get_data_column

continuePlotting = False


def change_state():
    global continuePlotting
    if continuePlotting:
        continuePlotting = False
    else:
        continuePlotting = True


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
