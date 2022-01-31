import matplotlib.pyplot as plt
import numpy as np

# use ggplot style for more sophisticated visuals
plt.style.use('ggplot')


def live_plotter(x_vec, y1_data, y2_data, y3_data, line1, line2, line3, identifier='', pause_time=0.1):
    if line1 == [] and line2 == [] and line3 == []:
        # this is the call to matplotlib that allows dynamic plotting
        plt.ion()
        fig = plt.figure(figsize=(13, 6))
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
        # create a variable for the line so we can later update it
        line1, = ax.plot(x_vec, y1_data, '-o', alpha=0.8)
        line2, = bx.plot(x_vec, y1_data, '-o', alpha=0.8)
        line3, = cx.plot(x_vec, y1_data, '-o', alpha=0.8)

        plt.show()

    # after the figure, axis, and line are created, we only need to update the y-data
    line1.set_ydata(y1_data)
    line2.set_ydata(y2_data)
    line3.set_ydata(y3_data)
    # adjust limits if new data goes beyond bounds
    if np.min(y1_data) <= line1.axes.get_ylim()[0] or np.max(y1_data) >= line1.axes.get_ylim()[1]:
        plt.ylim([np.min(y1_data) - np.std(y1_data), np.max(y1_data) + np.std(y1_data)])
    if np.min(y2_data) <= line2.axes.get_ylim()[0] or np.max(y2_data) >= line2.axes.get_ylim()[1]:
        plt.ylim([np.min(y2_data) - np.std(y2_data), np.max(y2_data) + np.std(y2_data)])
    if np.min(y3_data) <= line3.axes.get_ylim()[0] or np.max(y3_data) >= line3.axes.get_ylim()[1]:
        plt.ylim([np.min(y3_data) - np.std(y3_data), np.max(y3_data) + np.std(y3_data)])
    # this pauses the data so the figure/axis can catch up - the amount of pause can be altered above
    plt.pause(pause_time)

    # return line so we can update it again in the next iteration
    return line1, line2, line3


def live_plotter_xy(x_vec, y1_data, y2_data, y3_data, line1, line2, line3, identifier='', pause_time=0.01):
    if line1 == [] and line2 == [] and line3 == []:
        plt.ion()
        fig = plt.figure(figsize=(13, 6))
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
        # create a variable for the line so we can later update it
        line1, = ax.plot(x_vec, y1_data, '-o', alpha=0.8)
        line2, = bx.plot(x_vec, y1_data, '-o', alpha=0.8)
        line3, = cx.plot(x_vec, y1_data, '-o', alpha=0.8)

    plt.show()

    line1.set_data(x_vec, y1_data)
    line2.set_data(x_vec, y2_data)
    line3.set_data(x_vec, y3_data)
    plt.xlim(np.min(x_vec), np.max(x_vec))
    if np.min(y1_data) <= line1.axes.get_ylim()[0] or np.max(y1_data) >= line1.axes.get_ylim()[1]:
        plt.ylim([np.min(y1_data) - np.std(y1_data), np.max(y1_data) + np.std(y1_data)])
    if np.min(y2_data) <= line2.axes.get_ylim()[0] or np.max(y2_data) >= line2.axes.get_ylim()[1]:
        plt.ylim([np.min(y2_data) - np.std(y2_data), np.max(y2_data) + np.std(y2_data)])
    if np.min(y3_data) <= line3.axes.get_ylim()[0] or np.max(y3_data) >= line3.axes.get_ylim()[1]:
        plt.ylim([np.min(y3_data) - np.std(y3_data), np.max(y3_data) + np.std(y3_data)])
    plt.pause(pause_time)

    return line1, line2, line3


size = 100
x_vec = np.linspace(0, 1, size + 1)[0:-1]
y1_vec = np.random.randn(len(x_vec))
y2_vec = np.random.randn(len(x_vec))
y3_vec = np.random.randn(len(x_vec))
line1 = []
line2 = []
line3 = []
while True:
    rand_val = np.random.randn(1)
    y1_vec[-1] = rand_val
    y2_vec[-1] = rand_val
    y3_vec[-1] = rand_val
    line1, line2, line3 = live_plotter(x_vec, y1_vec, y2_vec, y3_vec, line1, line2, line3)
    y1_vec = np.append(y1_vec[1:], 0.0)
    y2_vec = np.append(y2_vec[1:], 0.0)
    y3_vec = np.append(y3_vec[1:], 0.0)
