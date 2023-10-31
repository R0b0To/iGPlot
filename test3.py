from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np


class Ball:

    def __init__(self, initpos, initvel, radius, M):
        self.pos = initpos
        self.vel = initvel
        self.radius = radius
        self.M = M

    def step(self, dt):

        self.pos += self.vel * dt
        self.vel[2] += -9.81 * dt * self.M

initpos = np.array([5., 5., 10.])
initvel = np.array([0., 0., 0.])
radius = .25
M, dt = 1, .1


test_ball = Ball(initpos, initvel, radius, M)

fig, ax = plt.subplots(subplot_kw=dict(projection='3d'))

pts = ax.plot([], [], [], 'bo', c='blue')


def init():
    for pt in pts:
        pt.set_data([], [])
        pt.set_3d_properties([])
    ax.set_xlim3d(0, 1.5 * initpos[0])
    ax.set_ylim3d(0, 1.5 * initpos[1])
    ax.set_zlim3d(0, 1.5 * initpos[2])
    return pts


def animate(i):
    test_ball.step(dt)
    for pt in pts:
        pt.set_data(test_ball.pos[0], test_ball.pos[1])
        pt.set_3d_properties(test_ball.pos[2])
        pt.set_markersize(10)

    return pts

anim = animation.FuncAnimation(fig, animate, init_func=init, frames=50)
mywriter = animation.FFMpegWriter(fps=10)
anim.save('mymovie.mp4', writer=mywriter)