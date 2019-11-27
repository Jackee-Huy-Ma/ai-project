import random
import torch
#Class used for ngrams. Basically a class representing a tripple
class RPS:
    def __init__(self,R, P, S):
        self.R = R
        self.P = P
        self.S = S
    
    def add(self,letter):
        if(letter == 'r'):
            self.R += 1
        
        if(letter == 'p'):
            self.P += 1
        
        if(letter == 's'):
            self.S += 1

    def total(self):
        return self.R + self.P + self. S
    
    def moves(self):
        maximum = max(self.R, self.P, self.S)
        # if everything is equal.
        if(maximum == self.R and maximum == self.P and maximum == self.S):
            return "rps"
        
        #TO DO for case of R == P and not S 
        if(maximum == self.R and maximum == self.P and maximum != self.S):
            return "rp"
        
        if(maximum == self.R and maximum == self.S and maximum != self.P):
            return "sr"
        
        if(maximum != self.R and maximum == self.P and maximum == self.S):
            return "ps"

        if(maximum == self.R):
            return "r"
        if(maximum == self.P):
            return "p"
        if(maximum == self.S):
            return "s"

    def debuging(self):
        print(f"R:{self.R} P:{self.P} S: {self.S}")
#Mapping out frequency of a Rock-Paper-Scissors Move of the user
userDataMap = {}

#String representing user move
userMoveString = ""

#All Possible Opening Move in Rock Paper Scissors    
openingMovesString = "rrr rrp rrs rss rsp rsr rpp rps rpr sss ssp ssr srr srp srs spp sps spr ppp pps ppr pss psp psr prr prs prp"

bigram = ""
turns = 0
aiPredict = ""
#Function that returns a list of Opening Moves
def openingMoves(s):
    tempString = s.split(' ')
    return tempString[random.randint(0, 27)]

openingMovesString = openingMoves(openingMovesString)

def ngrams(userMoves):
    if(len(userMoves) <= 2):
        return openingMovesString[turns]
        #print(len(userMoves))
        
    
    bigram = "" + userMoves[turns - 2] + userMoves[turns - 1]; 
    userMoves = userMoves.lower()
    index = 0
    needle = 0
    #print(f"bigrams:{bigram}")
    while(needle != 1):
        #print(f"userMoves: {userMoves}")
        #print(f"bigrams: {bigram}")
        needle = userMoves.find(bigram, index)
        index = needle + len(bigram)
        
        if((bigram not in userDataMap)):
            userDataMap.setdefault(bigram,RPS(0,0,0))
            
        if(needle == -1):
            break

        if(index >= len(userMoves) - 1):
            break

        if(userMoves[index] == ' '):
            continue
        
        if(userMoves[index] == 'r' or userMoves[index] == 'p' or userMoves[index] == 's'):
            userDataMap[bigram].add(userMoves[index])
    
    #print(f"AI Move:{userDataMap[bigram].moves()}")
    return userDataMap[bigram].moves()
#while(gameState):
while(True):
    #print("Enter Move: r or p or s")
    userInput = input()
    userMoveString += userInput
    #print(f"UserMoves:{userMoveString}")
    aiPredict = ngrams(userMoveString)
    turns += 1
    #print(f"User Move:{userInput}")
    print(f"all user Moves:{userMoveString}")
    print(f"AI Predict:{aiPredict}")
    print("Turn is over")