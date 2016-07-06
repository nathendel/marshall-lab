import numpy as np
import matplotlib.pyplot as plt
import random
import time
from math import floor


class Cell:
    cells = []

    def __init__(self, t=0, L=0, N=200, trans_speed=1.8 / 10, k_on=.2, k_off=.2,
                 avalanche_on=True, thresh=5, num_release=5,
                 L_mod=True, build_size=.25 / 200, decay_size=.0037 / 10,
                 rms_disp=3.5777 / 10, ava_power=2.85):  # L is length, N is number of particles

        #         cdef float L

        self.t = t
        self.L = L
        self.trans_speed = trans_speed
        self.k_on = k_on
        self.k_off = k_off
        self.N = N
        self.motors = [Motor(self) for i in range(N)]

        self.active50 = self.N
        self.avalanche_on = avalanche_on
        self.thresh = thresh
        self.num_release = num_release
        self.recruited = 0
        self.L_mod = L_mod
        self.build_size = build_size
        self.decay_size = decay_size
        self.rms_disp = rms_disp
        self.ava_power = ava_power
        self.ava = []

        self.L_trace = np.zeros(t)
        # self.track_active = np.zeros(t)

        if t:
            self.sim(t)

    def count_active(self):
        return sum([p.isactive for p in self.motors])

    def sim(self, t):

        for i in range(t):

            #         print(self.count_active())
            if self.avalanche_on:
                self.avalanche()

            if self.L_mod:
                if self.L >= self.decay_size:
                    self.L -= self.decay_size

                # new may 27
                elif self.L < self.decay_size:
                    self.L = 0

                self.L_trace[i] = self.L

            for p in self.motors:

                if p.isactive:
                    if p.isbound:
                        p.active_trans()
                    else:
                        p.diffuse()
                        #             else:
                        #                 self.inactive += 1
                p.track[i] = p.pos

            # self.track_active[i] = self.count_active()

    def avalanche(self):
        # distr = floor(1/np.random.power(self.ava_power))

        num_inactive = self.N - self.count_active()
        inactive = [p for p in self.motors if not p.isactive]
        if num_inactive > self.thresh:
            #             release = min(floor(1/np.random.power(3)),num_inactive)
            distr = int(5 * np.random.weibull(1) + 1)  # parameters are totally arbitrary

            release = min(distr, num_inactive)
            self.ava.append(release)

            for i in range(release):  # commented out to try power law
                #             for i in range(1/np.random.power(3))
                inactive[i].isactive = True
                inactive[i].isbound = True

                if self.L_mod:
                    inactive[i].built = False
            self.recruited += self.num_release

    def L_plot(self):
        t = round(len(self.L_trace) / 60)

        plt.plot(self.L_trace);

        #         plt.plot(self.L_trace[0::60]);

        plt.xlabel('time');
        plt.ylabel('flagellar length (um)');
        plt.title('Flagellar growth');
        plt.show()

    def plot_growth_rate(self):
        L_min = self.L_trace[0::120]
        #         growthrate = [j-i for i, j in zip(pile5.L_trace[:-1], pile5.L_trace[1:])]

        growthrate = [j - i for i, j in zip(L_min[:-1], L_min[1:])]
        #         gr_min=growthrate[0::120]
        #         plt.plot(L_min,gr_min);
        plt.plot(L_min[0:-1], growthrate)
        plt.xlabel('Flagellar Length (um)');
        plt.ylabel('Growth rate (um/s)');

    def growth(self):  # Engel and Ludington et al 2009 Fig 1b attempt
        plt.figure(1)
        self.L_plot()
        plt.figure(2)
        self.plot_growth_rate()

    def __repr__(self):
        string = 'Cell of length %s populated by %d motors' % (self.L, self.N)
        return string


class Motor:
    instances = []

    def __init__(self, cell, isactive=True, isbound=True):
        self.pos = 0
        self.isactive = isactive
        self.isbound = isbound
        Motor.instances.append(self)
        self.cell = cell
        self.track = np.zeros(self.cell.t)
        self.built = False

    def diffuse(self):

        if not self.cell.L_mod:
            #                 if self.isactive:
            if self.pos == self.cell.L:
                self.binding()
                #                 print(self.isbound)

                #                 if not self.binding(): #check if it re-binds, don't move if it does
                # #                 print(self.isbound)
                if self.isbound == False:
                    self.pos -= self.cell.rms_disp


            elif self.pos == 0:
                self.isactive = False  # keep this for later, using avalanche model

            #                 self.isbound = True

            else:
                r=np.random.rand()
                if r<.5:
                    self.pos -= self.cell.rms_disp
                else:
                    self.pos += self.cell.rms_disp
                # self.pos += (random.choice([-1, 1]) * self.cell.rms_disp)
            #             self.track.append(self.pos)


        elif self.cell.L_mod:
            if self.pos > self.cell.L:  # for length decay
                self.pos = self.cell.L

            if self.pos == self.cell.L:
                #                     self.binding()
                #                     print(self.isbound)

                if not self.isbound:
                    self.pos -= self.cell.rms_disp


            else:

                # r=np.random.rand


                r=np.random.rand()
                if r<.5:
                    self.pos -= self.cell.rms_disp
                else:
                    self.pos += self.cell.rms_disp

                # self.pos += (random.choice([-1, 1]) * self.cell.rms_disp)

                # try this line to force positions in between 0 and L:
                # self.pos = np.median([0,self.cell.L,self.pos])

                if self.pos < 0:
                    self.pos = 0
                elif self.pos > self.cell.L:
                    self.pos = self.cell.L

                # self.pos = min(max(0, self.pos), self.cell.L)

            #             self.track.append(self.pos)

            if self.pos <= 0:
                self.isactive = False  # keep this for later, using avalanche model


            #                     elif self.isbound == False:
            #                         self.pos += random.choice([-1,1])
            #                         elif not self.isbound:
            #                             self.pos -= 1

            #                  if self.isbound == False:
            # #                     self.pos -= 1
            #                             self.pos += random.choice([-1,1])

            #                 print(self.isbound)


            #                 if not self.binding(): #check if it re-binds, don't move if it does
            # #                 print(self.isbound)


            #             if self.pos == 0:
            #                 self.isactive = False #keep this for later, using avalanche model

            #                 self.isbound = True

    def active_trans(self):
        if self.pos < self.cell.L:
            self.pos += self.cell.trans_speed
            self.pos = min(self.pos, self.cell.L)
        #         if self.pos == self.cell.L:
        if self.pos >= self.cell.L:
            if not self.built:
                self.cell.L += self.cell.build_size
                self.built = True
            self.isbound = False
        #         self.track.append(self.pos)

    def binding(self):
        roll = np.random.rand()
        if self.isbound == False:
            if roll < self.cell.k_on:  # probability of binding to the IFT particle, stalling diffusion
                self.isbound = True
            #                 print('bound!')
        else:  # if self.isbound == True
            if roll < self.cell.k_off:
                self.isbound = False
            #                 print('unbound!')

            #         return self.isbound #return the updated bound state

    def trace(self):
        plt.plot(self.track);
        plt.xlabel('time');
        plt.ylabel('position');

    def __repr__(self):
        string = 'Motor at position %s' % self.pos
        return string


#

if __name__ == '__main__':
    a=Cell(t=30000)
# 	# print(a.L)

## run profiler: python -m cProfile -s cumtime cell2.py


'''
notes on default params:
N=200 based on 10 transport complexes from Marshall and Rosenbaum 2001 Appendix multiplied by each injection event
sends 1-30 IFT particles from Ludington 2013 p.3926

'''
