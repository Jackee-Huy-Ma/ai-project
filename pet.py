import math
from enum import Enum
from random import randint
# Pet.py is a small project that demonstrates Goal Oriented Behavior
# Basic Run through of this game is to interact with a digital pet
# The pet AI will decide which State it will be in. E.g (Hungry, Sleepy, Energetic, Etc)
# All the player has to do is just hit enter after naming pet
# Note this is super unrealistic and most of the time te AI State / Action does not make sense.
class AIGoals(Enum):
    REST = 1
    MOVE = 2
    EAT = 3
    BATHROOM = 4

class AIActions:
    def __init__(self):
        self.DRINKWATER = [(AIGoals.BATHROOM.name, 1), (AIGoals.EAT.name, -1), "DRINKWATER"]
        self.VISITBATHROOM = [(AIGoals.BATHROOM.name, -1), (AIGoals.EAT.name, 1), "VISITBATHROOM"]
        self.BEDTIME = [(AIGoals.REST.name, -1), (AIGoals.MOVE.name, 1), "BEDTIME"]
        self.EATALOT = [(AIGoals.EAT.name, -1), (AIGoals.MOVE.name, 1), "EATALOT"]
        self.RUN = [(AIGoals.MOVE.name, -1), (AIGoals.REST.name, 1), "RUN"]
        self.DIGEST = [(AIGoals.EAT.name, - 1), (AIGoals.REST.name, 1), "DIGEST"]
        self.HUNGRY = [(AIGoals.EAT.name, 1), (AIGoals.BATHROOM.name, -1), "HUNGRY"]
        self.THIRSTY = [(AIGoals.BATHROOM.name, 1), (AIGoals.MOVE.name, -1), "THIRSTY"]
        self.masterActionList = [self.DRINKWATER, self.VISITBATHROOM, self.BEDTIME, self.EATALOT, self.RUN, self.DIGEST, self.HUNGRY, self.THIRSTY]
class State:
    def __init__(self):
        self.action = None
    
    def __init__(self, action):
        self.action = action
    
    def run(self):
        assert 0, "Error, run not implemented"
    
    def next(self, input):
        assert 0, "Error, next not implemented"

class StateMachine:
    def __init__(self, initialState):
        self.currentState = initialState

    def run(self):
        self.currentState = self.currentState.run()

class Goals:
    def __init__(self):
        self.goal_dict = dict()
        for goals in AIGoals:
            self.goal_dict.setdefault(goals.name, 5)
            #print(goals.name)
       
    def setGoal(key, value):
        if key not in self.goal_dict:
            self.goal_dict.setdefault(key, randint(0, 9))
            return
        self.goal_dict[key] = value
        
class Neutral(State):
    def __init__(self):
        self.action = None
    
    def run(self, AI):
        print(f"{AI.name} is neutral")
        AI.StateMachine.currentState = Neutral()

class Rest(State):
    def __init__(self):
        self.action = None
    
    def run(self, AI):
        print(f"{AI.name} is resting")
        AI.StateMachine.currentState = Neutral()

class Move(State):
    def __init__(self):
        self.action = None
    
    def run(self, AI):
        print(f"{AI.name} is Moving")
        AI.StateMachine.currentState = Neutral()

class Eat(State):
    def __init__(self):
        self.action = None
    
    def run(self, AI):
        print(f"{AI.name} is eating")
        AI.StateMachine.currentState = Neutral()

class Bathroom(State):
    def __init__(self):
        self.action = None
    
    def run(self, AI):
        print(f"{AI.name} is going to the bathroom")
        AI.StateMachine.currentState = Neutral()

class AiPet:
    def __init__(self, name):
        self.name = name
        self.StateMachine = StateMachine(Move())
        self.Goals = Goals()
        self.aiActions = AIActions()

    def chooseState(self):
        tempAction = self.aiActions.masterActionList[0]
        minDiscontentment = 90
        tempTieList = []
        for i in range(len(self.aiActions.masterActionList)):
            actualDiscontentment = 0
            for j in range(len(self.aiActions.masterActionList[i]) -1):
                #tempDiscounting += (self.aiActions.masterActionList[i])
                #print(self.aiActions.masterActionList[i][j][1])
                #print(self.aiActions.masterActionList[i][j][0])
                actualDiscontentment += math.pow((self.aiActions.masterActionList[i][j][1] + self.Goals.goal_dict.get(self.aiActions.masterActionList[i][j][0])), 2)
            if(minDiscontentment == actualDiscontentment):
                tempTieList.append(self.aiActions.masterActionList[i])

            if(minDiscontentment > actualDiscontentment):
                minDiscontentment = actualDiscontentment
                tempAction = self.aiActions.masterActionList[i]
            #print(f"{self.aiActions.masterActionList[i][len(self.aiActions.masterActionList[i]) - 1]}:", end='')
        
        if(len(tempTieList) > 1):
            tempAction = tempTieList[randint(0, len(tempTieList) - 1)]

        print(f"Minimum Discontentment:{minDiscontentment} caused by Action:{tempAction[len(tempAction) - 1]}")
        
        for i in range(len(tempAction) - 1):
            newGoalValue = self.Goals.goal_dict.get(tempAction[i][0]) + tempAction[i][1]

            if(newGoalValue <= 0):
                newGoalValue = 1

            self.Goals.goal_dict[tempAction[i][0]] = newGoalValue

        maximum = -1
        
        tempkeyTie = []
        for key, value in self.Goals.goal_dict.items():
            if(maximum <= value):
                maximum = value
                #print(f"key:{key}, value:{value}")

        for key, value in self.Goals.goal_dict.items():
            if(maximum == value):
                #print(f"Maximum:{maximum} key:{key}")
                tempkeyTie.append(key)
        
        if(maximum >= 3):
           for i in range(len(tempkeyTie)):
               self.Goals.goal_dict[tempkeyTie[i]] = 1

        if(len(tempkeyTie) == 1):
            #print("No Ties")
            if(tempkeyTie[0] == AIGoals.MOVE.name):
                self.StateMachine.currentState = Move()
                return
            elif(tempkeyTie[0] == AIGoals.EAT.name):
                self.StateMachine.currentState = Eat()
                return
            elif(tempkeyTie[0] == AIGoals.BATHROOM.name):
                self.StateMachine.currentState = Bathroom()
                return
            elif(tempkeyTie[0] == AIGoals.REST.name):
                self.StateMachine.currentState = Rest()
                return

        randomTieBreakerChoice = tempkeyTie[randint(0, len(tempkeyTie) - 1)]
        
        if(randomTieBreakerChoice == AIGoals.MOVE.name):
            self.StateMachine.currentState = Move()
        elif(randomTieBreakerChoice == AIGoals.EAT.name):
            self.StateMachine.currentState = Eat()
        elif(randomTieBreakerChoice == AIGoals.BATHROOM.name):
            self.StateMachine.currentState = Bathroom()
        elif(randomTieBreakerChoice == AIGoals.REST.name):
                self.StateMachine.currentState = Rest()
            
def main():
    print("Welcome to Pet.py!")
    print("Please give your pet AI a name.")
    aiPet = AiPet(input())
    '''
    print(len(aiPet.aiActions.masterActionList))
    print(len(aiPet.Goals.goal_dict))
    
    for key, data in aiPet.Goals.goal_dict.items():
        print(key, data)
    '''
    while True:
        #print(aiPet.name)
        aiPet.chooseState()
        for key, data in aiPet.Goals.goal_dict.items():
            print(key, data)
        aiPet.StateMachine.currentState.run(aiPet)
       
        userInput = input()
    
if __name__ == '__main__':
    main()
