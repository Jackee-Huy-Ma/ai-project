import random
import string

#https://www.gkbrk.com/wiki/hill_climbing/
#For Hill climbing please go to this person's website
#Contains an excellent tutorial

target = "artificial intelligence"
userTries = 0
aiTries = 0
userScore = 0
aiScore = 0
userAnswer = ""
def generate_word(length = len(target)):
    return [random.choice(string.printable) for _ in range(length)]

def score(word):
    difference = 0
    
    for i in range(len(target)):
        myLetter = word[i]
        acutalLetter = target[i]
        difference += abs(ord(myLetter) - ord(acutalLetter)) 

    return difference
#Simple Game Guess word


# AI will hillclimb it's way to the word.
def ai_change(word):
    i = random.randint(0, len(word) - 1)
    word[i] = random.choice(string.printable)


print("Guess Word Game!")

while(userAnswer != target):
    userAnswer = input()
    userTries += 1
    userScore = score(userAnswer)
    print(f"user Attempts:{userTries}, userScore:{userScore}")

aiGuess = generate_word()
aiScore = score(aiGuess)

while True:
    aiTries +=1
    print(f"AI GUESS: {aiGuess} turn:{aiTries}, Distance from actual word: = {aiScore}")
    aiTrylist = list(aiGuess)
    ai_change(aiTrylist)
    tempAIScore = score(aiTrylist)
    if score(aiTrylist) < aiScore:
        aiGuess = aiTrylist
        aiScore = tempAIScore 
    
    if aiScore == 0:
        print(f"AI GUESS: {aiGuess} turn:{aiTries}, Distance from actual word: = {aiScore}")
        break
