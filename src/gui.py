#!/usr/bin/env python3

import kxg
import pyglet

from .world import Player
from .messages import SetupPlayer, MakeInvestment

class Gui:

    def __init__(self):
        self.window = pyglet.window.Window()
        self.window.set_visible(True)
        self.batch = pyglet.graphics.Batch()
        self.texts = []

        self.background_group = pyglet.graphics.OrderedGroup(0)
        self.buttons_group = pyglet.graphics.OrderedGroup(1)
        self.text_group = pyglet.graphics.OrderedGroup(2)

    def on_refresh_gui(self):
        self.window.clear()
        self.batch.draw()

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
        self.player = Player()

    def on_setup_gui(self, gui):
        self.gui = gui
        self.gui.window.set_handlers(self)

        self.supply_label = self.gui.create_text('', 20, 280)
        self.demand_label = self.gui.create_text('', 20, 220)
        self.price_label = self.gui.create_text('',  20, 160)
        self.wealth_label = self.gui.create_text('', 20, 80)
        self.income_label = self.gui.create_text('', 20, 20)

    def on_start_game(self, num_players):
        self >> SetupPlayer(self.player)
        self >> MakeInvestment(self.player.cities[0],
                self.world.investment_tree['small grain farm'])

    def on_draw(self):
        grains = self.world.industry_tree['grains']
        self.wealth_label.text = '${:.0f}'.format(self.player.wealth)
        self.income_label.text = '${:.0f}/sec'.format(self.player.wealth_per_sec)
        self.supply_label.text = 'Supply (grains): {:.0f}/sec'.format(self.player.cities[0].calculate_supply(grains))
        self.demand_label.text = 'Demand (grains): {:.0f}/sec'.format(grains.calculate_demand())
        self.price_label.text = 'Price (grains): ${:.0f}'.format(grains.calculate_price())

        self.gui.on_refresh_gui()



