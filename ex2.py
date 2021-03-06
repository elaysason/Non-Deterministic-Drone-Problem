import operator
import sys
import random
import math
import itertools
from collections import deque


class DroneAgent:
    """
    A class used to represent a drone.

    Attributes
    ----------
    prob_path : list of tuples
        A list of the problomatic points for passage of drones. 
    map_size : tuple of ints
        The size of the map.
    package_number : int
        Number of packages in the game.
    last_turn_package : int
        The last turn in which a package was delivered,initialized to number of turns.
    turns_per_package : list of int.
        How many turns it took to deliver each package.
    """
    def __init__(self, initial):
        """
        Parameters
        ----------
        intial: Dictionary
            Intial state of the enviorment
        """
        
        prob_path = []
        i = 0
        for row in initial['map']:
            for j in range(len(row)):
                if row[j] == "I":
                    prob_path.append((i, j))
            i += 1
        self.prob_path = prob_path
        self.map_size = (len(initial['map']), len(initial['map'][0]))
        self.package_number = len(initial['packages'].keys())
        self.last_turn_package = initial['turns to go']
        self.turns_per_package = []
    
    def normalize(self, probs, state, client_num):
        """
        Normalize the probablities if the drone is one of the edges of the map.
        
        Parameters
        ----------
        probs : tuple of int.
            The probability to move in each direction(up, down, left, right, or stay in place).
        state : Dictionary
            Current state of the environment
        client_num : int
            The number of client
            
        Returns
        ----------
        list of int: Normalized probalities if the drone is on one of the edges of the map, else the problities.
        """
        changed_probs = list(probs)
        client = list(state['clients'].keys())[client_num]
        if state['clients'][client]['location'][0] == 0:
            changed_probs[0] = 0
        if state['clients'][client]['location'][1] == 0:
            changed_probs[2] = 0
        if state['clients'][client]['location'][0] == self.map_size[0]-1:
            changed_probs[1] = 0
        if state['clients'][client]['location'][1] == self.map_size[1]-1:
            changed_probs[3] = 0
        prob_factor = 1 / sum(changed_probs)
        return [prob_factor * p for p in changed_probs]
    
    def distance_in_map(self,state, source, destination):
        """
        Calculate the euclidean distance from the soucre to the desination.
        
        Parameters
        ----------
        state : Dictionary
            Current state of the environment.
        source : list of int.
            The source point.            
        destination : list of int.
            The destination point.    
        
        Returns
        ----------
        int : The euclidean between the points.
        """
        return ((source[0]-destination[0])**2 +(source[1]-destination[1])**2 )**0.5

    def packages_of_drone(self, drone, state):
        """
        Parameters
        ----------
        drone: str
            The name of the drone 
        state : Dictionary
            Current state of the environment.
            
        Returns
        ----------
        list of str: The packages that the drone carries.
        """
        packages = []
        for i, package_location in enumerate(state['packages'].values()):
            if package_location == drone:
                packages.append(list(state['packages'].keys())[i])
        return packages

    def in_map(self,point):
        """
        Checks if the point is in the map
        Parameters
        ----------
        point: tuple of int
            The point itself.
        
        Returns
        ----------
        bool : if the point in the map
        """
        return 0 <= point[0] <= self.map_size[0] - 1 and 0 <= point[1] <= self.map_size[1] - 1

    def actions(self, state):
        """
        Parameters
        ----------
        state : Dictionary
            Current state of the environment.
        
        Returns
        ----------
        list of tuples: The best possible actions from each kind to perform from the current state.
        """
        Alldrones_actions = []
        All_comb = []
        drones_pos = list(state["drones"].values())
        packs_pos = list(state["packages"].values())
        clients = [state["clients"]]
        drones_names = list(state["drones"].keys())
        clients_names = list(state["clients"].keys())
        packs_names = list(state["packages"].keys())
        drone_num = 0
        for point in drones_pos:
            drone_actions = []
            x_pos = point[0]
            y_pos = point[1]
            packges_of_drone = self.packages_of_drone(list(state['drones'].keys())[drone_num], state)
            # check for delivery
            is_delivered = False
            for i,client in enumerate(list(clients[0].values())):
                client_loc = client["location"]
                client_wpacs = client["packages"]
                if ((x_pos, y_pos) == client_loc) and (len(packges_of_drone) > 0):
                    if packges_of_drone[0] in client_wpacs:
                        drone_actions.append(
                            ("deliver", drones_names[drone_num], clients_names[i], packges_of_drone[0]))
                        is_delivered = True
                    if len(packges_of_drone) > 1:
                        if packges_of_drone[1] in client_wpacs:
                            drone_actions.append(
                                ("deliver", drones_names[drone_num], clients_names[i], packges_of_drone[1]))
                            is_delivered = True
            if is_delivered:
                drone_num += 1
                Alldrones_actions.append(drone_actions)
                continue
            # get the best move direction
            directions = [[0, 1], [1, 0], [0, -1], [-1, 0], [1, 1], [-1, -1], [1, -1], [-1, 1]]
            legal_directions = [direction for direction in directions if (x_pos + direction[0],y_pos+direction[1])
                                not in self.prob_path and self.in_map((x_pos + direction[0],y_pos+direction[1]))]
            cost = [[self.move_score(state,[x_pos+direction[0],y_pos+direction[1]],drones_names[drone_num]),direction]
                    for direction in legal_directions]
            min_move_cost = min(cost)
            # check for pickup
            pickup_score = [-sys.maxsize,[]]
            if (x_pos, y_pos) in packs_pos and (len(packges_of_drone) < 2):
                for pac in range(len(packs_pos)):
                    if packs_pos[pac] == (x_pos, y_pos):
                        pickup_score[0] = 2
                        pickup_score[1].append(pac)
            # check if wait should be added.
            wait_score = self.wait_score(state,drones_names[drone_num])
            if wait_score == max([-1 * min_move_cost[0],pickup_score[0],wait_score]):
                drone_actions.append(("wait", drones_names[drone_num]))
            elif pickup_score[0] == max([-1 * min_move_cost[0],pickup_score[0],wait_score]):
                for p in pickup_score[1]:
                    drone_actions.append(("pick up", drones_names[drone_num],packs_names[p]))
            drone_actions.append(
                ("move", drones_names[drone_num], (x_pos + min_move_cost[1][0], y_pos + min_move_cost[1][1])))
            drone_num += 1
            Alldrones_actions.append(drone_actions)

        for act in itertools.product(*Alldrones_actions):
            All_comb.append(act)
            # check for same drones pickup
        if len(drones_pos) > 1:
            for comb in All_comb:
                if (len(comb[0]) < 3) or (len(comb[1]) < 3):
                    continue
                else:
                    if (comb[0][0] == 'pick up') and (comb[1][0] == 'pick up'):
                        if (comb[0][2] == comb[1][2]):
                            All_comb.remove(comb)
        All_comb.append(tuple([('reset')]))
        All_comb.append(tuple([('terminate')]))
        return All_comb

    def client_package(self, state, package):
        """
        Parameters
        ----------
        state : Dictionary
            Current state of the environment.
        package: str
            The name of the package     
        
        Returns
        ----------
        The client who wants the package, None if no client wants it.
        """
        for i, client in enumerate(state['clients'].values()):
            if package in client['packages']:
                return i
        return None

    def closet_drone(self, state,drones,drone, package_location):
         """
        Parameters
        ----------
        state : Dictionary
            Current state of the environment.
        drones: Dictionary
            all drones
        drone:
            drone name to not inculde
        package_location : tuple
            the location of the package
        
        Returns
        ----------
        int : The min distance from the package to a drone
        """
        min = sys.maxsize
        i = 0
        for d in drones:
            if d == drone:
                continue
            cur_value = self.distance_in_map(state, list(package_location), list(state['drones'][d]))
            if cur_value < min:
                min = cur_value
            i += 1
        return min

    def next_move(self,state,client):
        """
        Parameters
        ----------
        state : Dictionary
            Current state of the environment.
        client : int
            The number of the client
        
        Returns
        ----------
        list : the location of the client after the next likely move.
        """
        directions = [[0, 1], [1, 0], [0, -1], [-1, 0], [0, 0]]
        prob = self.normalize(list(state['clients'].values())[client]['probabilities'],state,client)
        indices = [i for i, x in enumerate(prob) if x == max(prob)]
        return [list(map(operator.add, list(state['clients'].values())[client]['location'], directions[i])) for i in indices]

    def wait_score(self,state, drone):
        """
        Parameters
        ----------
        state : Dictionary
            Current state of the environment.
        drone : str
            The drone name.
        
        Returns
        ----------
        int : a score given to the wait action.
        """
        drone_packs = self.packages_of_drone(drone, state)
        if len(drone_packs) == 0:
            return -50000
        clients = [self.client_package(state, package) for package in drone_packs]
        clients_distance = [min([self.distance_in_map(state, state['drones'][drone], next) for next in self.next_move(state,i)]) for i in clients]
        clients_min = min(clients_distance)
        if clients_min == 0:
            return 3
        return -10000

    def move_score(self, state, pos_after_move, drone):
        """
        Parameters
        ----------
        state : Dictionary
            Current state of the environment.
        pos_after_move : list
            The point after making a move action
        drone : str
            The drone name.
        
        Returns
        ----------
        int : a score given to the move action.
        """
        dis = 0
        drone_packs = self.packages_of_drone(drone, state)
        packages = list(state['packages'].values())
        free_packages = [[package,list(state['packages'])[i]] for i,package in enumerate(packages) if not isinstance(package,str)]
        packages_dist = [self.distance_in_map(state, pos_after_move, package[0]) for package in free_packages]
        package_min_index = -1
        if len(free_packages) != 0:
            packages_min = min(packages_dist)
            package_min_index = packages_dist.index(packages_min)
            dis += packages_min
        if len(drone_packs) != 0:
            clients = [self.client_package(state, package) for package in drone_packs]
            clients_dist = [self.distance_in_map(state, pos_after_move, self.next_move(state,i)[0]) for i in clients]
            clients_min = min(clients_dist)
            if len(drone_packs) == 1 and len(free_packages) != 0:
                drones = state['drones']
                if self.closet_drone(state,drones,drone,free_packages[package_min_index][0]) == 0:
                    return -10
                else:
                    return min([clients_min,dis])
            else:
                return clients_min
        else:
            return dis

    def act(self, state):
        """
        Parameters
        ----------
        state : Dictionary
            Current state of the environment.
        
        Returns
        ----------
        tuple : a global act(act for each drone) given the state.
        """
        all_comb = self.actions(state)
        global_act_score = -sys.maxsize
        global_act_index = 0
        if len(state['packages']) == 0:
            turns = state['turns to go']
            if turns >= 2 * (sum(self.turns_per_package)/len(self.turns_per_package)) and self.package_number>= 2:
                return all_comb[-2][0]

        del all_comb[-1]
        del all_comb[-1]
        for i, global_act in enumerate(all_comb):
            curr_score = 0
            for atomic_act in global_act:
                if atomic_act[0] == 'deliver':
                    curr_score += 60
                if atomic_act[0] == 'pick up':
                    curr_score += 2
                if atomic_act[0] == 'move':
                    curr_score -= self.move_score(state, atomic_act[2], atomic_act[1])
                if atomic_act[0] == 'wait':
                    wait_score = self.wait_score(state,atomic_act[1])
                    curr_score += wait_score
            if curr_score > global_act_score:
                global_act_score = curr_score
                global_act_index = i
            actions = [atomic[0] for atomic in all_comb[global_act_index]]
            if 'deliver' in actions:
                self.turns_per_package.append(self.last_turn_package - state['turns to go'])
                self.last_turn_package = state['turns to go']
        return tuple(all_comb[0])
