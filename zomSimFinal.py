##########################################
# YES, all of these packages are need =) #
##########################################
import random as rn
import matplotlib.pyplot as plt
import time
import plotly.express as px
from pandas import DataFrame

###########
# Classes #
###########
class colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    WHITE = '\33[37m'
    BLUE = '\33[34m'
    YELLOW = '\33[33m'
    END = '\033[0m'

    SUS = "blue"
    INF = "red"
    EV = "green"


class Point():
    def __init__(self):
        self.x = rn.randint(0, islandSize)
        self.y = rn.randint(0, islandSize)

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getLocation(self):
        return self.x, self.y


class Person(Point):
    def __init__(self, name):
        super().__init__()
        self.name = name


    def fightChance(self):
        return rn.randint(0, 100)

    def move(self):
        self.x += rn.randint(-1, 1)
        self.y += rn.randint(-1, 1)

        if self.x > islandSize:
            self.x = islandSize

        if self.x < 0:
            self.x = 0

        if self.y > islandSize:
            self.y = islandSize

        if self.y < 0:
            self.y = 0


class Susceptible(Person):
    def __init__(self, name):
        super().__init__(name)
        self.color = colors.SUS

    def escape(self):
        print(self.color + self.name + " has escaped safely!" + colors.END)

    def kill(self):
        return "Susceptible " + self.name + "has killed "

    def playDead(self):
        return rn.randint(0, 100)


class Infected(Person):
    def __init__(self, name):
        super().__init__(name)
        self.color = colors.INF
        self.evolve = rn.randrange(0, 100)

    def bite(self):
        return self.name + " has bitten "

    def evolveChance(self):
        if self.evolve >= 90:
            return True
        else:
            return False


class Evolved(Infected):
    def __init__(self, name):
        super().__init__(name)
        self.color = colors.EV

    def makeNoise(self):
        print(colors.WHITE + "You hear a faint roar in the distance..." + colors.END)


class Removed(Person):
    def __init__(self, name, timeOfDeath):
        super().__init__(name)
        self.color = colors.YELLOW
        self.timeOfDeath = timeOfDeath

    def getTimeOfDeath(self, name, timeOfDeath):
        print(name + " died at day " + str(timeOfDeath))


fnameList = ["John", "Geyson", "Raina", "Ranilo", "Evan", "Josh", "Nigel", "Deaz", "Justin", "Kamryn", "Darian",
             "Naoto", "Heather", "Komlan", "Stephon", "Anakin", "Yoda", "Ben", "Sheev", "Maul", "Tarkin", "Thrawn"]
lnameList = ["Camaclang", "Fernandez", "Wright", "Regino", "Timko", "Heredia", "Jennings", "Nunoo", "Kani-Yeboah",
             "Smolinski",
             "Jacobs", "Johnson", "Ono", "Craddock", "Attiogbe", "Fonrose", "Skywalker", "Kenobi", "Palpatine"]


##################################################################################################################
##################################################################################################################


gData = {} # Used for the animation later on


def main():
    global islandSize
    #############################################################
    # Ask user for input for however many Susceptibles          #
    #############################################################
    initSus = False
    while not initSus:
        susceptibleCount = int(input("Enter number of Susceptibles on Island (0 - 300): "))
        if susceptibleCount < 1:
            print("Susceptibles cannot be below 0!")
            initSus = False
        elif susceptibleCount > 300:
            print("Susceptibles are way too high!")
            initSus = False
        else:
            initSus = True

    #####################################################################################
    # Depending on the amount of Susceptibles the amount of zombies spawned will change #
    #####################################################################################
    initInfected = False
    while not initInfected:
        if susceptibleCount in range(150, 301):
            infectedCount = rn.randint(50, 100)
            initInfected = True
        elif susceptibleCount in range(25, 150):
            infectedCount = rn.randint(10, 50)
            initInfected = True
        elif susceptibleCount in range(10, 25):
            infectedCount = rn.randint(5, 10)
            initInfected = True
        else:
            infectedCount = rn.randint(2, 5)
            initInfected = True
    removedCount = 0
    evolvedCount = 0

    ########################
    # Generate island size #
    ########################
    initIsland = False
    while not initIsland:
        islandSize = int(input("Enter island size (25 - 400): "))
        if islandSize in range(25, 401):
            initIsland = True
        else:
            print("Error in island initialization!")
            initIsland = False

    #####################################
    # Lists to store from the main loop #
    #####################################
    sus = []
    inf = []
    ev = []
    rem = []

    #####################################
    # Create lists in gData             #
    #####################################
    gData["x"] = []
    gData["y"] = []
    gData["iter"] = []
    gData["id"] = []
    gData["size"] = []
    gData["color"] = []

    #######################
    # Counters for graphs #
    #######################
    sTest = susceptibleCount  # Used as the height of the graph (y-coordinate)
    days = []  # Used as the width of the graph (x-coordinate)
    sCount = []
    iCount = []
    rCount = []
    evCount = []

    ########################################################
    # Create objects from name list, attach to lists above #
    ########################################################
    for i in range(susceptibleCount):
        susTemp = Susceptible(rn.choice(fnameList) + " " + rn.choice(lnameList))
        sus.append(susTemp)


    for i in range(infectedCount):
        infTemp = Infected(rn.choice(fnameList) + " " + rn.choice(lnameList))
        inf.append(infTemp)

    ######################
    # Iterator & boolean #
    ######################
    i = 0
    done = False

    ############################################################################################
    # Main Loop, only done when Susceptible or infected are 0 or if infected and evolved are 0 #
    ############################################################################################
    while not done:
        days.append(i)
        sCount.append(susceptibleCount)
        iCount.append(infectedCount)
        rCount.append(removedCount)
        evCount.append(evolvedCount)

        #################################
        # Append data for the animation #
        #################################
        for s in sus:
            gData["x"].append(s.x)
            gData["y"].append(s.y) # The x and y coordinates of each class
            gData["iter"].append(i) # This is the frame the animation will be at
            gData["id"].append(s.name) # Will render individual circles for the animation
            gData["size"].append(1) # Size of the circles
            gData["color"].append(s.color) # Color of the circles

        for z in inf:
            gData["x"].append(z.x)
            gData["y"].append(z.y)
            gData["iter"].append(i)
            gData["id"].append(z.name)
            gData["size"].append(1)
            gData["color"].append(z.color)

        if evolvedCount > 0:
            for e in ev:
                gData["x"].append(e.x)
                gData["y"].append(e.y)
                gData["iter"].append(i)
                gData["id"].append(e.name)
                gData["size"].append(1)
                gData["color"].append(colors.BLUE)

        ###############################################################
        # Print which day and however many of each category there are #
        ###############################################################
        print("=====================================")
        print("Day {}".format(i))
        print("Susceptible: {}".format(susceptibleCount))
        print("Infected: {}".format(infectedCount))
        print("Evolved: {}".format(evolvedCount))
        print("Removed: {}\n".format(removedCount))
        i += 1

        ############################################################################
        # Iterate through each list of objects, events happens ONLY if susceptible #
        # is on the same x/y coordinate                                            #
        ############################################################################
        for s in sus:
            s.move()

        for z in inf:
            z.move()

        for z in inf:
            if z.evolveChance():
                # print(z.evolveChance())
                # time.sleep(5)
                newEv = Evolved(z.name)
                evolvedCount += 1
                ev.append(newEv)
                newEv.makeNoise()

                infectedCount -= 1
                inf.remove(z)

        for s in sus:
            for z in inf:

                if s.getLocation() == z.getLocation():
                    event = rn.randint(1, 3)

                    #########################################################################
                    # If event is 1, then the zombie and susceptible fight. The susceptible #
                    # only has a 25% chance of killing the infected                         #
                    #########################################################################
                    if event == 1:

                        if z.fightChance() >= 25:
                            print(colors.RED + z.bite() + s.name + "! They are now Infected!" + colors.END)
                            newInf = Infected(s.name)
                            infectedCount += 1
                            inf.append(newInf)
                            try:
                                susceptibleCount -= 1
                                sus.remove(s)
                            except:
                                pass

                        else:
                            print(colors.GREEN + s.kill() + "Infected " + z.name + colors.END)
                            newR = Removed(z.name, i)
                            removedCount += 1
                            rem.append(newR)

                            inf.remove(z)
                            infectedCount -= 1

                    #########################################################
                    # Susceptible has chances to escape or trick the zombie #
                    #########################################################
                    elif event == 2:
                        s.escape()
                    elif event == 3:
                        if s.playDead() >= 35:
                            print(
                                colors.BLUE + s.name + " played dead. It confused the zombie and ignored " + s.name + colors.END)
                        else:
                            print(colors.RED + z.name + " was not entertained by " + s.name + "'s trick." + colors.END)
                            newInf = Infected(s.name)
                            infectedCount += 1
                            inf.append(newInf)
                            try:
                                susceptibleCount -= 1
                                sus.remove(s)
                            except:
                                pass

        #########################################################################################################
        # Only when there are Evolved present would they move, similar events but lower chances of Susceptibles #
        # winning                                                                                               #
        #########################################################################################################
        if evolvedCount > 0:
            for e in ev:
                e.move()

            for s in sus:
                for e in ev:
                    if s.getLocation() == e.getLocation():
                        event = rn.randint(1, 3)

                        if event == 1:
                            if e.fightChance() >= 10:
                                print(colors.RED + e.bite() + s.name + "! They are now Infected!" + colors.END)
                                newInf = Infected(s.name)
                                infectedCount += 1
                                inf.append(newInf)

                                try:
                                    susceptibleCount -= 1
                                    sus.remove(s)
                                except:
                                    pass
                            else:
                                print(colors.GREEN + s.kill() + "Evolved " + e.name + colors.END)
                                newR = Removed(e.name, i)
                                removedCount += 1
                                rem.append(newR)

                                ev.remove(e)
                                evolvedCount -= 1

                        ##########################################################
                        # Susceptible has chances to escape or trick the evolved #
                        ##########################################################
                        elif event == 2:
                            s.escape()

                        elif event == 3:
                            if s.playDead() >= 35:
                                print(
                                    colors.GREEN + s.name + " played dead. It confused the zombie and ignored " + s.name + colors.END)
                            else:
                                print(colors.RED + e.name + " was not entertained by " + s.name + "'s trick." + colors.END)
                                newInf = Infected(s.name)
                                infectedCount += 1
                                inf.append(newInf)
                                try:
                                    susceptibleCount -= 1
                                    sus.remove(s)
                                except:
                                    pass

        ########################################################
        # Guard statements if there are evolved present or not #
        ########################################################
        if evolvedCount > 1:
            if i == 1000 or susceptibleCount == 0 or (infectedCount == 0 and evolvedCount == 0):
                done = True
        else:
            if i == 1000 or susceptibleCount == 0 or infectedCount == 0:
                done = True

    if done:
        print("Simulation Finished")

        #########
        # Graph #
        #########
        plt.plot(days, sCount, label="Susceptible")
        plt.plot(days, iCount, label="Zombie")
        plt.plot(days, rCount, label="Removed")
        plt.plot(days, evCount, label="Evolved")
        plt.legend()
        plt.title("Team 1.2 Simulation Graph")
        plt.xlabel("Time (Days)")
        plt.ylabel("Number of People")
        if (infectedCount > sTest + 5):
            plt.axis([0, len(days), 0, infectedCount + 5])
        else:
            plt.axis([0, len(days), 0, sTest + 5])
        plt.show()

        ################################################################################################
        # Close the first graph to start the animation, it will start in your browser                  #
        # This is the animation. If the iterations are above 500 PLEASE WAIT FOR THE ANIMATION TO LOAD #
        # Red circles = Infected                                                                       #
        # Blue circles = Susceptibles                                                                  #
        # Green = Evolved, but having a hard time implementing a third color for some reason           #
        ################################################################################################
        dataFrame = DataFrame(gData)
        fig = px.scatter(dataFrame, x="x", y="y", animation_frame="iter", animation_group="id", size="size", color="color", range_x=[-10, islandSize + 5 ], range_y=[-10, islandSize + 5])
        fig.show()

main()