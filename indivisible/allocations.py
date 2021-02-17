"""
Represents an allocation of a indivisible items among agents ---  the output of an item-allocation algorithm.
Used mainly for display purposes.

Programmer: Erel Segal-Halevi
Since: 2020-11
"""

from typing import *
from fairpy.indivisible.agents import Agent, AdditiveAgent, Item, Bundle


class Allocation:
    """
    >>> Alice = AdditiveAgent({'x':1, 'y':2, 'z':3}, name="Alice")
    >>> George = AdditiveAgent({'x':3, 'y':2, 'z':1}, name="George")
    >>> A = Allocation([Alice, George], ["xy","z"])
    >>> print(A)
    Alice's bundle: {x,y},  value: 3,  all values: [3, 3]
    George's bundle: {z},  value: 1,  all values: [5, 1]
    <BLANKLINE>
    >>> B = Allocation([George, Alice])
    >>> B.set_bundles(["xy","z"])
    >>> print(B)
    George's bundle: {x,y},  value: 5,  all values: [5, 1]
    Alice's bundle: {z},  value: 3,  all values: [3, 3]
    <BLANKLINE>
    """

    def __init__(self, agents: List[Agent], bundles: List[Bundle] = None):
        self.agents = agents
        if bundles is None:
            bundles = [None] * len(agents)
        self.bundles = bundles

    def get_bundle(self, agent_index: int):
        return self.bundles[agent_index]

    def get_bundles(self):
        return self.bundles

    def set_bundle(self, agent_index: int, bundle: Bundle):
        """
        Sets the bundle of the given index.

        :param agent_index: index of the agent.
        :param bundle: a list of intervals.
        """
        self.bundles[agent_index] = bundle

    def set_bundles(self, bundles: List[Bundle]):
        """
        Sets the bundle of the given index.

        :param agent_index: index of the agent.
        :param bundle: a list of intervals.
        """
        self.bundles = bundles

    def __repr__(self):
        result = ""
        for i_agent, agent in enumerate(self.agents):
            agent_bundle = self.bundles[i_agent]
            agent_value = agent.value(agent_bundle)
            result += "{}'s bundle: {},  value: {},  all values: {}\n".format(
                agent.name(), stringify_bundle(agent_bundle), agent_value,
                [agent.value(bundle) for bundle in self.bundles],
                [agent_value - agent.value(bundle) for bundle in self.bundles],
            )
        return result


def stringify_bundle(bundle: Bundle):
    """
    Convert a bundle where each item is a character to a compact string representation.
    For testing purposes only.

    >>> stringify_bundle({'x','y'})
    '{x,y}'
    >>> stringify_bundle({'y','x'})
    '{x,y}'
    """
    return "{" + ",".join(sorted(bundle)) + "}"
    # return ",".join(["".join(item) for item in bundle])

'''
A class that represents a fractional allocation, that is, an allocation in which several agents can be given parts of 
the same object.
'''
class FractionalAllocation:
    """
       >>> agent1 = AdditiveAgent({'x':1, 'y':2, 'z':3}, name="agent1")
       >>> agent2 = AdditiveAgent({'x':3, 'y':2, 'z':1}, name="agent2")
       >>> A = FractionalAllocation([agent1, agent2], [{'x':0.5, 'y':0.5, 'z':0.5},{'x':0.5, 'y':0.5, 'z':0.5}])
       >>> print(A)
       agent1's bundle: {x,y,z},  value: 3.0
       agent2's bundle: {x,y,z},  value: 3.0
       <BLANKLINE>
       >>> A.value_of_fractional_allocation()
       6.0
       >>> agent3 = AdditiveAgent({'x':1, 'y':2, 'z':3}, name="agent3")
       >>> agent4 = AdditiveAgent({'x':3, 'y':2, 'z':1}, name="agent4")
       >>> B = FractionalAllocation([agent3, agent4], [{'x':0.4, 'y':0, 'z':0.5},{'x':0.6, 'y':1, 'z':0.5}])
       >>> print(B)
       agent3's bundle: {x,z},  value: 1.9
       agent4's bundle: {x,y,z},  value: 4.3
       <BLANKLINE>
       >>> B.value_of_fractional_allocation()
       6.2
       >>> agent3 = AdditiveAgent({'x':1, 'y':-2, 'z':3}, name="agent3")
       >>> agent4 = AdditiveAgent({'x':3, 'y':2, 'z':-1}, name="agent4")
       >>> C = FractionalAllocation([agent3, agent4], [{'x':0.4, 'y':0, 'z':0.5},{'x':0.6, 'y':1, 'z':0.5}])
       >>> print(C)
       agent3's bundle: {x,z},  value: 1.9
       agent4's bundle: {x,y,z},  value: 3.3
       <BLANKLINE>
       >>> C.value_of_fractional_allocation()
       5.2
       >>> agent5 = AdditiveAgent({'x':1, 'y':2, 'z':3}, name="agent5")
       >>> agent6 = AdditiveAgent({'x':3, 'y':2, 'z':1}, name="agent6")
       >>> FractionalAllocation([agent5, agent6], [{'x':0.4, 'y':0, 'z':0.5}])
       The amount of agents differs from the dictionaries that represent how much each agent received from each item.
       <BLANKLINE>
       >>> agent7 = AdditiveAgent({'x':1, 'y':2, 'z':3}, name="agent7")
       >>> agent8 = AdditiveAgent({'x':3, 'y':2, 'z':1}, name="agent8")
       >>> FractionalAllocation([agent7, agent8], [{'x':0.4, 'y':0, 'z':0.5},{'x':0.4, 'y':0, 'z':0.1},{'x':0.2, 'y':1, 'z':0.4}])
       The amount of agents differs from the dictionaries that represent how much each agent received from each item.
       <BLANKLINE>
       >>> agent9 = AdditiveAgent({'x':1, 'y':2, 'z':3}, name="agent9")
       >>> agent10 = AdditiveAgent({'x':3, 'y':2, 'z':1}, name="agent10")
       >>> FractionalAllocation([agent9, agent10], [{'x':0, 'y':0, 'z':0.5},{'x':0.6, 'y':1, 'z':5}])
       The values of the fractional allocation of items are not between 0 and 1
       Invalid input.
       <BLANKLINE>
    """

    # constructor
    def __init__(self, agents: List[AdditiveAgent], map_item_to_fraction: List[dict]):
        if len(agents) != len(map_item_to_fraction):
            print("The amount of agents differs from the dictionaries that represent how much each agent received from each item.")
            self.agents = None
            self.map_item_to_fraction = None
        elif check_input(map_item_to_fraction):
            self.agents = agents
            self.map_item_to_fraction = map_item_to_fraction
        else:
            print("Invalid input.")
            self.agents = None
            self.map_item_to_fraction = None

    # A method that calculates the value of the whole allocation. Returns float number.
    def value_of_fractional_allocation(self) -> float:
        result = 0
        for i_agent, agent in enumerate(self.agents):
                agent_value = get_value_of_agent_in_alloc(self.agents[i_agent].map_good_to_value, self.map_item_to_fraction[i_agent])
                result += agent_value
        return result

    # to string
    def __repr__(self):
        if self.agents is None and self.map_item_to_fraction is None:
            return ""
        else:
            result = ""
            for i_agent, agent in enumerate(self.agents):
                agent_bundle = stringify_bundle(get_items_of_agent_in_alloc(self.map_item_to_fraction[i_agent]))
                agent_value = get_value_of_agent_in_alloc(self.agents[i_agent].map_good_to_value, self.map_item_to_fraction[i_agent])
                result += "{}'s bundle: {},  value: {}\n".format(agent.name(),  agent_bundle, agent_value)
            return result


# -------------------------Help functions for the Fractional Allocation class--------------------------------------------
"""
The function checks the input value of the allocation.
That is, it checks:
1. All values of all items are between 0 and 1
2. There is no item whose sum of values is greater than 1
3. There is no item that has not been assigned to any agent, i.e. for each agent in the same item the value is 0
"""
def check_input(map_item_to_fraction: List[dict]) -> bool:
    """
    ### Examples of proper input
    >>> check_input([{'x':0.5, 'y':0.5, 'z':0.5},{'x':0.5, 'y':0.5, 'z':0.5}])
    True
    >>> check_input([{'x':0.4, 'y':0, 'z':0.5},{'x':0.6, 'y':1, 'z':0.5}])
    True

    ### Checks for values that are not in the range of 0 to 1
    >>> check_input([{'x':0.5, 'y':0.5, 'z':1.9},{'x':0.5, 'y':0.5, 'z':0.5}])
    The values of the fractional allocation of items are not between 0 and 1
    False
    >>> check_input([{'x':0.5, 'y':0.5, 'z':1},{'x':0.5, 'y':0.5, 'z':-0.1}])
    The values of the fractional allocation of items are not between 0 and 1
    False

    ### Checks for items whose sum of parts is greater than 1
    >>> check_input([{'x':0.7, 'y':0.5, 'z':0.5},{'x':0.9, 'y':0.5, 'z':0.5}])
    There is an item whose sum of parts is greater than 1
    False

    ### Checks for items that has not been assigned to any agent
    >>> check_input([{'x':0, 'y':0.5, 'z':0.5},{'x':0, 'y':0.5, 'z':0.5}])
    There is an item that has not been assigned to any agent
    False
    """
    sum_value_list = [0] * len(map_item_to_fraction[0])  # Help array
    for i in range(len(map_item_to_fraction)):
        for v, j in zip(map_item_to_fraction[i].values(), range(len(sum_value_list))):
            sum_value_list[j] += v
            if v > 1 or v < 0:
                print("The values of the fractional allocation of items are not between 0 and 1")
                return False

    for k in range(len(sum_value_list)):
        if sum_value_list[k] > 1:
            print("There is an item whose sum of parts is greater than 1")
            return False
        if sum_value_list[k] == 0:
            print("There is an item that has not been assigned to any agent")
            return False
    return True

'''
The function checks which objects the agent received by receiving map_item_to_fraction and then checks whether the value 
of the part he received from that item is greater than 1 if so he will add it to list another list no, and finally return the list of items.
'''
def get_items_of_agent_in_alloc(map_item_to_fraction: dict):
    """
    >>> print(get_items_of_agent_in_alloc({'x':0.4, 'y':0, 'z':0.5}))
    ['x', 'z']
    """
    result = []
    for key, val in zip(map_item_to_fraction.keys(), map_item_to_fraction.values()):
        if val > 0:
            result.append(key)
    return result

'''
Calculate the value of all the fractions of the items that a particular agent received
'''
def get_value_of_agent_in_alloc(value_of_the_whole_items: dict, amount_of_the_items: dict) -> float:
    """
    >>> get_value_of_agent_in_alloc({'x':1, 'y':2, 'z':3},{'x':0.5, 'y':0.5, 'z':0.5})
    3.0
    >>> get_value_of_agent_in_alloc({'x':1, 'y':2, 'z':3, 'p':9},{'x':0.1, 'y':0.5, 'z':0.8, 'p':0.7})
    9.8
    """
    value = 0
    for v1, v2 in zip(value_of_the_whole_items.values(), amount_of_the_items.values()):
        value += v1*v2
    return value


if __name__ == "__main__":
    import doctest
    (failures, tests) = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures, tests))







