from agent.agent import *
import numpy as np
from debug import *
import copy
import operator
class beeInfo:
    def __init__(self, direction, velocity, state, AtHub):
        self.direction = direction #stored in degrees
        self.velocity = velocity
        self.state = state
        self.atHub = AtHub
        #include a variable projecting at what time it left the hub? (add later)

class hubController:
    def __init__(self, radius, agents, environment):
        self.reset(radius, agents, environment)


    def beeCheckOut(self, bee):
        #eprint("BEECHECKOUT: ")
        #eprint(".. id:", bee.id, "Angle:", np.rad2deg(bee.direction), ".. bee in hub?:", bee.inHub)
        angle = bee.direction % (2*np.pi)
        angle = int(int(angle*(180/np.pi))/5) #converting to fit in the array
        agent = self.agentList[bee.id]
        if (self.directionParams[angle] == -1):      #No user input, all is well
            eprint("checking out:", bee.id, "direction:", int(bee.direction*(180/np.pi)))
            self.directions[angle] = self.directions[angle] + 1
            agent.atHub = 0
        elif self.directionParams[angle] < self.directions[angle]: #too many bees, stop it!
            eprint("INHIBITED!!!!! ")
            eprint("Angle:", angle, "  Id:", bee.id, "  Bee in hub?:", bee.inHub)
            self.environment.sort_by_state(bee.id, bee.state.__class__, Observing().__class__)
            bee.state = Observing(bee)
        elif (self.directionParams[angle] > self.directions[angle]): #there needs to be more bees in that direction anyways
            eprint("checking out:", bee.id, "direction:", int(bee.direction*(180/np.pi)))
            self.directions[angle] = self.directions[angle] + 1
            agent.atHub = 0
        elif self.directionParams[angle] == self.directions[angle]: #perfect amount of bees, stop it
            eprint("INHIBITED!!!!! ")
            eprint("Angle:", angle, "  Id:", bee.id, "  Bee in hub?:", bee.inHub)
            self.environment.sort_by_state(bee.id, bee.state.__class__, Observing().__class__)
            bee.state = Observing(bee)

        agent.direction = angle*5
        #eprint("going in:", agent.direction)
        agent.state = bee.state
        return agent.atHub
         #******if explorer set a timer for it, if assessor calculate projected time
        #so upon check out state is used to gauge stuff for right now it can just be used as the array

    def beeCheckIn(self, id,dir): #technically only explorers or assessors will ever call this (which they do as they enter the hub)
        #check if they are coming in from a weird angle if they're assessors, which can be a 'red flag'
        eprint("checking in:", id, " Initial direction:", self.agentList[id].direction, " from:", int(dir*(180/np.pi))+180)
        angle = int(self.agentList[id].direction/5)
        #angle = angle % (2 * np.pi)
        #angle = int(int(angle * (180 / np.pi)) / 5)   # converting to fit in the array
        self.directions[angle] = self.directions[angle] - 1
        #if self.directions[angle] < 0:
            #eprint("IT's negative!!")
            #eprint("id:",id, " directionsValue:",self.directions[angle], " angle:", angle*5)
        self.agentList[id].atHub = 1

    def handleRadialControl(self, jsonInput):
        #eprint(jsonInput)
        jsonDict = jsonInput['state'] # id, dictionary(r:radian, deg: degrees, val: 1-30)
        self.directionInput(jsonDict['deg'],jsonDict['val'])

    def directionInput(self, direction, newValue): #user inhibits or excites the amount of bees in each direction
                                                    #direction is given in degrees

        angle = int(int(direction % 360) / 5)   # converting to fit in the array

        self.directionParams[angle] = int(newValue)
        #eprint(angle)
        #eprint(int(newValue))

    def hiveAdjust(self, bees):
        #sortedParams = sorted(self.directionParams, operator.getitem(1), Reverse=True)
        # ^^this is so it will adjust the bees based on the biggest difference or the lowest difference first, an option if this is a problem
        for counter in range(0, 72): #the one problem with this is then the lower buckets have priority of sending bees out hence ^^
            angle = counter
            if self.directionParams[angle] == -1:  # No user input, all is well
                #eprint("test1")
                pass
            elif self.directionParams[angle] < self.directions[angle]:  # too many bees, just keep stopping them from leaving
                #eprint("test2")
                pass
            elif self.directionParams[angle] > self.directions[angle]:  # not enough bees send out more! from observers

                for id,bee in bees.items(): #use environment classes soon.
                    if bee.state.__class__ == Observing().__class__ and bee.inHub is True: #to speed up keep a list of the observers..
                        if np.random.random() < 0.5: #this gives a 50% chance of it happening
                            break
                        #eprint("hiveadjust: ")
                        #eprint("angle:",angle*5, ".. id:",bee.id, ".. bee in hub?:", bee.inHub)

                        bee.state = Exploring(bee)
                        self.environment.sort_by_state(bee.id, Observing().__class__, Exploring().__class__)
                        bee.state.inputExplore=True
                        bee.state.exploretime *= 0.5 #since the bees are going out in an almost straight line.
                        bee.direction = ((angle*5)/180)*np.pi
                        self.directions[angle] += 1
                        agent = self.agentList[bee.id]
                        agent.direction = angle*5
                        agent.atHub = 0
                        bee.inHub = False
                        break # only execute this once per iteration, that way it's a 'slow' change
            elif self.directionParams[angle] == self.directions[angle]:  #meaning it has reached the user's requirements
                #pass
                self.directionParams[angle] = -1


    def reset(self, radius, agents, environment):
        self.environment = environment
        self.radius = radius  # needs an array of direction parameters
        self.directions = [None]*72  # #bees that have left the hub in each direction
        self.directionParams = [None]*72  # #desired user values
        # counter * (np.pi / 72)
        self.agentList = {}
        for counter in range(0, 72):
            self.directions[counter] = 0
            self.directionParams[counter] = -1
        # self.directionParams[10] = 10
        for id, bee in agents.items():
            info = beeInfo(int(bee.direction * (180 / np.pi)), bee.velocity, bee.state, 1)
            self.agentList[bee.id] = info


    def convertToIndex(self, degrees):
        int(int(degrees % 360) / 5)


'''
Hub controller TODO: add functionality for the mission state
 fix check ins!!'''

