#!/usr/bin/env python3

import kxg
import networkx as nx

class World(kxg.World):

    def __init__(self):
        self.players = []
        self.industry_tree = None
        self.investment_tree = None


class Player(kxg.Token):

    def __init__(self):
        self.cities = []
        self.wealth = 0


class City(kxg.Token):

    def __init__(self):
        self.available_industries = []
        self.investments = []


class Industry(kxg.Token):

    def __init__(self, name, base_demand, base_price):
        self.name = name
        self.base_demand = base_demand
        self.base_price = base_price


class IndustryGroup(kxg.Token):
    
    def __init__(self, industries, base_demand):
        self.industries = industries
        self.base_demand = base_demand


class IndustryTree(kxg.Token):
    
    def __init__(self):
        super().__init__()
        self.table = {}
        self.graph = networkx.Graph()
        self.groups = []

    @property
    def all_industries(self):
        return self.table.values()

    def add_industry(self, name, base_demand, base_price):
        assert not self.world, "the industry tree should not change during the game"
        self.table[name] = Industry(name, base_demand, base_price)
        self.graph.add_node(name)

    def add_industry_edge(self, upstream_name, downstream_name):
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
        self.name = name
        self.industry = industry
        self.supply_addend = supply_addend
        self.supply_multiplier = supply_multiplier


class InvestmentTree:

    def __init__(self, industry_tree):
        super().__init__()
        self.industry_tree = industry_tree
        self.table = {}
        self.graph = nx.Graph()
     
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

