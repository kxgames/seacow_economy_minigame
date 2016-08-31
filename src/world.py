#!/usr/bin/env python3

import kxg
import networkx

class World(kxg.World):

    def __init__(self):
        super().__init__()
        self.players = []
        self.industry_tree = None
        self.investment_tree = None

    @property
    def industries(self):
        return self.industry_tree.all_industries

    @property
    def cities(self):
        for player in self.players:
            yield from player.cities


class Player(kxg.Token):

    def __init__(self):
        super().__init__()
        self.cities = []
        self.wealth = 0
        self.wealth_per_sec = 0

    def on_update_game(self, dt):
        for city in self.cities:
            for industry in self.world.industries:
                self.wealth_per_sec += city.calculate_profit(industry)

        self.wealth += self.wealth_per_sec * dt


class City(kxg.Token):

    def __init__(self, player):
        super().__init__()
        self.player = player
        self.available_industries = []
        self.investments = []

    def calculate_supply(self, industry):
        # This function will be called many, many times each time the profits 
        # from each industry need to be worked out.  If this becomes a problem, 
        # caching the result should be very achievable.
        relevant_investments = [
                invst for invst in self.investments
                if invst.industry == industry
        ]
        supply_capacity = sum(x.supply_addend for x in relevant_investments)
        supply_efficiency = sum(x.supply_multiplier for x in relevant_investments)
        return supply_capacity * supply_efficiency

    def calculate_profit(self, industry):
        return self.calculate_supply(industry) * industry.calculate_price()


class Industry(kxg.Token):

    def __init__(self, name, base_demand, base_price):
        super().__init__()
        self.name = name
        self.base_demand = base_demand
        self.base_price = base_price

    def calculate_demand(self):
        # Currently the demand doesn't change, but in the future it should 
        # account for investments made in other industries, technologies 
        # researched, the global population, recent building construction, and 
        # other things in that vein.
        return self.base_demand

    def calculate_price(self):
        global_supply = sum(x.calculate_supply(self) for x in self.world.cities)
        if global_supply == 0: return 0
        return self.base_price * self.calculate_demand() / global_supply


class IndustryGroup(kxg.Token):
    
    def __init__(self, industries, base_demand):
        super().__init__()
        self.industries = industries
        self.base_demand = base_demand


class IndustryTree(kxg.Token):
    
    def __init__(self):
        super().__init__()
        self.table = {}
        self.graph = networkx.Graph()
        self.groups = []

    def __getitem__(self, name):
        return self.table[name]

    @property
    def all_industries(self):
        return self.table.values()

    def add_industry(self, name, base_demand, base_price):
        assert not self.world, "the industry tree should not change during the game"
        self.table[name] = Industry(name, base_demand, base_price)
        self.graph.add_node(name)

    def add_industry_edge(self, upstream_name, downstream_name):
        # I don't think this method isn't named very well.  It creates an edge 
        # in the industry tree, but it's easier to think of it as defining that 
        # the upstream industry produces the raw materials used by the 
        # downstream one.
        assert not self.world, "the industry tree should not change during the game"
        self.graph.add_edge(upstream_name, downstream_name)

    def add_industry_group(self, industry_names, base_demand):
        assert not self.world, "the industry tree should not change during the game"
        self.groups.append(IndustryGroup(
            [self.table[x] for x in industry_names], base_demand))


class Investment(kxg.Token):
    """
    Increase the supply for a particular industry.

    Investments can either add to the existing supply or multiply the existing 
    supply.  The former are typically buildings and the latter are typically 
    technologies.
    """

    def __init__(self, industry, name, cost, supply_addend, supply_multiplier=0):
        super().__init__()
        self.name = name
        self.industry = industry
        self.supply_addend = supply_addend
        self.supply_multiplier = supply_multiplier


class InvestmentTree(kxg.Token):

    def __init__(self, industry_tree):
        super().__init__()
        self.industry_tree = industry_tree
        self.table = {}
        self.graph = networkx.Graph()
     
    @property
    def all_investments(self):
        return self.table.values()

    def available_investments(self, city):
        pass

    def add_investment(self, industry_name, name, cost, add=0, mul=0):
        assert not self.world, "the investment tree should not change during the game"
        industry = self.industry_tree[industry_name]
        self.table[name] = Investment(name, industry, cost, add, mul)
        self.graph.add_node(name)

    def add_investment_edge(self, upstream_name, downstream_name):
        assert not self.world, "the investment tree should not change during the game"
        self.graph.add_edge(upstream_name, downstream_name)

