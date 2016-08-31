#!/usr/bin/env python3

import kxg
import pyglet

class Gui:

    def __init__(self):
        self.window = pyglet.window.Window()
        self.window.set_visible(True)
        self.batch = pyglet.graphics.Batch()
        self.texts = []

        self.background_group = pyglet.graphics.OrderedGroup(0)
        self.buttons_group = pyglet.graphics.OrderedGroup(1)
        self.text_group = pyglet.graphics.OrderedGroup(2)

        self.test_counter = 0
        self.tester = self.create_text('{:d}'.format(self.test_counter), 0, 0)

    def on_refresh_gui(self):
        self.window.clear()
        self.batch.draw()
        self.test_counter += 1
        self.tester.text='{:d}'.format(self.test_counter)

    def create_text(self, initial_message, x_coor, y_coor):
        self.texts.append(pyglet.text.Label(
            initial_message,
            font_name='Arial',
            font_size=40,
            x = x_coor, y = y_coor,
            anchor_x='left', anchor_y='bottom',
            batch= self.batch, group= self.text_group
            ))
        return self.texts[-1]


class GuiActor(kxg.Actor):

    def __init__(self):
        super().__init__()

    def on_setup_gui(self, gui):
        self.gui = gui
        self.gui.window.set_handlers(self)

    def on_draw(self):
        self.gui.on_refresh_gui()


