# -*- coding: utf-8 -*-
"""
@author: enom
"""
import tkinter as tk
from math import sin, cos, radians


class GeometricPattern():
    D_THETA_MAX = 20
    DEG = 360
    D_PHI = 1
    def __init__(self, center_x=0, center_y=0):
        self.center_x = center_x
        self.center_y = center_y
        self.r = int(0.8*min(self.center_x, self.center_y) / 3) #80
        self.a = int(0.8*2*min(self.center_x, self.center_y) / 3) #160
        self.phi = 0
        self.mag = 104
        self.d_theta = 1
        self.get_points()
        
    def dec_r(self, event):
        self.r -= 1
        if self.r < 1:
            self.r = 1
    
    def inc_r(self, event):
        if self.r + self.a < min(self.center_x, self.center_y):
            self.r += 1
        
    def dec_a(self, event):
        self.a -= 1
        if self.a < 1:
            self.a = 1
    
    def inc_a(self, event):
        if self.r + self.a < min(self.center_x, self.center_y):
            self.a += 1
    
    def dec_d_theta(self, event):
        self.d_theta -= 1
        if self.d_theta < 1:
            self.d_theta = 1
    
    def inc_d_theta(self, event):
        self.d_theta += 1
        if self.d_theta > GeometricPattern.D_THETA_MAX:
            self.d_theta = GeometricPattern.D_THETA_MAX
    
    def dec_mag(self, event):
        self.mag -= 1
        if self.mag < 0:
            self.mag %= GeometricPattern.DEG
    
    def inc_mag(self, event):
        self.mag += 1
        if self.mag >= GeometricPattern.DEG:
            self.mag %= GeometricPattern.DEG

    def inc_phi(self):
        self.phi += 1
        self.phi %= GeometricPattern.DEG
        
    def get_points(self):
        #self.points = [(x1, y1), (x2, y2), ..., (xn, yn), (x1, y1)]
        self.points = [
                (self.center_x + self.r*cos(radians(theta))
                + self.a*cos(radians(self.phi + theta*self.mag)),
               self.center_y + self.r*sin(radians(theta))
                + self.a*sin(radians(self.phi + theta*self.mag)))
                for theta in range(0, GeometricPattern.DEG, self.d_theta)]
        self.points.append((self.points[0], self.points[1]))


class Simulator():
    MS = 16 #16 ms/frame (approx. 60 fps)
    def __init__(self, width, height):
        #ウインドウサイズ
        self.width = width
        self.height = height

        #ウインドウとウィジットの作成・設定
        self.window = tk.Tk()
        self.window.title(string='Sample Trig Function on Tkinter')
        self.window.resizable(width=False, height=False)
        self.canvas = tk.Canvas(
                self.window, width=self.width, height=self.height)
        
        #canvas上での関数の原点座標
        self.center_x = width / 2
        self.center_y = height / 2
        
        #各文字列を表示する座標
        self.quit_x = 20
        self.quit_y = 30
        self.r_x = width - 20
        self.r_y = height - 120
        self.a_x = width - 20
        self.a_y = height - 90
        self.mag_x = width - 20
        self.mag_y = height - 60
        self.d_theta_x = width - 20
        self.d_theta_y = height - 30
        
        self.gp = GeometricPattern(self.center_x, self.center_y)
        
        self.canvas.create_rectangle(
                0, 0, self.width, self.height, fill='black')
        self.draw()
        self.canvas.pack()
        
        #キーバインド
        self.window.bind('<KeyPress-q>', self.quit)
        self.window.bind('<KeyPress-z>', self.gp.dec_r)
        self.window.bind('<KeyPress-a>', self.gp.inc_r)
        self.window.bind('<KeyPress-x>', self.gp.dec_a)
        self.window.bind('<KeyPress-s>', self.gp.inc_a)
        self.window.bind('<KeyPress-c>', self.gp.dec_mag)
        self.window.bind('<KeyPress-d>', self.gp.inc_mag)
        self.window.bind('<KeyPress-v>', self.gp.dec_d_theta)
        self.window.bind('<KeyPress-f>', self.gp.inc_d_theta)

    def quit(self, event):
        self.window.destroy()
        
    def draw(self):
        #幾何学模様の表示
        self.canvas.create_line(
                self.gp.points, fill='white', tag='sample')

        #各文字列の表示
        self.canvas.create_text(
                self.quit_x, self.quit_y,
                text='Quit: q',
                tag='sample', font=('Arial', 12), fill='white', anchor=tk.W)
        self.canvas.create_text(
                self.r_x, self.r_y,
                text='Z < '+str(self.gp.r).zfill(3)+'> A',
                tag='sample', font=('Arial', 12), fill='white', anchor=tk.E)
        self.canvas.create_text(
                self.a_x, self.a_y,
                text='X < '+str(self.gp.a).zfill(3)+'> S',
                tag='sample', font=('Arial', 12), fill='white', anchor=tk.E)
        self.canvas.create_text(
                self.mag_x, self.mag_y,
                text='C < '+str(self.gp.mag).zfill(3)+'> D',
                tag='sample', font=('Arial', 12), fill='white', anchor=tk.E)
        self.canvas.create_text(
                self.d_theta_x, self.d_theta_y,
                text='V < '+str(self.gp.d_theta).zfill(3)+'> F',
                tag='sample', font=('Arial', 12), fill='white', anchor=tk.E)

    def delete(self):
        #tagが'sample'のオブジェクトをすべて削除する
        self.canvas.delete('sample')

    def loop(self):
        #描画のメインループ
        self.gp.inc_phi()
        self.gp.get_points()
        self.delete()
        self.draw()
        self.window.after(Simulator.MS, self.loop)


def main():
    WIDTH = 800
    HEIGHT = 600
    simulator = Simulator(WIDTH, HEIGHT)
    simulator.loop()
    simulator.window.mainloop()


if __name__ == '__main__':
    main()