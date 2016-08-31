#!/usr/bin/env python3

import kxg

from .messages import SetupWorld

class Referee(kxg.Referee):

    def on_start_game(self, num_players):
        self >> SetupWorld()

