import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import matplotlib.dates as mdates


style.use('fivethirtyeight')
fig = plt.figure()
ax = fig.add_subplot(1,1,1)

def animate(i):
    graph = open('prices.txt','r')
    xas = []
    yas = []
    for line in graph:
        if len(line) > 1:
            x,y = line.split(',')
            xas.append(x)
            yas.append(y)
            dt = mdates.datestr2num(xas)
    ax.clear()
    ax.plot(dt,yas,lw=1)
    ax.xaxis_date()
    #ax.set_ylim([0.026,0.028])

ani = animation.FuncAnimation(fig,animate,interval=10000)
plt.show()

