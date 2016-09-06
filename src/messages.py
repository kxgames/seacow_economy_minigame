#!/usr/bin/env python3

import kxg

from .world import *

class SetupWorld(kxg.Message):

    def __init__(self):
        self.industry_tree = None
        self.investment_tree = None

        self.setup_industry_tree()
        self.setup_investment_tree()

    def setup_industry_tree(self):
        self.industry_tree = tree = IndustryTree()

        tree.add_industry('grains', 20, 10, 0.1)
        tree.add_industry('fruits', 20, 10, 0.1)
        tree.add_industry('livestock', 20, 10, 0.1)
        tree.add_industry('stone', 20, 10, 0.1)
        tree.add_industry('lumber', 20, 10, 0.1)
        tree.add_industry('paper', 20, 10, 0.1)
        tree.add_industry('iron', 20, 10, 0.1)

        tree.add_industry_edge('lumber', 'paper')

        tree.add_industry_group(['grains', 'fruits', 'livestock'], 10)
        tree.add_industry_group(['lumber', 'stone'], 10)

    def setup_investment_tree(self):
        self.investment_tree = tree = InvestmentTree(self.industry_tree)

        tree.add_investment('grains', 'small grain farm', 100, add=1)
        tree.add_investment('grains', 'large grain farm', 500, add=10)
        tree.add_investment('grains', 'crop rotation', 100, mul=0.1)
        tree.add_investment('fruits', 'small fruit farm', 100, add=1)
        tree.add_investment('fruits', 'large fruit farm', 500, add=10)
        tree.add_investment('fruits', 'new technology', 100, add=0.1)
        tree.add_investment('livestock', 'small herd', 100, add=1)
        tree.add_investment('livestock', 'large herd', 500, add=10)
        tree.add_investment('livestock', 'new technology', 100, add=0.1)
        tree.add_investment('stone', 'small quarry', 100, add=1)
        tree.add_investment('stone', 'large quarry', 500, add=10)
        tree.add_investment('stone', 'new technology', 100, add=0.1)
        tree.add_investment('lumber', 'small lumber mill', 100, add=1)
        tree.add_investment('lumber', 'large lumber mill', 500, add=10)
        tree.add_investment('lumber', 'new technology', 100, add=0.1)
        tree.add_investment('paper', 'small press', 100, add=1)
        tree.add_investment('paper', 'large press', 500, add=10)
        tree.add_investment('paper', 'new technology', 100, add=0.1)
        tree.add_investment('iron', 'small mine', 100, add=1)
        tree.add_investment('iron', 'large mine', 500, add=10)
        tree.add_investment('iron', 'new technology', 100, add=0.1)

        tree.add_investment_edge('small grain farm', 'large grain farm')
        tree.add_investment_edge('small fruit farm', 'large fruit farm')
        tree.add_investment_edge('small herd', 'large herd')
        tree.add_investment_edge('small quarry', 'large quarry')
        tree.add_investment_edge('small lumber mill', 'large lumber mill')
        tree.add_investment_edge('small press', 'large press')
        tree.add_investment_edge('small mine', 'large mine')

    def tokens_to_add(self):
        yield self.industry_tree
        yield self.investment_tree
        yield from self.industry_tree.groups
        yield from self.industry_tree.all_industries
        yield from self.investment_tree.all_investments

    def on_check(self, world):
        pass

    def on_execute(self, world):
        world.industry_tree = self.industry_tree
        world.investment_tree = self.investment_tree


class SetupPlayer(kxg.Message):

    def __init__(self, player):
        self.player = player
        self.player.cities = [City(self.player)]

    def tokens_to_add(self):
        yield self.player
        yield from self.player.cities

    def on_check(self, world):
        pass

    def on_execute(self, world):
        world.players.append(self.player)


class MakeInvestment(kxg.Message):

    def __init__(self, city, investment):
        self.city = city
        self.investment = investment

    def on_check(self, world):
        pass

    def on_execute(self, world):
        self.city.investments.append(self.investment)

