import random
import colorsys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5.uic import loadUi
import sys
import math
import time
import matplotlib.pyplot as plt
import librosa.display
import numpy as np
import pygame
from AudioAnalyzer import *

class AduioVisualizer:
    def __init__(self):
        self.play = True

    def rnd_color(self):
        h, s, l = random.random(), 0.5 + random.random() / 2.0, 0.4 + random.random() / 5.0
        return [int(256 * i) for i in colorsys.hls_to_rgb(h, l, s)]

    def click(self, path):
        
            #print(path)
            #new_path = path.replace("C:/Users/domin/OneDrive - Oregon State University/CS things/361/Assignment 5/","")
            #print(new_path)
            #self.play = True
            filename = path

            #filename = "sob.wav"
            notes = []
            init_array = []
            init_bars = []
            counter = 0
            angle = 0
            bass = 0
            trigger = -40
            trigger_started = 0
            low_decibel = -90
            high_decibel = 90
            c_color1 = random.randint(0, 124)
            c_color2 = random.randint(0, 124)
            c_color3 = random.randint(0, 124)
            print(c_color1)
            poly_color1 = random.randint(125, 255)
            poly_color2 = random.randint(125, 255)
            poly_color3 = random.randint(125, 255)
            print(poly_color1)
            c_color = (c_color1, c_color2, c_color3)
            poly_color = [poly_color1, poly_color2, poly_color3]
            b_color = poly_color.copy()
            polygon_color_vel = [0, 0, 0]
            polygon = []
            poly_color = poly_color.copy()
            pygame.init()
            ObjectInfo = pygame.display.Info()
            screen_width = 700
            screen_height = 700
            Xcord = int(screen_width / 2)
            Ycord = int(screen_height/2)
            low_radius = 50
            high_radius = 100
            radius = low_radius
            radius_val = 0
            #blah
            data = MusicData()
            data.load(filename)
            # Set up the drawing window
            screen = pygame.display.set_mode([screen_width, screen_height])
            time = pygame.time.get_ticks()
            Frame = time
            bass = {"start": 40, "stop": 100, "count": 12}
            heavy = {"start": 110, "stop": 260, "count": 40}
            low = {"start": 261, "stop": 2500, "count": 50}
            high = {"start": 2601, "stop": 6500, "count": 20}
            music_groups = [bass, heavy, low, high]
            length = 0

            for j in music_groups:
                s = j["stop"] - j["start"]
                count = j["count"]
                moduloe = s%count
                step = int(s/count)
                jesus = j["start"]
                for i in range(count):
                    step_array = None
                    if moduloe > 0:
                        moduloe = moduloe - 1
                        step_array = np.arange(start=jesus, stop=jesus + step + 2)
                        jesus += step + 3
                    else:
                        step_array = np.arange(start=jesus, stop=jesus + step + 1)
                        jesus += step + 2
                    init_array.append(step_array)
                    length = length + 1
                init_bars.append(init_array)
            theta = 360/length

            for k in init_bars:
                circle_array = []
                for l in k:
                    circle_array.append(AverageNotes(Xcord+radius*math.cos(math.radians(angle - 90)), Ycord+radius*math.sin(math.radians(angle - 90)), l, (255, 0, 255), angle=angle, width=8, max_height=370))
                    angle = angle + theta

                notes.append(circle_array)

            pygame.mixer.music.load(filename)
            pygame.mixer.music.play(0)
            pygame.mixer.music.set_volume(0.0)

            running = True

            while running:
                #self.play = self.set_state()
                if(self.play == False):
                    pygame.mixer.music.pause()
                while self.play:
                    pygame.mixer.music.unpause()
                    bass = 0
                    polygon = []
                    time = pygame.time.get_ticks()
                    change = (time - Frame) / 1000.0
                    Frame = time
                    counter = counter + change
                    screen.fill(c_color)

                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            running = False
                    
                    for i in notes:
                        for j in i:
                            j.update_all(change, pygame.mixer.music.get_pos() / 1000.0, data)
                    
                    for i in notes[0]:
                        bass += i.avg
                    bass /= len(notes[0])

                    if bass > trigger:
                        if trigger_started == 0:
                            trigger_started = pygame.time.get_ticks()
                        if (pygame.time.get_ticks() - trigger_started)/1000.0 > 2:
                            b_color = self.rnd_color()
                            trigger_started = 0
                        if b_color is None:
                            b_color = self.rnd_color()
                        newr = low_radius + int(bass * ((high_radius - low_radius) / (high_decibel - low_decibel)) + (high_radius - low_radius))
                        radius_val = (newr - radius) / 0.15
                        polygon_color_vel = [(b_color[x] - poly_color[x])/0.15 for x in range(len(poly_color))]

                    if radius > low_radius:
                        trigger_started = 0
                        b_color = None
                        radius_val = (low_radius - radius) / 0.15
                        polygon_color_vel = [(poly_color[x] - poly_color[x])/0.15 for x in range(len(poly_color))]

                    else:
                        trigger_started = 0
                        poly_color = poly_color.copy()
                        b_color = None
                        polygon_color_vel = [0, 0, 0]
                        radius_val = 0
                        radius = low_radius
                    radius += radius_val * change

                    for i in range(len(polygon_color_vel)):
                        value = polygon_color_vel[i]*change + poly_color[i]
                        poly_color[i] = value
                    for x in notes:
                        for j in x:
                            j.x, j.y = Xcord+radius*math.cos(math.radians(j.angle - 90)), Ycord+radius*math.sin(math.radians(j.angle - 90))
                            j.update_rect()
                            polygon.append(j.rect.points[3])
                            polygon.append(j.rect.points[2])
                    pygame.draw.polygon(screen, poly_color, polygon)
                    pygame.draw.circle(screen, c_color, (Xcord, Ycord), int(radius))
                    pygame.display.flip()
                bruh = 69
                pygame.event.pump()
            pygame.quit()


    def set_True(self):
        self.play = True
        print("done")

    def set_False(self):
        self.play = False
        print("complete")

def turn(cord, angle):
    cos_angle, sin_angle = math.cos(angle), math.sin(angle)
    return (
        cord[0] * cos_angle - cord[1] * sin_angle,
        cord[0] * sin_angle + cord[1] * cos_angle
    )


def translate(cord, offset):
    return cord[0] + offset[0], cord[1] + offset[1]


def tight(min, max, val):
    if val < min:
        return min
    if val > max:
        return max

    return val



#Libarary Based off of tutorial mentioned above
class MusicData:
    def __init__(self):
        self.frequencies = 0 
        self.time = 0  
        self.spectrogram = None  

    def load(self, filename):
        time_series, sample_rate = librosa.load(filename)
        stft = np.abs(librosa.stft(time_series, hop_length=512, n_fft=2048*4))
        self.spectrogram = librosa.amplitude_to_db(stft, ref=np.max) 
        frequencies = librosa.core.fft_frequencies(n_fft=2048*4)  
        times = librosa.core.frames_to_time(np.arange(self.spectrogram.shape[1]), sr=sample_rate, hop_length=512, n_fft=2048*4)
        self.time = len(times)/times[len(times) - 1]
        self.frequencies = len(frequencies)/frequencies[len(frequencies)-1]

    def get_decibel(self, target_time, freq):
        return self.spectrogram[int(freq*self.frequencies)][int(target_time*self.time)]



class Notes:
    def __init__(self, x, y, freq, color, width=50, min_height=10, max_height=100, min_decibel=-80, max_decibel=0):
        self.x, self.y, self.freq = x, y, freq
        self.color = color
        self.width, self.min_height, self.max_height = width, min_height, max_height
        self.height = min_height
        self.min_decibel, self.max_decibel = min_decibel, max_decibel
        self.__decibel_height_ratio = (self.max_height - self.min_height)/(self.max_decibel - self.min_decibel)

    def update(self, dt, decibel):
        desired_height = decibel * self.__decibel_height_ratio + self.max_height
        speed = (desired_height - self.height)/0.1
        self.height += speed * dt
        self.height = tight(self.min_height, self.max_height, self.height)


class MoreNotes(Notes):
    def __init__(self, x, y, rng, color, width=50, min_height=10, max_height=100, min_decibel=-80, max_decibel=0):
        super().__init__(x, y, 0, color, width, min_height, max_height, min_decibel, max_decibel)
        self.rng = rng
        self.avg = 0

    def update_all(self, dt, time, analyzer):
        self.avg = 0
        for i in self.rng:
            self.avg += analyzer.get_decibel(time, i)

        self.avg /= len(self.rng)
        self.update(dt, self.avg)

class AverageNotes(MoreNotes):

    def __init__(self, x, y, rng, color, angle=0, width=50, min_height=10, max_height=100, min_decibel=-80, max_decibel=0):
        super().__init__(x, y, 0, color, width, min_height, max_height, min_decibel, max_decibel)
        self.rng = rng
        self.rect = None
        self.angle = angle

    def update_rect(self):
        self.rect = Rectangle(self.x, self.y, self.width, self.height)
        self.rect.rotate(self.angle)


class Rectangle:
    def __init__(self,x ,y, w, h):
        self.x, self.y, self.w, self.h = x,y, w, h
        self.points = []
        self.origin = [self.w/2,0]
        self.offset = [self.origin[0] + x, self.origin[1] + y]
        self.rotate(0)
    def rotate(self, angle):
        template = [
            (-self.origin[0], self.origin[1]),
            (-self.origin[0] + self.w, self.origin[1]),
            (-self.origin[0] + self.w, self.origin[1] - self.h),
            (-self.origin[0], self.origin[1] - self.h)
        ]
        self.points = [translate(turn(xy, math.radians(angle)), self.offset) for xy in template]
    def draw(self,screen):
        pygame.draw.polygon(screen, (255,255, 0), self.points)



def window():
    #sys.exit(app.exec())
    #filename = "lucid.wav"
    #click(filename, play)
    print("Bruhhhh")

window()