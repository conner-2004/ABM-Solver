import numpy as np
import random
import copy
import pandas as pd

from scipy.optimize import minimize
import tkinter as tk
from tkinter import ttk
p1SelectedRNG = ""
p2SelectedRNG = ""
player1 = ""
player2 = ""
options = [
        'Lucky', 'Advantaged', 'Thief', 'Juggernaut', 'Stunner',
        'Duplicator', 'Gambler', 'Tax Collector', 'Copywriter',
        'Conjurer', 'The Sumo', 'Fireborne', 'Retired', 'Parrymaster',
        'Cheater', 'Cupid', 'Investor', 'Defender', 'Last Ditch',
        'Null', 'Joe'
    ]

#turn=1
wins = 0
winRate = 0
movestackOptions = []
oppMovestackOptions = []
center_frame = ""


class player():
    def __init__(self, inputClass, **kwargs):
        self.chosenClass = inputClass
        self.movestackMade = False
        self.stackChoice = ""
        self.activeMove = ""
        self.mana = 1
        self.blocks = 5
        self.attackCost = 1
        if self.chosenClass == "Lucky" or self.chosenClass == "Advantaged" or self.chosenClass == "Juggernaut" or self.chosenClass == "Stunner" or self.chosenClass == "Duplicator" or self.chosenClass == "Gambler" or self.chosenClass == "Copywriter" or self.chosenClass == "The Sumo" or self.chosenClass == "Retired" or self.chosenClass == "Cheater" or self.chosenClass == "Cupid" or self.chosenClass == "Investor" or self.chosenClass == "Defender" or self.chosenClass == "Last Ditch" or self.chosenClass == "Joe":
            self.stacksLeft = 0
            if self.chosenClass == "Cupid":
                self.copiesLeft = 1
            elif self.chosenClass == "Juggernaut" or self.chosenClass == "Stunner":
                self.attackStreak = 0
            elif self.chosenClass == "Copywriter":
                self.copyStreak = 1
                self.oppLastMove = ""
            elif self.chosenClass == "Duplicator":
                self.manaStreak = 0
            elif self.chosenClass == "Retired":
                self.mana = 7
            elif self.chosenClass == "Investor":
                self.mana = 5
            elif self.chosenClass == "Last Ditch":
                self.lastDitchCounter = 0
                self.extraManaAdded = 0
            elif self.chosenClass == "Gambler":
                self.blocks = 3
        elif self.chosenClass == "Thief":
            self.stacksLeft = 1
        elif self.chosenClass == "Tax Collector":
            self.stacksLeft = 3
        elif self.chosenClass == "Conjurer":
            self.stacksLeft = 2
        elif self.chosenClass == "Fireborne":
            self.stacksLeft = 1
            self.extraLifetimeRemaining = 0
        elif self.chosenClass == "Parrymaster":
            self.stacksLeft = 3
            self.succesfullyParried = False
        elif self.chosenClass == "Null":
            self.stacksLeft = 1

        self.__dict__.update(kwargs)

    def deep_copy(self):
        """Creates a deep copy of the current object."""
        return copy.deepcopy(self)




def main_simul(player1,player2,player1InitialState,player2InitialState,turn):
    #global turn
    winner = ""
    game_over = False
    #turn = 1
 #  print(player1.mana, "          ", player2.mana)
 #   print(player1.blocks, "          ", player2.blocks)
    while game_over == False:

        # if p1 is conjured class and has the ability available ask if they want to use it
        # if yes - check if p2 is conjured class an ask if they want to use it
        # if p2 is not conjured class then make sure p2 picks the move first
        # elif p2 is conjured and has ability availably ask if they want to use it
        # if yes - make sure p1 picks the move first
        # if neither used conjure ability carry on as normal.




        if player1.chosenClass == "Conjurer" and player1.stacksLeft > 0 and player1.mana > 0:
            p1reasonableMoves = findReasonableMovestacks(player1, player2, player1InitialState,
                                                         player2InitialState, turn,False, False)     #   print(reasonableMoveStacks)
            randNumb = random.randint(0, len(p1reasonableMoves) - 1)
            player1.stackChoice = p1reasonableMoves[randNumb][0]
            if player2.chosenClass == "Conjurer" and player2.stacksLeft > 0 and player2.mana > 0:
                if player1.stackChoice == "y":
                    #print(player1.mana)
                    p2reasonableMoves = findReasonableMovestacks(player2, player1,player2InitialState,
                                                                 player1InitialState,turn, False, False)
                    randNumb = random.randint(0, len(p2reasonableMoves) - 1)
                    player2.stackChoice = p2reasonableMoves[randNumb][0]
                    if player2.stackChoice == "n":
                        #print("Player 1 has conjured. They can see your move.")
                        p2reasonableMoves = findReasonableMovestacks(player2,player1,player2InitialState,player1InitialState,turn,False,True)
                        randNumb = random.randint(0, len(p2reasonableMoves) - 1)
                        player2.activeMove = p2reasonableMoves[randNumb][1]
                        #print(f"Player 2 has elected to {player2.activeMove}")
                        p1reasonableMoves = findReasonableMovestacks(player1,player2,player1InitialState,player2InitialState,turn,True,True)
                        randNumb = random.randint(0, len(p1reasonableMoves) - 1)
                        player1.activeMove = p1reasonableMoves[randNumb][1]
                        player1.mana -= 1
                    elif player2.stackChoice == "y":
                        #print("Both conjured. Cancels out.")
                        player1.stackChoice = "n" #remove all y stackchoices from reasonablemoves
                        player2.stackChoice = "n" #remove all y stackchoices form reasonablemoves
                        #generate new random movestacks for both
                        player1.mana -= 1
                        player2.mana -= 1
                elif player1.stackChoice == "n":
                    p2reasonableMoves = findReasonableMovestacks(player2,player1,player2InitialState,player1InitialState,turn,False,False)
                    randNumb = random.randint(0, len(p2reasonableMoves) - 1)
                    player2.stackChoice = p2reasonableMoves[randNumb][0]
                    if player2.stackChoice == "y":
                        #print("Player 2 has conjured. They can see your move.")
                        p1reasonableMoves = findReasonableMovestacks(player1,player2,player1InitialState,player2InitialState,turn,False,True)
                        randNumb = random.randint(0, len(p1reasonableMoves) - 1)
                        player1.activeMove = p1reasonableMoves[randNumb][1]
                        #print(f"Player 1 has elected to {player1.activeMove}")
                        p2reasonableMoves = findReasonableMovestacks(player2,player1,player2InitialState,player1InitialState,turn,True,True)
                        randNumb = random.randint(0, len(p2reasonableMoves) - 1)
                        player2.activeMove = p2reasonableMoves[randNumb][0]
                        player2.mana-=1
                    else:
                        randNumb = random.randint(0, len(p1reasonableMoves) - 1)
                        player1.stackChoice = "n"
                        player1.activeMove = p1reasonableMoves[randNumb][1]

                        randNumb = random.randint(0, len(p2reasonableMoves) - 1)
                        player2.stackChoice = "n"
                        player2.activeMove = p2reasonableMoves[randNumb][1]
                        if player1.chosenClass == "Fireborne" and player1.stackChoice == "y":
                            player1.mana -= 1

                        elif player1.chosenClass == "Parrymaster" and player1.stackChoice == "y":
                            player1.mana -= 1

                        if player2.chosenClass == "Fireborne" and player2.stackChoice == "y":
                            player2.mana -= 1

                        elif player2.chosenClass == "Parrymaster" and player2.stackChoice == "y":
                            player2.mana -= 1


            elif player1.stackChoice == "y":
                    #print("Player 1 has conjured. They can see your move.")
                    #print(turn)
                    p2reasonableMoves = findReasonableMovestacks(player2,player1,player2InitialState,player2InitialState,turn, False, True)
                    if len(p2reasonableMoves) == 0:
                        print(turn)
                        print("Player 2:")
                        print(player2.mana)
                        print(player2.blocks)
                        print("Player 1:")
                        print(player1.mana)
                        print(player1.blocks)
                    randNumb = random.randint(0, len(p2reasonableMoves) - 1)
                    player2.activeMove = p2reasonableMoves[randNumb][1]
                    #print(f"Player 2 has elected to {player2.activeMove}")
                    #print(player2.activeMove)
                    p1reasonableMoves = findReasonableMovestacks(player1, player2, player1InitialState,player2InitialState,turn, True, True)
                    if len(p1reasonableMoves) == 0:
                        print(turn)
                        print("Player 1:")
                        print(player1.mana)
                        print(player1.blocks)
                        print("Player 2:")
                        print(player2.mana)
                        print(player2.blocks)
                    #print(p1reasonableMoves)
                    randNumb = random.randint(0, len(p1reasonableMoves) - 1)
                    #print(randNumb)
                    #print(p1reasonableMoves)
                    player1.activeMove = p1reasonableMoves[randNumb][1]
                    player1.mana -= 1
            else:
                randNumb = random.randint(0, len(p1reasonableMoves) - 1)
                player1.stackChoice = "n"
                player1.activeMove = p1reasonableMoves[randNumb][1]

                p2reasonableMoves = findReasonableMovestacks(player2, player1, player2InitialState, player1InitialState,
                                                             turn, False, False)
                randNumb = random.randint(0, len(p2reasonableMoves) - 1)
                player2.stackChoice = p2reasonableMoves[randNumb][0]
                player2.activeMove = p2reasonableMoves[randNumb][1]
                if player1.chosenClass == "Fireborne" and player1.stackChoice == "y":
                    player1.mana -= 1

                elif player1.chosenClass == "Parrymaster" and player1.stackChoice == "y":
                    player1.mana -= 1

                if player2.chosenClass == "Fireborne" and player2.stackChoice == "y":
                    player2.mana -= 1

                elif player2.chosenClass == "Parrymaster" and player2.stackChoice == "y":
                    player2.mana -= 1
        elif player2.chosenClass == "Conjurer" and player2.stacksLeft > 0 and player2.mana > 1:
                p2reasonableMoves = findReasonableMovestacks(player2, player1,player2InitialState,player1InitialState,turn, False, False)
                #print(p2reasonableMoves)
                #print(player2.mana)
                #print(player1.mana)
                #print(player1.blocks)
                randNumb = random.randint(0, len(p2reasonableMoves) - 1)
                player2.stackChoice = p2reasonableMoves[randNumb][0]
                #print(player2.stackChoice)
                if player2.stackChoice == "y":
                    #print(player2.mana)
                    #print("Player 2 has conjured. They can see your move.")
                    p1reasonableMoves = findReasonableMovestacks(player1,  player2, player1InitialState,player2InitialState,turn,False, True)
                    randNumb = random.randint(0, len(p1reasonableMoves) - 1)
                    player1.activeMove = p1reasonableMoves[randNumb][1]
                    #print(f"Player 1 has elected to {player1.activeMove}")
                    p2reasonableMoves = findReasonableMovestacks(player2, player1,player2InitialState,player1InitialState,turn, True, True)
                    randNumb = random.randint(0, len(p2reasonableMoves) - 1)
                    player2.activeMove = p2reasonableMoves[randNumb][1]
                    player2.mana-=1

                else:
                    randNumb = random.randint(0, len(p2reasonableMoves)-1)
                    player2.stackChoice = "n"
                    player2.activeMove = p2reasonableMoves[randNumb][1]


                    p1reasonableMoves = findReasonableMovestacks(player1, player2, player1InitialState,
                                                                 player2InitialState, turn, False, False)
                    randNumb = random.randint(0, len(p1reasonableMoves) - 1)
                    player1.stackChoice = p1reasonableMoves[randNumb][0]
                    player1.activeMove = p1reasonableMoves[randNumb][1]


                    if player1.chosenClass == "Fireborne" and player1.stackChoice == "y":
                        player1.mana -= 1

                    elif player1.chosenClass == "Parrymaster" and player1.stackChoice == "y":
                        player1.mana -= 1

                    if player2.chosenClass == "Fireborne" and player2.stackChoice == "y":
                        player2.mana -= 1

                    elif player2.chosenClass == "Parrymaster" and player2.stackChoice == "y":
                        player2.mana -= 1
        else:
            p1reasonableMoves = findReasonableMovestacks(player1,player2,player1InitialState,player2InitialState,turn,False,False)
            #print(p1reasonableMoves)
            #print(player1.mana)
            randNumb = random.randint(0,len(p1reasonableMoves)-1)
            player1.stackChoice = p1reasonableMoves[randNumb][0]
            player1.activeMove = p1reasonableMoves[randNumb][1]
         #   print(player1.stackChoice)
         #   print(player1.activeMove)
            p2reasonableMoves = findReasonableMovestacks(player2,player1,player2InitialState,player1InitialState,turn,False,False)
            if len(p2reasonableMoves)==0:
                print(player2.mana)
                print(player2.blocks)
                print(player1.mana)
                print(player1.blocks)
            #print(p2reasonableMoves)
            #print(player2.mana)
            randNumb = random.randint(0,len(p2reasonableMoves)-1)
            player2.stackChoice = p2reasonableMoves[randNumb][0]
            #if player2.chosenClass == "Conjurer" and player2.stackChoice == "y":
            player2.activeMove = p2reasonableMoves[randNumb][1]

            if player1.chosenClass == "Fireborne" and player1.stackChoice == "y":
                player1.mana -= 1

            elif player1.chosenClass == "Parrymaster" and player1.stackChoice == "y":
                player1.mana -= 1

            if player2.chosenClass == "Fireborne" and player2.stackChoice == "y":
                player2.mana -= 1

            elif player2.chosenClass == "Parrymaster" and player2.stackChoice == "y":
                player2.mana -= 1
             #   print(player2.stackChoice)
              #  print(player2.activeMove)


              #  print(f"Turn {turn}")
        #print("Before")
        #print(player2.stacksLeft)
        player1,player2,turn,game_over,winner = movestack_resolve(player1,player2,player1InitialState,player2InitialState,turn)
        #print("After")
        #print(player2.stacksLeft)
        #print(turn)
    game_over = False
 #   print("Game over!")
 #  print(f"{winner} is your winner!")
    return winner


def findReasonableMovestacks(player,oppPlayer,playerBaseState,oppPlayerBaseState,turn,abuserInformed,victimInformed):

    reasonableMoveStacks = [["n", "Attack"], ["n", "Block"], ["n", "Mana"], ["n", "Copy"], ["y", "Attack"], ["y", "Block"], ["y", "Mana"]]
    forcedWin = False

    #available stacks
    if player.stacksLeft == 0:
        if ["y", "Attack"] in reasonableMoveStacks:
            reasonableMoveStacks.remove(["y", "Attack"])
        if ["y", "Block"] in reasonableMoveStacks:
            reasonableMoveStacks.remove(["y", "Block"])
        if ["y", "Mana"] in reasonableMoveStacks:
            reasonableMoveStacks.remove(["y", "Mana"])

    elif player.chosenClass == "Conjurer":
        if player.mana == 0:
            if ["y", "Attack"] in reasonableMoveStacks:
                reasonableMoveStacks.remove(["y", "Attack"])
            if ["y", "Block"] in reasonableMoveStacks:
                reasonableMoveStacks.remove(["y", "Block"])
            if ["y", "Mana"] in reasonableMoveStacks:
                reasonableMoveStacks.remove(["y", "Mana"])

        elif player.mana <= player.attackCost:
            reasonableMoveStacks.remove(["y","Attack"])

    elif player.chosenClass == "Thief":
        if turn == 1:
            if ["y", "Attack"] in reasonableMoveStacks:
                reasonableMoveStacks.remove(["y", "Attack"])
            if ["y", "Block"] in reasonableMoveStacks:
                reasonableMoveStacks.remove(["y", "Block"])
            if ["y", "Mana"] in reasonableMoveStacks:
                reasonableMoveStacks.remove(["y", "Mana"])


    elif player.chosenClass == "Tax Collector":
        if player.mana == 0:
            if ["y", "Attack"] in reasonableMoveStacks:
                reasonableMoveStacks.remove(["y", "Attack"])
            if ["y", "Block"] in reasonableMoveStacks:
                reasonableMoveStacks.remove(["y", "Block"])
            if ["y", "Mana"] in reasonableMoveStacks:
                reasonableMoveStacks.remove(["y", "Mana"])

        elif player.mana < player.attackCost:
            if ["y", "Attack"] in reasonableMoveStacks:
                reasonableMoveStacks.remove(["y", "Attack"])

    elif player.chosenClass == "Fireborne":
        if player.mana == 0:
            if ["y", "Attack"] in reasonableMoveStacks:
                reasonableMoveStacks.remove(["y", "Attack"])
            if ["y", "Block"] in reasonableMoveStacks:
                reasonableMoveStacks.remove(["y", "Block"])
            if ["y", "Mana"] in reasonableMoveStacks:
                reasonableMoveStacks.remove(["y", "Mana"])

        elif player.mana <= player.attackCost:
            reasonableMoveStacks.remove(["y","Attack"])


    elif player.chosenClass == "Parrymaster":
        if player.mana == 0:
            if ["y", "Attack"] in reasonableMoveStacks:
                reasonableMoveStacks.remove(["y", "Attack"])
            if ["y", "Block"] in reasonableMoveStacks:
                reasonableMoveStacks.remove(["y", "Block"])
            if ["y", "Mana"] in reasonableMoveStacks:
                reasonableMoveStacks.remove(["y", "Mana"])

        elif player.mana <= player.attackCost:
            reasonableMoveStacks.remove(["y","Attack"])


    #available moves
    if player.mana < player.attackCost:
        if ["n", "Attack"] in reasonableMoveStacks:
            reasonableMoveStacks.remove(["n", "Attack"])
        if ["y","Attack"] in reasonableMoveStacks:
            reasonableMoveStacks.remove(["y","Attack"])

    if player.blocks < 1:
        if ["n", "Block"] in reasonableMoveStacks:
            reasonableMoveStacks.remove(["n", "Block"])
        if ["y","Block"] in reasonableMoveStacks:
            reasonableMoveStacks.remove(["y","Block"])
    if player.chosenClass != "Cupid":
        if ["n", "Copy"] in reasonableMoveStacks:
            reasonableMoveStacks.remove(["n", "Copy"])
    elif player.copiesLeft == 0:
        if ["n", "Copy"] in reasonableMoveStacks:
            reasonableMoveStacks.remove(["n", "Copy"])




    #conj exceptions
    if oppPlayer.chosenClass == "Conjurer" and abuserInformed == False and victimInformed == True:









      if player.mana > 6*oppPlayer.mana + oppPlayer.blocks:

        if ["n", "Block"] in reasonableMoveStacks:
            reasonableMoveStacks.remove(["n", "Block"])
        if ["n", "Mana"] in reasonableMoveStacks:
            reasonableMoveStacks.remove(["n", "Mana"])

        if ["n", "Copy"] in reasonableMoveStacks:
            reasonableMoveStacks.remove(["n", "Copy"])
        if ["y", "Attack"] in reasonableMoveStacks:
            reasonableMoveStacks.remove(["y", "Attack"])
        if ["y", "Block"] in reasonableMoveStacks:
            reasonableMoveStacks.remove(["y", "Block"])
        if ["y", "Mana"] in reasonableMoveStacks:
            reasonableMoveStacks.remove(["y", "Mana"])

      elif player.chosenClass == "Copywriter":
          if oppPlayer.mana == 0 and ((oppPlayer.blocks < 3 and player.mana >= player.attackCost) or (oppPlayer.blocks >= 3 and player.mana >= oppPlayer.blocks - 2)):
                  if ["n", "Block"] in reasonableMoveStacks:
                      reasonableMoveStacks.remove(["n", "Block"])
                  if ["n", "Mana"] in reasonableMoveStacks:
                      reasonableMoveStacks.remove(["n", "Mana"])
                  if ["n", "Copy"] in reasonableMoveStacks:
                      reasonableMoveStacks.remove(["n", "Copy"])
                  if ["y", "Attack"] in reasonableMoveStacks:
                      reasonableMoveStacks.remove(["y", "Attack"])
                  if ["y", "Block"] in reasonableMoveStacks:
                      reasonableMoveStacks.remove(["y", "Block"])
                  if ["y", "Mana"] in reasonableMoveStacks:
                      reasonableMoveStacks.remove(["y", "Mana"])
          else:
              if oppPlayer.mana - 1 >= oppPlayer.attackCost:
                  if ["n", "Copy"] in reasonableMoveStacks:
                      reasonableMoveStacks = [["n", "Copy"]]
                  else:
                      if ["n", "Mana"] in reasonableMoveStacks:
                          reasonableMoveStacks.remove(["n", "Mana"])
                      if ["y", "Mana"] in reasonableMoveStacks:
                          reasonableMoveStacks.remove(["y", "Mana"])

                  if player.mana >= oppPlayer.mana:
                      if ["n", "Block"] in reasonableMoveStacks:
                          reasonableMoveStacks.remove(["n", "Block"])
                      if ["y", "Block"] in reasonableMoveStacks:
                          reasonableMoveStacks.remove(["y", "Block"])

                  elif player.blocks > 0:
                      if ["n", "Attack"] in reasonableMoveStacks:
                          reasonableMoveStacks.remove(["n", "Attack"])
                      if ["y", "Attack"] in reasonableMoveStacks:
                          reasonableMoveStacks.remove(["y", "Attack"])

              else:
                  if ["n", "Block"] in reasonableMoveStacks:
                      reasonableMoveStacks.remove(["n", "Block"])
                  if ["y", "Block"] in reasonableMoveStacks:
                      reasonableMoveStacks.remove(["y", "Block"])
                  if ["n", "Attack"] in reasonableMoveStacks:
                      reasonableMoveStacks.remove(["n", "Attack"])
                  if ["y", "Attack"] in reasonableMoveStacks:
                      reasonableMoveStacks.remove(["y", "Attack"])
                  if ["n", "Copy"] in reasonableMoveStacks:
                      reasonableMoveStacks.remove(["n", "Copy"])

      elif player.chosenClass == "Conjurer":
          if player.mana >= player.attackCost and oppPlayer.mana-1 == 0 and player.mana+player.stacksLeft > oppPlayer.blocks:
                          if ["n", "Block"] in reasonableMoveStacks:
                              reasonableMoveStacks.remove(["n", "Block"])
                          if ["n", "Mana"] in reasonableMoveStacks:
                              reasonableMoveStacks.remove(["n", "Mana"])
                          if ["n", "Copy"] in reasonableMoveStacks:
                              reasonableMoveStacks.remove(["n", "Copy"])
                          if ["y", "Attack"] in reasonableMoveStacks:
                              reasonableMoveStacks.remove(["y", "Attack"])
                          if ["y", "Block"] in reasonableMoveStacks:
                              reasonableMoveStacks.remove(["y", "Block"])
                          if ["y", "Mana"] in reasonableMoveStacks:
                              reasonableMoveStacks.remove(["y", "Mana"])
          else:
              if oppPlayer.mana-1 >= oppPlayer.attackCost:
                  if ["n", "Copy"] in reasonableMoveStacks:
                      reasonableMoveStacks = [["n", "Copy"]]
                  else:
                      if ["n", "Mana"] in reasonableMoveStacks:
                          reasonableMoveStacks.remove(["n", "Mana"])
                      if ["y", "Mana"] in reasonableMoveStacks:
                          reasonableMoveStacks.remove(["y", "Mana"])

                  if player.mana >= oppPlayer.mana:
                      if ["n", "Block"] in reasonableMoveStacks:
                          reasonableMoveStacks.remove(["n", "Block"])
                      if ["y", "Block"] in reasonableMoveStacks:
                          reasonableMoveStacks.remove(["y", "Block"])

                  elif player.blocks > 0:
                      if ["n", "Attack"] in reasonableMoveStacks:
                          reasonableMoveStacks.remove(["n", "Attack"])
                      if ["y", "Attack"] in reasonableMoveStacks:
                          reasonableMoveStacks.remove(["y", "Attack"])

              else:
                  if ["n", "Block"] in reasonableMoveStacks:
                      reasonableMoveStacks.remove(["n", "Block"])
                  if ["y", "Block"] in reasonableMoveStacks:
                      reasonableMoveStacks.remove(["y", "Block"])
                  if ["n", "Attack"] in reasonableMoveStacks:
                      reasonableMoveStacks.remove(["n", "Attack"])
                  if ["y", "Attack"] in reasonableMoveStacks:
                      reasonableMoveStacks.remove(["y", "Attack"])
                  if ["n", "Copy"] in reasonableMoveStacks:
                      reasonableMoveStacks.remove(["n", "Copy"])

      else:
        if oppPlayer.mana-1 >= oppPlayer.attackCost:
            if ["n", "Copy"] in reasonableMoveStacks:
                reasonableMoveStacks = [["n", "Copy"]]
            elif player.blocks >0 or player.mana >= player.attackCost:
                if ["n", "Mana"] in reasonableMoveStacks:
                    reasonableMoveStacks.remove(["n", "Mana"])
                if ["y", "Mana"] in reasonableMoveStacks:
                    reasonableMoveStacks.remove(["y", "Mana"])

            if player.mana >= oppPlayer.mana and player.mana >= player.attackCost:
                if ["n", "Block"] in reasonableMoveStacks:
                    reasonableMoveStacks.remove(["n", "Block"])
                if ["y", "Block"] in reasonableMoveStacks:
                    reasonableMoveStacks.remove(["y", "Block"])

            elif player.blocks > 0:
                if ["n", "Attack"] in reasonableMoveStacks:
                    reasonableMoveStacks.remove(["n", "Attack"])
                if ["y", "Attack"] in reasonableMoveStacks:
                    reasonableMoveStacks.remove(["y", "Attack"])

        else:
            if ["n", "Block"] in reasonableMoveStacks:
                reasonableMoveStacks.remove(["n", "Block"])
            if ["y", "Block"] in reasonableMoveStacks:
                reasonableMoveStacks.remove(["y", "Block"])
            if ["n", "Attack"] in reasonableMoveStacks:
                reasonableMoveStacks.remove(["n", "Attack"])
            if ["y", "Attack"] in reasonableMoveStacks:
                reasonableMoveStacks.remove(["y", "Attack"])
            if ["n", "Copy"] in reasonableMoveStacks:
                reasonableMoveStacks.remove(["n", "Copy"])


    elif player.chosenClass == "Conjurer" and abuserInformed == True and victimInformed == True:
      """print("yellow")
      print(player.mana)
      print(player.blocks)
      print(oppPlayer.mana)"""
      if player.mana > 6 * oppPlayer.mana + oppPlayer.blocks:
            if oppPlayer.stacksLeft == 0 and oppPlayer.chosenClass != "Defender" and oppPlayer.chosenClass != "Stunner" and oppPlayer.chosenClass != "Copywriter" and oppPlayer.chosenClass != "The Sumo" and oppPlayer.chosenClass != "Fireborne" and oppPlayer.chosenClass != "Cupid":
                if oppPlayer.blocks == 0 and oppPlayer.mana < oppPlayer.attackCost and player.mana-1 >= player.attackCost:
                    reasonableMoveStacks = [["y", "Attack"]]
                else:
                    if oppPlayer.activeMove == "Attack" and player.blocks > 0:
                        reasonableMoveStacks = [["y", "Block"]]
                    elif oppPlayer.activeMove == "Block" or player.mana-1 < player.attackCost:
                        reasonableMoveStacks = [["y", "Mana"]]
                    elif oppPlayer.activeMove == "Mana":
                        reasonableMoveStacks = [["y", "Attack"]]
                    elif oppPlayer.activeMove == "Copy":
                        if player.mana > oppPlayer.mana and player.mana-1 >= player.attackCost:
                            reasonableMoveStacks = [["y", "Attack"]]
                        else:
                            reasonableMoveStacks = [["y", "Mana"]]







            elif oppPlayer.chosenClass == "Defender":
                if oppPlayer.blocks == 0 and oppPlayer.mana < oppPlayer.attackCost and player.mana-1 >= player.attackCost:
                    reasonableMoveStacks = [["y", "Attack"]]
                else:
                    if oppPlayer.activeMove == "Attack" and player.blocks > 0:
                        reasonableMoveStacks = [["y", "Block"]]
                    elif oppPlayer.activeMove == "Block" or player.mana-1 < player.attackCost:
                        reasonableMoveStacks = [["y", "Mana"]]
                    elif oppPlayer.activeMove == "Mana":
                        reasonableMoveStacks = [["y", "Attack"]]
                    elif oppPlayer.activeMove == "Copy":
                        if player.mana > oppPlayer.mana and player.mana-1 >= player.attackCost:
                            reasonableMoveStacks = [["y", "Attack"]]
                        else:
                            reasonableMoveStacks = [["y", "Mana"]]
            elif oppPlayer.chosenClass == "Stunner":
                if oppPlayer.blocks == 0 and oppPlayer.mana < oppPlayer.attackCost and player.mana-1 >= player.attackCost:
                    reasonableMoveStacks = [["y", "Attack"]]
                else:
                    if oppPlayer.activeMove == "Attack" and player.blocks > 0:
                        reasonableMoveStacks = [["y", "Block"]]
                    elif oppPlayer.activeMove == "Block" or player.mana-1 < player.attackCost:
                        reasonableMoveStacks = [["y", "Mana"]]
                    elif oppPlayer.activeMove == "Mana":
                        reasonableMoveStacks = [["y", "Attack"]]
                    elif oppPlayer.activeMove == "Copy":
                        if player.mana > oppPlayer.mana and player.mana-1 >= player.attackCost:
                            reasonableMoveStacks = [["y", "Attack"]]
                        else:
                            reasonableMoveStacks = [["y", "Mana"]]
                """elif player.chosenClass == "Thief":
                elif player.chosenClass == "Stunner":
                elif player.chosenClass == "Tax Collector":
                elif player.chosenClass == "Copywriter":
                elif player.chosenClass == "Conjurer":
                elif player.chosenClass == "The Sumo":"""
            elif oppPlayer.chosenClass == "Copywriter":
                if player.mana-1>=player.attackCost and not (oppPlayer.mana > 0 or (oppPlayer.blocks > 2) or (
                        oppPlayer.blocks == 2 and oppPlayer.oppLastMove == "Attack") or (
                                oppPlayer.blocks == 1 and oppPlayer.copyStreak == 2 and oppPlayer.oppLastMove == "Attack")):
                    reasonableMoveStacks = [["y", "Attack"]]
                else:
                    if oppPlayer.activeMove == "Attack" and player.blocks > 0:
                        reasonableMoveStacks = [["y", "Block"]]
                    elif oppPlayer.activeMove == "Block" or player.mana-1 < player.attackCost:
                        reasonableMoveStacks = [["y", "Mana"]]
                    elif oppPlayer.activeMove == "Mana":
                        reasonableMoveStacks = [["y", "Attack"]]
                    elif oppPlayer.activeMove == "Copy":
                        if player.mana > oppPlayer.mana and player.mana-1 >= player.attackCost:
                            reasonableMoveStacks = [["y", "Attack"]]
                        else:
                            reasonableMoveStacks = [["y", "Mana"]]

                """elif player.chosenClass == "Thief":
                elif player.chosenClass == "Stunner":
                elif player.chosenClass == "Tax Collector":
                elif player.chosenClass == "Copywriter":
                elif player.chosenClass == "Conjurer":
                elif player.chosenClass == "The Sumo":
                    if oppPlayer.blocks == 0 and oppPlayer.mana < oppPlayer.attackCost:
                        if ["n", "Block"] in reasonableMoveStacks:
                            reasonableMoveStacks.remove(["n", "Block"])
                        if ["n", "Mana"] in reasonableMoveStacks:
                            reasonableMoveStacks.remove(["n", "Mana"])
                        if ["n", "Copy"] in reasonableMoveStacks:
                            reasonableMoveStacks.remove(["n", "Copy"])
                        if ["y", "Attack"] in reasonableMoveStacks:
                            reasonableMoveStacks.remove(["y", "Attack"])
                        if ["y", "Block"] in reasonableMoveStacks:
                            reasonableMoveStacks.remove(["y", "Block"])
                        if ["y", "Mana"] in reasonableMoveStacks:
                            reasonableMoveStacks.remove(["y", "Mana"])"""
            elif oppPlayer.chosenClass == "The Sumo":
                if oppPlayer.mana < oppPlayer.attackCost and player.mana-1 >= player.attackCost:
                    reasonableMoveStacks = [["y", "Attack"]]
                else:
                    if oppPlayer.activeMove == "Attack" and player.blocks > 0:
                        reasonableMoveStacks = [["y", "Block"]]
                    elif oppPlayer.activeMove == "Block" or player.mana-1 < player.attackCost:
                        reasonableMoveStacks = [["y", "Mana"]]
                    elif oppPlayer.activeMove == "Mana":
                        reasonableMoveStacks = [["y", "Attack"]]
                    elif oppPlayer.activeMove == "Copy":
                        if player.mana > oppPlayer.mana and player.mana-1 >= player.attackCost:
                            reasonableMoveStacks = [["y", "Attack"]]
                        else:
                            reasonableMoveStacks = [["y", "Mana"]]

                """elif player.chosenClass == "Thief":
                elif player.chosenClass == "Stunner":
                elif player.chosenClass == "Tax Collector":
                elif player.chosenClass == "Copywriter":
                elif player.chosenClass == "Conjurer":
                elif player.chosenClass == "The Sumo":
                    if oppPlayer.blocks == 0 and oppPlayer.mana < oppPlayer.attackCost:
                        if ["n", "Block"] in reasonableMoveStacks:
                            reasonableMoveStacks.remove(["n", "Block"])
                        if ["n", "Mana"] in reasonableMoveStacks:
                            reasonableMoveStacks.remove(["n", "Mana"])
                        if ["n", "Copy"] in reasonableMoveStacks:
                            reasonableMoveStacks.remove(["n", "Copy"])
                        if ["y", "Attack"] in reasonableMoveStacks:
                            reasonableMoveStacks.remove(["y", "Attack"])
                        if ["y", "Block"] in reasonableMoveStacks:
                            reasonableMoveStacks.remove(["y", "Block"])
                        if ["y", "Mana"] in reasonableMoveStacks:
                            reasonableMoveStacks.remove(["y", "Mana"])"""
            elif oppPlayer.chosenClass == "Fireborne" and oppPlayer.stacksLeft == 0:
                if oppPlayer.stacksLeft == 0 and (
                        oppPlayer.extraLifetimeRemaining == 0 or player.mana+1 > 6 * oppPlayer.mana + 1 + oppPlayer.blocks + 4):
                        reasonableMoveStacks = [["y", "Attack"]]
                else:
                    if oppPlayer.activeMove == "Attack" and player.blocks > 0:
                        reasonableMoveStacks = [["y", "Block"]]
                    elif oppPlayer.activeMove == "Block" or player.mana-1 < player.attackCost:
                        reasonableMoveStacks = [["y", "Mana"]]
                    elif oppPlayer.activeMove == "Mana":
                        reasonableMoveStacks = [["y", "Attack"]]
                    elif oppPlayer.activeMove == "Copy":
                        if player.mana > oppPlayer.mana and player.mana-1 >= player.attackCost:
                            reasonableMoveStacks = [["y", "Attack"]]
                        else:
                            reasonableMoveStacks = [["y", "Mana"]]

                """elif player.chosenClass == "Thief":
                elif player.chosenClass == "Stunner":
                elif player.chosenClass == "Tax Collector":
                elif player.chosenClass == "Copywriter":
                elif player.chosenClass == "Conjurer":
                elif player.chosenClass == "The Sumo":"""
            elif oppPlayer.chosenClass == "Cupid":
                if oppPlayer.copiesLeft == 0:
                    if player.mana+1 > 6 * oppPlayer.mana + oppPlayer.blocks and player.mana-1>=player.attackCost:
                        reasonableMoveStacks = [["y", "Attack"]]
                    else:
                        if oppPlayer.activeMove == "Attack" and player.blocks > 0:
                            reasonableMoveStacks = [["y", "Block"]]
                        elif oppPlayer.activeMove == "Block" or player.mana-1 < player.attackCost:
                            reasonableMoveStacks = [["y", "Mana"]]
                        elif oppPlayer.activeMove == "Mana":
                            reasonableMoveStacks = [["y", "Attack"]]
                        elif oppPlayer.activeMove == "Copy":
                            if player.mana > oppPlayer.mana and player.mana-1 >= player.attackCost:
                                reasonableMoveStacks = [["y", "Attack"]]
                            else:
                                reasonableMoveStacks = [["y", "Mana"]]


                elif player.mana+1 > 6 * oppPlayer.mana + oppPlayer.blocks + 6 and player.mana-1>=player.attackCost:
                    reasonableMoveStacks = [["y", "Attack"]]

                else:
                    if oppPlayer.activeMove == "Attack" and player.blocks > 0:
                        reasonableMoveStacks = [["y", "Block"]]
                    elif oppPlayer.activeMove == "Block" or player.mana-1 < player.attackCost:
                        reasonableMoveStacks = [["y", "Mana"]]
                    elif oppPlayer.activeMove == "Mana":
                        reasonableMoveStacks = [["y", "Attack"]]
                    elif oppPlayer.activeMove == "Copy":
                        if player.mana > oppPlayer.mana and player.mana-1 >= player.attackCost:
                            reasonableMoveStacks = [["y", "Attack"]]
                        else:
                            reasonableMoveStacks = [["y", "Mana"]]



            elif oppPlayer.stacksLeft > 0:
                if oppPlayer.chosenClass != "Thief" and oppPlayer.chosenClass != "Tax Collector" and oppPlayer.chosenClass != "Fireborne" and oppPlayer.chosenClass != "Null" and player.mana-1>=player.attackCost:
                    reasonableMoveStacks = [["y", "Attack"]]
                else:
                    if oppPlayer.activeMove == "Attack" and player.blocks > 0:
                        reasonableMoveStacks = [["y", "Block"]]
                    elif oppPlayer.activeMove == "Block" or player.mana-1 < player.attackCost:
                        reasonableMoveStacks = [["y", "Mana"]]
                    elif oppPlayer.activeMove == "Mana":
                        reasonableMoveStacks = [["y", "Attack"]]
                    elif oppPlayer.activeMove == "Copy":
                        if player.mana > oppPlayer.mana and player.mana-1 >= player.attackCost:
                            reasonableMoveStacks = [["y", "Attack"]]
                        else:
                            reasonableMoveStacks = [["y", "Mana"]]
            else:
                if oppPlayer.activeMove == "Attack" and player.blocks > 0:
                    reasonableMoveStacks = [["y", "Block"]]
                elif oppPlayer.activeMove == "Block" or player.mana-1 < player.attackCost:
                    reasonableMoveStacks = [["y", "Mana"]]
                elif oppPlayer.activeMove == "Mana":
                    reasonableMoveStacks = [["y", "Attack"]]
                elif oppPlayer.activeMove == "Copy":
                    if player.mana > oppPlayer.mana and player.mana-1 >= player.attackCost:
                        reasonableMoveStacks = [["y", "Attack"]]
                    else:
                        reasonableMoveStacks = [["y", "Mana"]]


      elif oppPlayer.chosenClass == "Retired" and oppPlayer.mana == 0:
          if oppPlayer.activeMove == "Block" or player.mana-1 < player.attackCost:
              reasonableMoveStacks = [["y", "Mana"]]
          else:
              reasonableMoveStacks = [["y", "Attack"]]


      elif player.mana-1 >= player.attackCost and oppPlayer.mana == 0:
          if player.mana + player.stacksLeft > oppPlayer.blocks:
              if oppPlayer.stacksLeft == 0 and oppPlayer.chosenClass != "Defender" and oppPlayer.chosenClass != "Stunner" and oppPlayer.chosenClass != "Copywriter" and oppPlayer.chosenClass != "Fireborne" and oppPlayer.chosenClass != "Cupid":

                      #active move of opponent? block or mana?
                      if oppPlayer.activeMove == "Block" or player.mana-1 < player.attackCost:
                          reasonableMoveStacks = [["y", "Mana"]]
                      else:
                          reasonableMoveStacks = [["y", "Attack"]]


              elif oppPlayer.chosenClass == "Cupid":
                  if oppPlayer.copiesLeft == 0:
                          if oppPlayer.activeMove == "Block" or player.mana-1 < player.attackCost:
                              #print(reasonableMoveStacks)
                              reasonableMoveStacks = [["y", "Mana"]]
                              #print(reasonableMoveStacks)
                          else:
                              reasonableMoveStacks = [["y", "Attack"]]
                  else:
                      if oppPlayer.activeMove == "Attack" and player.blocks > 0:
                          reasonableMoveStacks = [["y", "Block"]]
                      elif oppPlayer.activeMove == "Block" or player.mana-1 < player.attackCost:
                          reasonableMoveStacks = [["y", "Mana"]]
                      elif oppPlayer.activeMove == "Mana":
                          reasonableMoveStacks = [["y", "Attack"]]
                      elif oppPlayer.activeMove == "Copy":
                          if player.mana > oppPlayer.mana and player.mana-1 >= player.attackCost:
                              reasonableMoveStacks = [["y", "Attack"]]
                          else:
                              reasonableMoveStacks = [["y", "Mana"]]
              else:
                  if oppPlayer.activeMove == "Attack" and player.blocks > 0:
                      reasonableMoveStacks = [["y", "Block"]]
                  elif oppPlayer.activeMove == "Block" or player.mana-1 < player.attackCost:
                      reasonableMoveStacks = [["y", "Mana"]]
                  elif oppPlayer.activeMove == "Mana":
                      reasonableMoveStacks = [["y", "Attack"]]
                  elif oppPlayer.activeMove == "Copy":
                      if player.mana > oppPlayer.mana and player.mana-1 >= player.attackCost:
                          reasonableMoveStacks = [["y", "Attack"]]
                      else:
                          reasonableMoveStacks = [["y", "Mana"]]
          else:
              if oppPlayer.activeMove == "Attack" and player.blocks > 0:
                  reasonableMoveStacks = [["y", "Block"]]
              elif oppPlayer.activeMove == "Block" or player.mana-1 < player.attackCost:
                  reasonableMoveStacks = [["y", "Mana"]]
              elif oppPlayer.activeMove == "Mana":
                  reasonableMoveStacks = [["y", "Attack"]]
              elif oppPlayer.activeMove == "Copy":
                  if player.mana > oppPlayer.mana and player.mana-1 >= player.attackCost:
                      reasonableMoveStacks = [["y", "Attack"]]
                  else:
                      reasonableMoveStacks = [["y", "Mana"]]



      else:
        if oppPlayer.activeMove == "Attack" and player.blocks > 0:
            reasonableMoveStacks = [["y", "Block"]]
        elif oppPlayer.activeMove == "Block" or player.mana-1 < player.attackCost:
            reasonableMoveStacks = [["y", "Mana"]]
        elif oppPlayer.activeMove == "Mana":
            reasonableMoveStacks = [["y", "Attack"]]
        elif oppPlayer.activeMove == "Copy":
            if player.mana > oppPlayer.mana and player.mana-1 >= player.attackCost:
                reasonableMoveStacks = [["y","Attack"]]
            else:
                reasonableMoveStacks = [["y","Mana"]]

    else:






            #forced wins
        if player.chosenClass == "Joe" and oppPlayer.chosenClass == "Joe":
            if player.mana > 6*oppPlayer.mana + oppPlayer.blocks:
                #forced win
                forcedWin = True
                if ["n", "Block"] in reasonableMoveStacks:
                    reasonableMoveStacks.remove(["n", "Block"])
                if ["n", "Mana"] in reasonableMoveStacks:
                    reasonableMoveStacks.remove(["n", "Mana"])

            elif player.mana >0 and player.blocks == 0 and oppPlayer.mana >0 and oppPlayer.blocks == 0:
                if ["n", "Block"] in reasonableMoveStacks:
                    reasonableMoveStacks.remove(["n", "Block"])
                if ["n", "Mana"] in reasonableMoveStacks:
                    reasonableMoveStacks.remove(["n", "Mana"])

            elif player.mana > 0 and oppPlayer.mana > 0 and oppPlayer.blocks == 0:
                if ["n", "Mana"] in reasonableMoveStacks:
                    reasonableMoveStacks.remove(["n", "Mana"])

            elif player.mana > 0 and oppPlayer.mana == 0:
                if ["n", "Block"] in reasonableMoveStacks:
                    reasonableMoveStacks.remove(["n", "Block"])


        elif player.mana > 6*oppPlayer.mana + oppPlayer.blocks:
            if oppPlayer.stacksLeft == 0 and oppPlayer.chosenClass != "Defender" and oppPlayer.chosenClass != "Stunner" and oppPlayer.chosenClass != "Copywriter" and oppPlayer.chosenClass != "The Sumo" and oppPlayer.chosenClass != "Fireborne" and oppPlayer.chosenClass != "Cupid":
                forcedWin = True

                if ["n", "Block"] in reasonableMoveStacks:
                    reasonableMoveStacks.remove(["n", "Block"])
                if ["n", "Mana"] in reasonableMoveStacks:
                    reasonableMoveStacks.remove(["n", "Mana"])

                if ["n", "Copy"] in reasonableMoveStacks:
                    reasonableMoveStacks.remove(["n","Copy"])
                if ["y", "Attack"] in reasonableMoveStacks:
                    reasonableMoveStacks.remove(["y","Attack"])
                if ["y", "Block"] in reasonableMoveStacks:
                    reasonableMoveStacks.remove(["y","Block"])
                if ["y", "Mana"] in reasonableMoveStacks:
                    reasonableMoveStacks.remove(["y","Mana"])







            elif oppPlayer.chosenClass == "Defender":
                if oppPlayer.blocks == 0 and oppPlayer.mana < oppPlayer.attackCost:
                    forcedWin = True

                    if ["n", "Block"] in reasonableMoveStacks:
                        reasonableMoveStacks.remove(["n", "Block"])
                    if ["n", "Mana"] in reasonableMoveStacks:
                        reasonableMoveStacks.remove(["n", "Mana"])
                    if ["n", "Copy"] in reasonableMoveStacks:
                        reasonableMoveStacks.remove(["n", "Copy"])
                    if ["y", "Attack"] in reasonableMoveStacks:
                        reasonableMoveStacks.remove(["y", "Attack"])
                    if ["y", "Block"] in reasonableMoveStacks:
                        reasonableMoveStacks.remove(["y", "Block"])
                    if ["y", "Mana"] in reasonableMoveStacks:
                        reasonableMoveStacks.remove(["y", "Mana"])
            elif oppPlayer.chosenClass == "Stunner":
                if oppPlayer.blocks == 0 and oppPlayer.mana < oppPlayer.attackCost and player.mana >= player.attackCost:
                    forcedWin = True
                    if ["n", "Block"] in reasonableMoveStacks:
                        reasonableMoveStacks.remove(["n", "Block"])
                    if ["n", "Mana"] in reasonableMoveStacks:
                        reasonableMoveStacks.remove(["n", "Mana"])
                    if ["n", "Copy"] in reasonableMoveStacks:
                        reasonableMoveStacks.remove(["n", "Copy"])
                    if ["y", "Attack"] in reasonableMoveStacks:
                        reasonableMoveStacks.remove(["y", "Attack"])
                    if ["y", "Block"] in reasonableMoveStacks:
                        reasonableMoveStacks.remove(["y", "Block"])
                    if ["y", "Mana"] in reasonableMoveStacks:
                        reasonableMoveStacks.remove(["y", "Mana"])
                elif oppPlayer.mana == 0 and oppPlayer.attackStreak == 0:
                    if ["n", "Block"] in reasonableMoveStacks:
                        reasonableMoveStacks.remove(["n", "Block"])
                    if ["n", "Mana"] in reasonableMoveStacks:
                        reasonableMoveStacks.remove(["n", "Mana"])
                    if ["n", "Copy"] in reasonableMoveStacks:
                        reasonableMoveStacks.remove(["n", "Copy"])
                    if ["y", "Attack"] in reasonableMoveStacks:
                        reasonableMoveStacks.remove(["y", "Attack"])
                    if ["y", "Block"] in reasonableMoveStacks:
                        reasonableMoveStacks.remove(["y", "Block"])
                    if ["y", "Mana"] in reasonableMoveStacks:
                        reasonableMoveStacks.remove(["y", "Mana"])
                """elif player.chosenClass == "Thief":
                elif player.chosenClass == "Stunner":
                elif player.chosenClass == "Tax Collector":
                elif player.chosenClass == "Copywriter":
                elif player.chosenClass == "Conjurer":
                elif player.chosenClass == "The Sumo":"""
            elif oppPlayer.chosenClass == "Copywriter":
                if not (oppPlayer.mana > 0 or (oppPlayer.blocks > 2) or (oppPlayer.blocks == 2 and oppPlayer.oppLastMove == "Attack") or (oppPlayer.blocks == 1 and oppPlayer.copyStreak == 2 and oppPlayer.oppLastMove == "Attack")):
                    forcedWin = True
                    if ["n", "Block"] in reasonableMoveStacks:
                        reasonableMoveStacks.remove(["n", "Block"])
                    if ["n", "Mana"] in reasonableMoveStacks:
                        reasonableMoveStacks.remove(["n", "Mana"])
                    if ["n", "Copy"] in reasonableMoveStacks:
                        reasonableMoveStacks.remove(["n", "Copy"])
                    if ["y", "Attack"] in reasonableMoveStacks:
                        reasonableMoveStacks.remove(["y", "Attack"])
                    if ["y", "Block"] in reasonableMoveStacks:
                        reasonableMoveStacks.remove(["y", "Block"])
                    if ["y", "Mana"] in reasonableMoveStacks:
                        reasonableMoveStacks.remove(["y", "Mana"])
                """elif player.chosenClass == "Thief":
                elif player.chosenClass == "Stunner":
                elif player.chosenClass == "Tax Collector":
                elif player.chosenClass == "Copywriter":
                elif player.chosenClass == "Conjurer":
                elif player.chosenClass == "The Sumo":
                    if oppPlayer.blocks == 0 and oppPlayer.mana < oppPlayer.attackCost:
                        if ["n", "Block"] in reasonableMoveStacks:
                            reasonableMoveStacks.remove(["n", "Block"])
                        if ["n", "Mana"] in reasonableMoveStacks:
                            reasonableMoveStacks.remove(["n", "Mana"])
                        if ["n", "Copy"] in reasonableMoveStacks:
                            reasonableMoveStacks.remove(["n", "Copy"])
                        if ["y", "Attack"] in reasonableMoveStacks:
                            reasonableMoveStacks.remove(["y", "Attack"])
                        if ["y", "Block"] in reasonableMoveStacks:
                            reasonableMoveStacks.remove(["y", "Block"])
                        if ["y", "Mana"] in reasonableMoveStacks:
                            reasonableMoveStacks.remove(["y", "Mana"])"""
            elif oppPlayer.chosenClass == "The Sumo":
                if oppPlayer.mana < oppPlayer.attackCost:
                    forcedWin = True
                    if ["n", "Block"] in reasonableMoveStacks:
                        reasonableMoveStacks.remove(["n", "Block"])
                    if ["n", "Mana"] in reasonableMoveStacks:
                        reasonableMoveStacks.remove(["n", "Mana"])
                    if ["n", "Copy"] in reasonableMoveStacks:
                        reasonableMoveStacks.remove(["n", "Copy"])
                    if ["y", "Attack"] in reasonableMoveStacks:
                        reasonableMoveStacks.remove(["y", "Attack"])
                    if ["y", "Block"] in reasonableMoveStacks:
                        reasonableMoveStacks.remove(["y", "Block"])
                    if ["y", "Mana"] in reasonableMoveStacks:
                        reasonableMoveStacks.remove(["y", "Mana"])
                """elif player.chosenClass == "Thief":
                elif player.chosenClass == "Stunner":
                elif player.chosenClass == "Tax Collector":
                elif player.chosenClass == "Copywriter":
                elif player.chosenClass == "Conjurer":
                elif player.chosenClass == "The Sumo":
                    if oppPlayer.blocks == 0 and oppPlayer.mana < oppPlayer.attackCost:
                        if ["n", "Block"] in reasonableMoveStacks:
                            reasonableMoveStacks.remove(["n", "Block"])
                        if ["n", "Mana"] in reasonableMoveStacks:
                            reasonableMoveStacks.remove(["n", "Mana"])
                        if ["n", "Copy"] in reasonableMoveStacks:
                            reasonableMoveStacks.remove(["n", "Copy"])
                        if ["y", "Attack"] in reasonableMoveStacks:
                            reasonableMoveStacks.remove(["y", "Attack"])
                        if ["y", "Block"] in reasonableMoveStacks:
                            reasonableMoveStacks.remove(["y", "Block"])
                        if ["y", "Mana"] in reasonableMoveStacks:
                            reasonableMoveStacks.remove(["y", "Mana"])"""
            elif oppPlayer.chosenClass == "Fireborne" and oppPlayer.stacksLeft == 0:
                if oppPlayer.stacksLeft == 0 and (oppPlayer.extraLifetimeRemaining == 0 or player.mana > 6*oppPlayer.mana+1 +oppPlayer.blocks + 4):
                    forcedWin = True
                    if ["n", "Block"] in reasonableMoveStacks:
                        reasonableMoveStacks.remove(["n", "Block"])
                    if ["n", "Mana"] in reasonableMoveStacks:
                        reasonableMoveStacks.remove(["n", "Mana"])
                    if ["n", "Copy"] in reasonableMoveStacks:
                        reasonableMoveStacks.remove(["n", "Copy"])
                    if ["y", "Attack"] in reasonableMoveStacks:
                        reasonableMoveStacks.remove(["y", "Attack"])
                    if ["y", "Block"] in reasonableMoveStacks:
                        reasonableMoveStacks.remove(["y", "Block"])
                    if ["y", "Mana"] in reasonableMoveStacks:
                        reasonableMoveStacks.remove(["y", "Mana"])
                """elif player.chosenClass == "Thief":
                elif player.chosenClass == "Stunner":
                elif player.chosenClass == "Tax Collector":
                elif player.chosenClass == "Copywriter":
                elif player.chosenClass == "Conjurer":
                elif player.chosenClass == "The Sumo":"""
            elif oppPlayer.chosenClass == "Cupid":

                if oppPlayer.copiesLeft == 0:
                    forcedWin = True
                    if ["n", "Block"] in reasonableMoveStacks:
                        reasonableMoveStacks.remove(["n", "Block"])
                    if ["n", "Mana"] in reasonableMoveStacks:
                        reasonableMoveStacks.remove(["n", "Mana"])
                    if ["n", "Copy"] in reasonableMoveStacks:
                        reasonableMoveStacks.remove(["n", "Copy"])
                    if ["y", "Attack"] in reasonableMoveStacks:
                        reasonableMoveStacks.remove(["y", "Attack"])
                    if ["y", "Block"] in reasonableMoveStacks:
                        reasonableMoveStacks.remove(["y", "Block"])
                    if ["y", "Mana"] in reasonableMoveStacks:
                        reasonableMoveStacks.remove(["y", "Mana"])

                elif player.mana > 6 * oppPlayer.mana + oppPlayer.blocks + 6:
                    forcedWin = True
                    if ["n", "Block"] in reasonableMoveStacks:
                        reasonableMoveStacks.remove(["n", "Block"])
                    if ["n", "Mana"] in reasonableMoveStacks:
                        reasonableMoveStacks.remove(["n", "Mana"])

                    if ["n", "Copy"] in reasonableMoveStacks:
                        reasonableMoveStacks.remove(["n", "Copy"])
                    if ["y", "Attack"] in reasonableMoveStacks:
                        reasonableMoveStacks.remove(["y", "Attack"])
                    if ["y", "Block"] in reasonableMoveStacks:
                        reasonableMoveStacks.remove(["y", "Block"])
                    if ["y", "Mana"] in reasonableMoveStacks:
                        reasonableMoveStacks.remove(["y", "Mana"])


            elif oppPlayer.stacksLeft > 0:
                if oppPlayer.chosenClass != "Thief" and oppPlayer.chosenClass != "Tax Collector" and oppPlayer.chosenClass != "Fireborne" and oppPlayer.chosenClass != "Null":
                        #print(player.mana)
                        #print(oppPlayer.mana)
                        forcedWin = True
                        if ["n", "Block"] in reasonableMoveStacks:
                            reasonableMoveStacks.remove(["n", "Block"])
                        if ["n", "Mana"] in reasonableMoveStacks:
                            reasonableMoveStacks.remove(["n", "Mana"])
                        if ["n", "Copy"] in reasonableMoveStacks:
                            reasonableMoveStacks.remove(["n", "Copy"])
                        if ["y", "Attack"] in reasonableMoveStacks:
                            reasonableMoveStacks.remove(["y", "Attack"])
                        if ["y", "Block"] in reasonableMoveStacks:
                            reasonableMoveStacks.remove(["y", "Block"])
                        if ["y", "Mana"] in reasonableMoveStacks:
                            reasonableMoveStacks.remove(["y", "Mana"])


                """elif oppPlayer.chosenClass == "Thief":
                    if (oppPlayer.mana == 0 and oppPlayer.blocks == 0) or (player.mana-1 > 6*(oppPlayer.mana+1)+oppPlayer.blocks):
                        if ["n", "Block"] in reasonableMoveStacks:
                            reasonableMoveStacks.remove(["n", "Block"])
                        if ["n", "Mana"] in reasonableMoveStacks:
                            reasonableMoveStacks.remove(["n", "Mana"])
                        if ["n", "Copy"] in reasonableMoveStacks:
                            reasonableMoveStacks.remove(["n", "Copy"])
                        if ["y", "Attack"] in reasonableMoveStacks:
                            reasonableMoveStacks.remove(["y", "Attack"])
                        if ["y", "Block"] in reasonableMoveStacks:
                            reasonableMoveStacks.remove(["y", "Block"])
                        if ["y", "Mana"] in reasonableMoveStacks:
                            reasonableMoveStacks.remove(["y", "Mana"])
                    elif player.chosenClass == "Thief":
                    elif player.chosenClass == "Stunner":
                    elif player.chosenClass == "Tax Collector":
                    elif player.chosenClass == "Copywriter":
                    elif player.chosenClass == "Conjurer":
                    elif player.chosenClass == "The Sumo":
                elif oppPlayer.chosenClass == "Tax Collector":
                    if (oppPlayer.mana == 0) or (oppPlayer.mana>=oppPlayer.attackCost):
                        if ["n", "Block"] in reasonableMoveStacks:
                            reasonableMoveStacks.remove(["n", "Block"])
                        if ["n", "Mana"] in reasonableMoveStacks:
                            reasonableMoveStacks.remove(["n", "Mana"])
                        if ["n", "Copy"] in reasonableMoveStacks:
                            reasonableMoveStacks.remove(["n", "Copy"])
                        if ["y", "Attack"] in reasonableMoveStacks:
                            reasonableMoveStacks.remove(["y", "Attack"])
                        if ["y", "Block"] in reasonableMoveStacks:
                            reasonableMoveStacks.remove(["y", "Block"])
                        if ["y", "Mana"] in reasonableMoveStacks:
                            reasonableMoveStacks.remove(["y", "Mana"])
                    elif player.chosenClass == "Thief":
                    elif player.chosenClass == "Stunner":
                    elif player.chosenClass == "Tax Collector":
                    elif player.chosenClass == "Copywriter":
                    elif player.chosenClass == "Conjurer":
                    elif player.chosenClass == "The Sumo":"""


        elif oppPlayer.chosenClass == "Retired" and oppPlayer.mana == 0:
            forcedWin = True
            if ["n", "Attack"] in reasonableMoveStacks:
                reasonableMoveStacks.remove(["n", "Attack"])
            if ["n", "Block"] in reasonableMoveStacks:
                reasonableMoveStacks.remove(["n", "Block"])
            if ["n", "Copy"] in reasonableMoveStacks:
                reasonableMoveStacks.remove(["n", "Copy"])
            if ["y", "Attack"] in reasonableMoveStacks:
                reasonableMoveStacks.remove(["y", "Attack"])
            if ["y", "Block"] in reasonableMoveStacks:
                reasonableMoveStacks.remove(["y", "Block"])
            if ["y", "Mana"] in reasonableMoveStacks:
                reasonableMoveStacks.remove(["y", "Mana"])


        elif player.chosenClass == "Copywriter":
            if (oppPlayer.mana == 0 and oppPlayer.blocks < 3 and player.mana >= player.attackCost) or (oppPlayer.mana == 0 and oppPlayer.blocks >= 3 and player.mana >= oppPlayer.blocks - 2):
               if oppPlayer.stacksLeft == 0 and oppPlayer.chosenClass != "Defender" and oppPlayer.chosenClass != "Stunner" and oppPlayer.chosenClass != "Copywriter" and oppPlayer.chosenClass != "Fireborne" and oppPlayer.chosenClass != "Cupid":
                    forcedWin = True
                    if ["n", "Block"] in reasonableMoveStacks:
                        reasonableMoveStacks.remove(["n", "Block"])
                    if ["n", "Mana"] in reasonableMoveStacks:
                        reasonableMoveStacks.remove(["n", "Mana"])
                    if ["n", "Copy"] in reasonableMoveStacks:
                        reasonableMoveStacks.remove(["n", "Copy"])
                    if ["y", "Attack"] in reasonableMoveStacks:
                        reasonableMoveStacks.remove(["y", "Attack"])
                    if ["y", "Block"] in reasonableMoveStacks:
                        reasonableMoveStacks.remove(["y", "Block"])
                    if ["y", "Mana"] in reasonableMoveStacks:
                        reasonableMoveStacks.remove(["y", "Mana"])
               if oppPlayer.chosenClass == "Cupid":
                    if oppPlayer.copiesLeft == 0:
                            forcedWin = True

                            if ["n", "Block"] in reasonableMoveStacks:
                                reasonableMoveStacks.remove(["n", "Block"])
                            if ["n", "Mana"] in reasonableMoveStacks:
                                reasonableMoveStacks.remove(["n", "Mana"])
                            if ["n", "Copy"] in reasonableMoveStacks:
                                reasonableMoveStacks.remove(["n", "Copy"])
                            if ["y", "Attack"] in reasonableMoveStacks:
                                reasonableMoveStacks.remove(["y", "Attack"])
                            if ["y", "Block"] in reasonableMoveStacks:
                                reasonableMoveStacks.remove(["y", "Block"])
                            if ["y", "Mana"] in reasonableMoveStacks:
                                reasonableMoveStacks.remove(["y", "Mana"])



        elif player.chosenClass == "Conjurer":
            if (player.stackChoice != "i" and player.mana-1 >= player.attackCost and oppPlayer.mana == 0) or (player.mana-(1+player.attackCost) >= player.attackCost and oppPlayer.mana == 0):
                if player.mana + player.stacksLeft > oppPlayer.blocks:

                  if oppPlayer.stacksLeft == 0 and oppPlayer.chosenClass != "Defender" and oppPlayer.chosenClass != "Stunner" and oppPlayer.chosenClass != "Copywriter" and oppPlayer.chosenClass != "Fireborne" and oppPlayer.chosenClass != "Cupid":
                    forcedWin = True
                    if player.stacksLeft > 0 and player.stackChoice != "i":
                        if ["n", "Attack"] in reasonableMoveStacks:
                            reasonableMoveStacks.remove(["n","Attack"])
                        if ["n", "Block"] in reasonableMoveStacks:
                            reasonableMoveStacks.remove(["n", "Block"])
                        if ["n", "Mana"] in reasonableMoveStacks:
                            reasonableMoveStacks.remove(["n", "Mana"])
                        if ["n", "Copy"] in reasonableMoveStacks:
                            reasonableMoveStacks.remove(["n", "Copy"])
                        if ["y","Block"] in reasonableMoveStacks:
                            reasonableMoveStacks.remove(["y","Block"])
                    else:
                        if ["n", "Block"] in reasonableMoveStacks:
                            reasonableMoveStacks.remove(["n", "Block"])
                        if ["n", "Mana"] in reasonableMoveStacks:
                            reasonableMoveStacks.remove(["n", "Mana"])
                        if ["n", "Copy"] in reasonableMoveStacks:
                            reasonableMoveStacks.remove(["n", "Copy"])
                        if ["y", "Attack"] in reasonableMoveStacks:
                            reasonableMoveStacks.remove(["y", "Attack"])
                        if ["y", "Block"] in reasonableMoveStacks:
                            reasonableMoveStacks.remove(["y", "Block"])
                        if ["y", "Mana"] in reasonableMoveStacks:
                            reasonableMoveStacks.remove(["y", "Mana"])
                  if oppPlayer.chosenClass == "Cupid":
                      if oppPlayer.copiesLeft == 0:
                          forcedWin = True
                          if ["y", "Attack"] or ["y","Block"] or ["y","Mana"] in reasonableMoveStacks:
                              if ["n", "Attack"] in reasonableMoveStacks:
                                  reasonableMoveStacks.remove(["n", "Attack"])
                              if ["n", "Block"] in reasonableMoveStacks:
                                  reasonableMoveStacks.remove(["n", "Block"])
                              if ["n", "Mana"] in reasonableMoveStacks:
                                  reasonableMoveStacks.remove(["n", "Mana"])
                              if ["n", "Copy"] in reasonableMoveStacks:
                                  reasonableMoveStacks.remove(["n", "Copy"])
                          else:
                              if ["n", "Block"] in reasonableMoveStacks:
                                  reasonableMoveStacks.remove(["n", "Block"])
                              if ["n", "Mana"] in reasonableMoveStacks:
                                  reasonableMoveStacks.remove(["n", "Mana"])
                              if ["n", "Copy"] in reasonableMoveStacks:
                                  reasonableMoveStacks.remove(["n", "Copy"])
                              if ["y", "Attack"] in reasonableMoveStacks:
                                  reasonableMoveStacks.remove(["y", "Attack"])
                              if ["y", "Block"] in reasonableMoveStacks:
                                  reasonableMoveStacks.remove(["y", "Block"])
                              if ["y", "Mana"] in reasonableMoveStacks:
                                  reasonableMoveStacks.remove(["y", "Mana"])

        if forcedWin == False:
            #pointless moves
            if player.chosenClass == "Conjurer":
                    if ["y","Attack"] in reasonableMoveStacks:
                        reasonableMoveStacks.remove(["y","Attack"])
                    if ["y","Block"] in reasonableMoveStacks:
                        reasonableMoveStacks.remove(["y","Block"])
                    if ["y","Mana"] in reasonableMoveStacks:
                        reasonableMoveStacks.remove(["y","Mana"])




            if player.mana >= player.attackCost and player.blocks == 0 and oppPlayer.mana >= oppPlayer.attackCost and oppPlayer.blocks == 0:
                #neither player can block
                #usually, you should always attack here.
                #what affects this?
                #maybe if you're fireborne and your life is active
                #if null, you can reset maybe
                if player.chosenClass != "Fireborne" and oppPlayer.chosenClass != "Fireborne":
                    if ["n", "Mana"] in reasonableMoveStacks:
                        reasonableMoveStacks.remove(["n", "Mana"])
                    if ["y","Mana"] in reasonableMoveStacks:
                        reasonableMoveStacks.remove(["y","Mana"])


            elif player.mana >= player.attackCost and oppPlayer.mana >= oppPlayer.attackCost and oppPlayer.blocks == 0:
                #opponent can't block
                #should never mana: if opponent attacks, blocking is better. if opponent manas, attacking is better.
                #exception might be fireborne where manaing might be better
                #or null where resetting might be better
                if player.chosenClass != "Fireborne" and oppPlayer.chosenClass != "Fireborne":
                    if ["n", "Mana"] in reasonableMoveStacks:
                        reasonableMoveStacks.remove(["n", "Mana"])
                    if ["y", "Mana"] in reasonableMoveStacks:
                        reasonableMoveStacks.remove(["y", "Mana"])

            elif player.mana < player.attackCost and oppPlayer.mana < oppPlayer.attackCost:
                if ["n","Attack"] in reasonableMoveStacks:
                    reasonableMoveStacks.remove(["n","Attack"])
                if ["n","Block"] in reasonableMoveStacks:
                    reasonableMoveStacks.remove(["n","Block"])
                if ["n","Copy"] in reasonableMoveStacks:
                    reasonableMoveStacks.remove(["n","Copy"])
                if ["y","Attack"] in reasonableMoveStacks:
                    reasonableMoveStacks.remove(["y","Attack"])
                if ["y","Block"] in reasonableMoveStacks:
                    reasonableMoveStacks.remove(["y","Block"])



            elif oppPlayer.mana < oppPlayer.attackCost:
                # opponent can't attack
                # basically, you should never block here because there is no attack threat
                # any class have an attack threat on 0 mana?
                # don't think so
                #doesn't make sense for fireborne, #doesn't make sense for null even because you would have a 1-0 advantage at least for null
                if ["n", "Block"] in reasonableMoveStacks:
                    reasonableMoveStacks.remove(["n", "Block"])
                if ["y", "Block"] in reasonableMoveStacks:
                    reasonableMoveStacks.remove(["y", "Block"])


            elif player.chosenClass == "Thief":
              if player.stacksLeft > 0 and turn > 1 and oppPlayer.chosenClass != "Fireborne" and oppPlayer.chosenClass != "Conj" and oppPlayer.chosenClass != "Parrymaster" and oppPlayer.chosenClass != "Tax Collector":

                if player.mana == 0 and oppPlayer.mana == 1:
                    if ["y", "Block"] in reasonableMoveStacks:
                        reasonableMoveStacks.remove(["y", "Block"])

                elif oppPlayer.mana == 2:
                    if ["n","Attack"] in reasonableMoveStacks:
                        reasonableMoveStacks.remove(["n","Attack"])
                    if ["n", "Block"] in reasonableMoveStacks:
                        reasonableMoveStacks.remove(["n", "Block"])
                    if ["n", "Mana"] in reasonableMoveStacks:
                        reasonableMoveStacks.remove(["n", "Mana"])

                    #if ["y", "Attack"] not in reasonableMoveStacks and player.mana >= player.attackCost:
                        #reasonableMoveStacks.append(["y,"Attack"])

            elif player.chosenClass == "Null" and player.stacksLeft > 0:
                if oppPlayer.mana > 6*player.mana + player.blocks:
                    #print(player.stacksLeft)
                    if ["n","Attack"] in reasonableMoveStacks:
                        reasonableMoveStacks.remove(["n","Attack"])
                    if ["n", "Block"] in reasonableMoveStacks:
                        reasonableMoveStacks.remove(["n", "Block"])
                    if ["n", "Mana"] in reasonableMoveStacks:
                        reasonableMoveStacks.remove(["n", "Mana"])
                elif oppPlayer.chosenClass == "Copywriter":
                    if player.mana == 0 and ((player.blocks < 3 and oppPlayer.mana >= player.attackCost) or (player.blocks >= 3 and oppPlayer.mana >= player.blocks - 2)):
                        if ["n", "Attack"] in reasonableMoveStacks:
                            reasonableMoveStacks.remove(["n", "Attack"])
                        if ["n", "Block"] in reasonableMoveStacks:
                            reasonableMoveStacks.remove(["n", "Block"])
                        if ["n", "Mana"] in reasonableMoveStacks:
                            reasonableMoveStacks.remove(["n", "Mana"])
                elif oppPlayer.chosenClass == "Conjurer":
                    if oppPlayer.mana - 1 >= oppPlayer.attackCost and player.mana == 0 and oppPlayer.mana + oppPlayer.stacksLeft > player.blocks:
                        if ["n", "Attack"] in reasonableMoveStacks:
                            reasonableMoveStacks.remove(["n", "Attack"])
                        if ["n", "Block"] in reasonableMoveStacks:
                            reasonableMoveStacks.remove(["n", "Block"])
                        if ["n", "Mana"] in reasonableMoveStacks:
                            reasonableMoveStacks.remove(["n", "Mana"])
                else:
                    if ["y","Attack"] in reasonableMoveStacks:
                        reasonableMoveStacks.remove(["y","Attack"])
                    if ["y", "Block"] in reasonableMoveStacks:
                        reasonableMoveStacks.remove(["y", "Block"])
                    if ["y", "Mana"] in reasonableMoveStacks:
                        reasonableMoveStacks.remove(["y", "Mana"])

                    #print(player.mana)




    #print(reasonableMoveStacks)
    return reasonableMoveStacks







def movestack_resolve(player1,player2,player1InitialState,player2InitialState,turn):
    # Look at the #abm-classes channel to see if stacks apply before or after moves are resolved.
    # null first
    #global turn
    winner = ""
    game_over = False
    if player1.chosenClass == "Null" and player1.stackChoice == "y":
        player1 = player1InitialState.deep_copy()
        player2 = player2InitialState.deep_copy()
        player1.stacksLeft -= 1
        if player2.chosenClass == "Null":
            player2.stacksLeft -= 1


        #print(player1.mana, "          ", player2.mana)
        #print(player1.blocks, "          ", player2.blocks)
    elif player2.chosenClass == "Null" and player2.stackChoice == "y":
        player1 = player1InitialState.deep_copy()
        player2 = player2InitialState.deep_copy()
        player2.stacksLeft -= 1
        #print("Null used")
        #print(player2.stackChoice)
        #print(player2.stacksLeft)
        #print(player1.mana, "          ", player2.mana)
        #print(player1.blocks, "          ", player2.blocks)

    else:
        # double cupid second
        if player1.activeMove == "Copy" and player2.activeMove == "Copy":
            player1.copiesLeft -= 1
            player2.copiesLeft -= 1
        else:

            # cupid stuff first
            if player1.activeMove == "Copy":
                player1.activeMove = player2.activeMove
                if player1.activeMove == "Attack" and player1.mana < player1.attackCost:
                    player1.mana += player1.attackCost
                player1.copiesLeft -= 1
            elif player2.activeMove == "Copy":
                player2.activeMove = player1.activeMove
                if player2.activeMove == "Attack" and player2.mana < player2.attackCost:
                    player2.mana += player2.attackCost
                player2.copiesLeft -= 1
            # remember that copywriter takes place before moves are resolved, but it's not a stack.
            if player1.chosenClass == "Copywriter":
                if player1.copyStreak > 0 and player1.oppLastMove == player2.activeMove:
                    player1.copyStreak += 1
                else:
                    player1.copyStreak = 1
                if player1.copyStreak >= 3:
                    player1.mana += 1
                player1.oppLastMove = player2.activeMove

            if player2.chosenClass == "Copywriter":
                if player2.copyStreak > 0 and player2.oppLastMove == player1.activeMove:
                    player2.copyStreak += 1
                else:
                    player2.copyStreak = 1
                if player2.copyStreak >= 3:
                    player2.mana += 1
                player2.oppLastMove = player1.activeMove

            # parrymaster doesn't matter before or after
            # every other stack is after
            # so just put every stack after besides null.
            if player1.activeMove == "Attack":
                player1.mana -= player1.attackCost
                player1.blocks = 5
                if player1.chosenClass == "Duplicator":
                    player1.manaStreak = 0
                elif player1.chosenClass == "Stunner" or player1.chosenClass == "Juggernaut":
                    player1.attackStreak += 1
                if player2.activeMove == "Attack":

                    player2.mana -= player2.attackCost
                    player2.blocks = 5
                    if player2.chosenClass == "Duplicator":
                        player2.manaStreak = 0
                    if player2.chosenClass == "Stunner" or player2.chosenClass == "Juggernaut":
                        player2.attackStreak += 1
                    elif player2.chosenClass == "The Sumo":
                        player2.mana += player2.attackCost
                    if player1.chosenClass == "The Sumo":
                        player1.mana += player1.attackCost
                elif player2.activeMove == "Block":
                    if player2.chosenClass == "Duplicator":
                        player2.manaStreak = 0
                    if player2.chosenClass == "Stunner" or player2.chosenClass == "Juggernaut":
                        player2.attackStreak = 0
                    player2.blocks -= 1
                    if player2.chosenClass == "Gambler":
                        randInt = random.randint(1, 100)
                        if randInt <= 45:
                            #print("Nothing happens.")
                            player2.mana += 0
                        elif randInt <= 65:
                            #print("Gain 1 mana!")
                            player2.mana += 1
                        elif randInt <= 85:
                            #print("Double your mana!")
                            player2.mana *= 2
                        else:
                            #print("Lose all mana.")
                            player2.mana = 0
                    elif player2.chosenClass == "Defender":
                        player2.blocks += 1
                elif player2.activeMove == "Mana":
                    if player2.chosenClass == "Stunner" or player2.chosenClass == "Juggernaut":
                        player2.attackStreak = 0
                    player2.blocks = 5
                    player2.mana += 1
                    game_over = True
                    winner = "Player 1"
                    if player2.chosenClass == "Lucky":
                        randInt = random.randint(1, 100)
                        if randInt <= 25:
                            game_over = False
                            winner = ""
                    elif player2.chosenClass == "Fireborne" and player2.extraLifetimeRemaining > 0:
                        game_over = False
                        winner = ""
                        player2.extraLifetimeRemaining = 0

            elif player1.activeMove == "Block":
                player1.blocks -= 1
                if player1.chosenClass == "Duplicator":
                    player1.manaStreak = 0
                elif player1.chosenClass == "Stunner" or player1.chosenClass == "Juggernaut":
                    player1.attackStreak = 0
                elif player1.chosenClass == "Gambler":
                    randInt = random.randint(1, 100)
                    if randInt <= 45:
                        #print("Nothing happens.")
                        player1.mana += 0
                    elif randInt <= 65:
                        #print("Gain 1 mana!")
                        player1.mana += 1
                    elif randInt <= 85:
                        #print("Double your mana!")
                        player1.mana *= 2
                    else:
                        #print("Lose all mana.")
                        player1.mana = 0
                if player2.activeMove == "Attack":
                    if player2.chosenClass == "Duplicator":
                        player2.manaStreak = 0

                    player2.mana -= player2.attackCost

                    player2.blocks = 5
                    if player1.chosenClass == "Defender":
                        player1.blocks += 1
                    if player2.chosenClass == "Stunner" or player2.chosenClass == "Juggernaut":
                        player2.attackStreak += 1
                elif player2.activeMove == "Block":
                    if player2.chosenClass == "Duplicator":
                        player2.manaStreak = 0
                    if player2.chosenClass == "Stunner" or player2.chosenClass == "Juggernaut":
                        player2.attackStreak = 0
                    player2.blocks -= 1
                    if player2.chosenClass == "Gambler":
                        randInt = random.randint(1, 100)
                        if randInt <= 45:
                            #print("Nothing happens.")
                            player2.mana += 0

                        elif randInt <= 65:
                            #print("Gain 1 mana!")
                            player2.mana += 1
                        elif randInt <= 85:
                            #print("Double your mana!")
                            player2.mana *= 2
                        else:
                            #print("Lose all mana.")
                            player2.mana = 0
                elif player2.activeMove == "Mana":
                    if player2.chosenClass == "Stunner" or player2.chosenClass == "Juggernaut":
                        player2.attackStreak = 0
                    player2.mana += 1
                    player2.blocks = 5
                    if player2.chosenClass == "Advantaged" and turn <= 3:
                        player2.mana += 1
                    elif player2.chosenClass == "Duplicator":
                        player2.mana += (2 ** player2.manaStreak) - 1
                        player2.manaStreak += 1
                    elif player2.chosenClass == "Retired":
                        player2.mana -= 1
                    elif player2.chosenClass == "Cheater":
                        randInt = random.uniform(0, 1)
                        if randInt <= (1 / 3):
                            player2.mana += 1



            elif player1.activeMove == "Mana":
                if player1.mana == 0 and player2.mana == 0:
                    if player1.chosenClass == "Last Ditch":
                        if player1.lastDitchCounter % 2 != 0 or player1.lastDitchCounter == 0:
                            player1.lastDitchCounter += 1
                            player1.extraManaAdded += 1
                            player1.mana += player1.extraManaAdded
                        else:
                            player1.mana += player1.extraManaAdded
                            player1.lastDitchCounter += 1
                    if player2.chosenClass == "Last Ditch":
                        if player2.lastDitchCounter % 2 != 0 or player2.lastDitchCounter == 0:
                            player2.lastDitchCounter += 1
                            player2.extraManaAdded += 1
                            player2.mana += player2.extraManaAdded
                        else:
                            player2.mana += player2.extraManaAdded
                            player2.lastDitchCounter += 1
                player1.mana += 1
                player1.blocks = 5
                if player1.chosenClass == "Stunner" or player1.chosenClass == "Juggernaut":
                    player1.attackStreak = 0
                elif player1.chosenClass == "Advantaged" and turn <= 3:
                    player1.mana += 1
                elif player1.chosenClass == "Duplicator":
                    player1.mana += (2 ** player1.manaStreak) - 1
                    player1.manaStreak += 1
                elif player1.chosenClass == "Retired":
                    player1.mana -= 1
                elif player1.chosenClass == "Cheater":
                    randInt = random.uniform(0, 1)
                    if randInt <= (1 / 3):
                        player1.mana += 1
                if player2.activeMove == "Attack":
                    if player2.chosenClass == "Duplicator":
                        player2.manaStreak = 0
                    game_over = True
                    player2.mana -= player2.attackCost
                    player2.blocks = 5
                    winner = "Player 2"
                    if player2.chosenClass == "Stunner" or player2.chosenClass == "Juggernaut":
                        player2.attackStreak += 1
                    if player1.chosenClass == "Lucky":
                        randInt = random.randint(1, 100)
                        if randInt <= 25:
                            game_over = False
                            winner = ""
                    elif player1.chosenClass == "Fireborne" and player1.extraLifetimeRemaining > 0:
                        game_over = False
                        winner = ""
                        player1.extraLifetimeRemaining = 0

                elif player2.activeMove == "Block":
                    if player2.chosenClass == "Duplicator":
                        player2.manaStreak = 0
                    if player2.chosenClass == "Stunner" or player2.chosenClass == "Juggernaut":
                        player2.attackStreak = 0
                    player2.blocks -= 1
                    if player2.chosenClass == "Gambler":
                        randInt = random.randint(1, 100)
                        if randInt <= 45:
                            #print("Nothing happens.")
                            player2.mana += 0
                        elif randInt <= 65:
                            #print("Gain 1 mana!")
                            player2.mana += 1
                        elif randInt <= 85:
                            #print("Double your mana!")
                            player2.mana *= 2
                        else:
                            #print("Lose all mana.")
                            player2.mana = 0
                elif player2.activeMove == "Mana":
                    if player2.chosenClass == "Stunner" or player2.chosenClass == "Juggernaut":
                        player2.attackStreak = 0
                    player2.mana += 1
                    player2.blocks = 5
                    if player1.chosenClass == "Investor":
                        player1.mana += 1
                    if player2.chosenClass == "Investor":
                        player2.mana += 1

                    if player2.chosenClass == "Advantaged" and turn <= 3:
                        player2.mana += 1
                    elif player2.chosenClass == "Duplicator":
                        player2.mana += (2 ** player2.manaStreak) - 1
                        player2.manaStreak += 1
                    elif player2.chosenClass == "Retired":
                        player2.mana -= 1
                    elif player2.chosenClass == "Cheater":
                        randInt = random.uniform(0, 1)
                        if randInt <= (1 / 3):
                            player2.mana += 1

            # now starting here you put the stacks.
            if player1.stackChoice == "y":
                player1.stacksLeft -= 1
                if player1.chosenClass == "Thief":
                    if player2.mana > 0:
                        player1.mana += 1
                        player2.mana -= 1
                elif player1.chosenClass == "Tax Collector":
                    if player1.mana > 0:
                        player1.mana -= 1
                    if player2.mana > 0:
                        player2.mana -= 1
                elif player1.chosenClass == "Fireborne":
                    player1.extraLifetimeRemaining = 5
                elif player1.chosenClass == "Parrymaster":
                    if player2.activeMove == "Attack":
                        player2.blocks = 0

            if player2.stackChoice == "y":
                player2.stacksLeft -= 1
                if player2.chosenClass == "Thief":
                    if player1.mana > 0:
                        player2.mana += 1
                        player1.mana -= 1
                elif player2.chosenClass == "Tax Collector":
                    if player2.mana > 0:
                        player2.mana -= 1
                    if player1.mana > 0:
                        player1.mana -= 1

                elif player2.chosenClass == "Fireborne":
                    player2.extraLifetimeRemaining = 5
                elif player2.chosenClass == "Parrymaster":
                    if player1.activeMove == "Attack":
                        player1.blocks = 0

        # here you put the aftereffects of classes.
        if player1.chosenClass == "Stunner":
            player2.attackCost = 2 ** player1.attackStreak
        elif player1.chosenClass == "Juggernaut" and player1.attackStreak > 0 and player1.attackStreak % 2 == 0:
            player2.blocks = 0
        elif player1.chosenClass == "Fireborne" and player1.extraLifetimeRemaining > 0 and player1.stackChoice == "n":
            player1.extraLifetimeRemaining -= 1
        elif player1.chosenClass == "Investor" and turn % 3 == 0 and player1.mana > 0:
            player1.mana -= 1

        if player2.chosenClass == "Stunner":
            player1.attackCost = 2 ** player2.attackStreak
        elif player2.chosenClass == "Juggernaut" and player2.attackStreak > 0 and player2.attackStreak % 2 == 0:
            player1.blocks = 0
        elif player2.chosenClass == "Fireborne" and player2.extraLifetimeRemaining > 0 and player2.stackChoice == "n":
            player2.extraLifetimeRemaining -= 1
        elif player2.chosenClass == "Investor" and turn % 3 == 0 and player2.mana > 0:
            player2.mana -= 1

        turn += 1
        if player1.mana == 0 and player2.mana == 0:
            if player1.chosenClass == "Retired" and player2.chosenClass == "Retired":
                if player1.chosenClass == "Retired" and player2.chosenClass == "Retired":
                    player1.mana = 1
                    player1.blocks = 5
                    player1.chosenClass = "Joe"
                    player2.mana = 1
                    player2.blocks = 5
                    player2.chosenClass = "Joe"
            if player1.chosenClass == "Parrymaster" and player1.stackChoice == "y" and player2.activeMove == "Attack":
                player1.mana += 1
                player2.mana += 1
                player1.blocks = 5
                player2.blocks = 0
                if player2.chosenClass == "Parrymaster" and player2.stackChoice == "y" and player1.activeMove == "Attack":
                    player1.blocks = 0
                elif player2.chosenClass == "Advantaged" and turn <= 3:
                    player2.mana += 1
                elif player2.chosenClass == "Duplicator":
                    player2.mana += (2 ** player2.manaStreak) - 1
                    player2.manaStreak += 1
                elif player2.chosenClass == "Retired":
                    player2.mana -= 1
                elif player2.chosenClass == "Cheater":
                    randInt = random.uniform(0, 1)
                    if randInt <= (1 / 3):
                        player2.mana += 1
                elif player2.chosenClass == "Last Ditch":
                    player2.mana += 1
                    if player2.lastDitchCounter % 2 != 0 or player2.lastDitchCounter == 0:
                            player2.lastDitchCounter += 1
                            player2.extraManaAdded += 1
                            player2.mana += player2.extraManaAdded
                    else:
                            player2.mana += player2.extraManaAdded
                            player2.lastDitchCounter += 1
                #print(f"Turn {turn}")
                #print(player1.mana, "          ", player2.mana)
                #print(player1.blocks, "          ", player2.blocks)
            elif player2.chosenClass == "Parrymaster" and player2.stackChoice == "y" and player1.activeMove == "Attack":
                player1.mana += 1
                player2.mana += 1
                player1.blocks = 0
                player2.blocks = 5
                if player1.chosenClass == "Advantaged" and turn <= 3:
                    player1.mana += 1
                elif player1.chosenClass == "Duplicator":
                    player1.mana += (2 ** player1.manaStreak) - 1
                    player1.manaStreak += 1
                elif player1.chosenClass == "Retired":
                    player1.mana -= 1
                elif player1.chosenClass == "Cheater":
                    randInt = random.uniform(0, 1)
                    if randInt <= (1 / 3):
                        player1.mana += 1
                elif player1.chosenClass == "Last Ditch":
                    player1.mana += 1
                    if player1.lastDitchCounter % 2 != 0 or player1.lastDitchCounter == 0:
                            player1.lastDitchCounter += 1
                            player1.extraManaAdded += 1
                            player1.mana += player1.extraManaAdded
                    else:
                            player1.mana += player1.extraManaAdded
                            player1.lastDitchCounter += 1
                #print(f"Turn {turn}")
                #print(player1.mana, "          ", player2.mana)
                #print(player1.blocks, "          ", player2.blocks)
            else:
                player1.activeMove = "Mana"
                player1.stackChoice = "n"
                player2.activeMove = "Mana"
                player2.stackChoice = "n"
                #print(f"Turn {turn}")
                return movestack_resolve(player1,player2,player1InitialState, player2InitialState, turn)


        if player1.mana<0:
            print("Player 1")
            print(player1.activeMove)
            print(player2.stackChoice)
        if player2.mana<0:
            print("Player 2")
            print(player2.activeMove)
            print(player2.stackChoice)


        player1.activeMove = ""
        player2.activeMove = ""
        player1.movestackMade = False
        player2.movestackMade = False
        player1.stackChoice = ""
        player2.stackChoice = ""


    return player1, player2, turn, game_over, winner

def findConstraints(player1,player2,turn):
    #global player1
    #global player2
    global wins
    global winRate
    global p1SelectedRNG
    global p2SelectedRNG
    global movestackOptions
    global oppMovestackOptions


    goofyPlayer1Copy = player1.deep_copy()
    goofyPlayer2Copy = player2.deep_copy()

    player1BaseState = player(player1.chosenClass)
    player2BaseState = player(player2.chosenClass)
    initialTurn = turn

    roughInputPositionWR = unoptimalWinRatesFinder(goofyPlayer1Copy,goofyPlayer2Copy,turn)
    #print(roughInputPositionWR)



    constraints = [[-9999999, -9999999, -9999999, -9999999, -9999999, -9999999, -9999999,"Attack"],
                   [-9999999, -9999999, -9999999, -9999999, -9999999, -9999999, -9999999,"Block"],
                   [-9999999, -9999999, -9999999, -9999999, -9999999, -9999999, -9999999,"Mana"],
                   [-9999999, -9999999, -9999999, -9999999, -9999999, -9999999, -99999990,"Copy"],
                   [-9999999, -9999999, -9999999, -9999999, -9999999, -9999999, -9999999,"StackAttack"],
                   [-9999999, -9999999, -9999999, -9999999, -9999999, -9999999, -9999999,"StackBlock"],
                   [-9999999, -9999999, -9999999, -9999999, -9999999, -9999999, -9999999,"StackMana"]
                   ]








    movestackOptions = findReasonableMovestacks(player1, player2, player1BaseState, player2BaseState, turn, False, False)
    oppMovestackOptions = findReasonableMovestacks(player2, player1, player2BaseState, player1BaseState, turn, False, False)


    if player2.chosenClass == "Conjurer" and player2.stackChoice == "i":
        if ["y","Attack"] in oppMovestackOptions:
            oppMovestackOptions.remove(["y","Attack"])
        if ["y","Block"] in oppMovestackOptions:
            oppMovestackOptions.remove(["y","Block"])
        if ["y","Mana"] in oppMovestackOptions:
            oppMovestackOptions.remove(["y","Mana"])



    if ["y","Mana"] not in oppMovestackOptions:
        del constraints[6]
        #print("Deleted!")
    if ["y","Block"] not in oppMovestackOptions:
        del constraints[5]
        #print("Deleted!")

    if ["y","Attack"] not in oppMovestackOptions:
        del constraints[4]
        #print("Deleted!")

    if ["n","Copy"] not in oppMovestackOptions:
        del constraints[3]
        #print("Deleted!")

    if ["n","Mana"] not in oppMovestackOptions:
        del constraints[2]
        #print("Deleted!")

    if ["n","Block"] not in oppMovestackOptions:
        del constraints[1]
        #print("Deleted!")

    if ["n","Attack"] not in oppMovestackOptions:
        del constraints[0]
        #print("Deleted!")




    for movestackOption in movestackOptions:


        game_over = False
        firstPlayer1Copy = player1.deep_copy()
        firstPlayer2Copy = player2.deep_copy()
        firstPlayer1Copy.stackChoice = movestackOption[0]
        firstPlayer1Copy.activeMove = movestackOption[1]
        for oppMovestackOption in oppMovestackOptions:
            #print(initialTurn)
            game_over = False
            firstPlayer2Copy.stackChoice = oppMovestackOption[0]
            firstPlayer2Copy.activeMove = oppMovestackOption[1]
            secondPlayer1Copy = firstPlayer1Copy.deep_copy()
            secondPlayer2Copy = firstPlayer2Copy.deep_copy()
            #print(secondPlayer1Copy.activeMove)
            #print(secondPlayer2Copy.activeMove)

            #if player1.chosenClass == "Lucky":
            #elif player1.chosenClass == "Gambler":
            #elif player1.chosenClass == "Cheater":

            #if player2.chosenClass == "Lucky":
            #elif player2.chosenClass == "Gambler":
            #elif player2.chosenClass == "Cheater":

            secondPlayer1Copy, secondPlayer2Copy, turn, game_over, winner = movestack_resolve(secondPlayer1Copy,secondPlayer2Copy,player1BaseState,player2BaseState,turn)
            if game_over == True:
                if winner == "Player 1":
                    wrChange = 1-roughInputPositionWR
                else:
                    wrChange = 0-roughInputPositionWR
                turn = initialTurn
            else:
                roughNewPosWR = unoptimalWinRatesFinder(secondPlayer1Copy,secondPlayer2Copy,turn)
                wrChange = roughNewPosWR-roughInputPositionWR
                #print(wrChange)
                """findSubConstraints(move2)
                accurateWR = findFrequencies(move2)
                #gives accurate win rate for a certain move-combo from the start"""






            if movestackOption == ["n","Attack"]:
                if oppMovestackOption == ["n","Attack"]:
                    for equation in constraints:
                        if equation[-1] == "Attack":
                           equation[0] = wrChange
                elif oppMovestackOption == ["n","Block"]:
                    for equation in constraints:
                        if equation[-1] == "Block":
                           equation[0] = wrChange
                elif oppMovestackOption == ["n","Mana"]:
                    for equation in constraints:
                        if equation[-1] == "Mana":
                           equation[0] = wrChange
                elif oppMovestackOption == ["n","Copy"]:
                    for equation in constraints:
                        if equation[-1] == "Copy":
                           equation[0] = wrChange
                elif oppMovestackOption == ["y","Attack"]:
                    for equation in constraints:
                        if equation[-1] == "StackAttack":
                           equation[0] = wrChange
                elif oppMovestackOption == ["y","Block"]:
                    for equation in constraints:
                        if equation[-1] == "StackBlock":
                           equation[0] = wrChange
                elif oppMovestackOption == ["y","Mana"]:
                    for equation in constraints:
                        if equation[-1] == "StackMana":
                           equation[0] = wrChange
            elif movestackOption == ["n","Block"]:
                if oppMovestackOption == ["n","Attack"]:
                    #print(winRate)
                    for equation in constraints:
                        if equation[-1] == "Attack":
                           equation[1] = wrChange
                elif oppMovestackOption == ["n","Block"]:
                    for equation in constraints:
                        if equation[-1] == "Block":
                           equation[1] = wrChange
                elif oppMovestackOption == ["n","Mana"]:
                    for equation in constraints:
                        if equation[-1] == "Mana":
                           equation[1] = wrChange
                elif oppMovestackOption == ["n","Copy"]:
                    for equation in constraints:
                        if equation[-1] == "Copy":
                           equation[1] = wrChange
                elif oppMovestackOption == ["y","Attack"]:
                    for equation in constraints:
                        if equation[-1] == "StackAttack":
                           equation[1] = wrChange
                elif oppMovestackOption == ["y","Block"]:
                    for equation in constraints:
                        if equation[-1] == "StackBlock":
                           equation[1] = wrChange
                elif oppMovestackOption == ["y","Mana"]:
                    for equation in constraints:
                        if equation[-1] == "StackMana":
                           equation[1] = wrChange
            elif movestackOption == ["n","Mana"]:
                if oppMovestackOption == ["n","Attack"]:
                    for equation in constraints:
                        if equation[-1] == "Attack":
                           equation[2] = wrChange
                elif oppMovestackOption == ["n","Block"]:
                    for equation in constraints:
                        if equation[-1] == "Block":
                           equation[2] = wrChange
                elif oppMovestackOption == ["n","Mana"]:
                    for equation in constraints:
                        if equation[-1] == "Mana":
                           equation[2] = wrChange
                elif oppMovestackOption == ["n","Copy"]:
                    for equation in constraints:
                        if equation[-1] == "Copy":
                           equation[2] = wrChange
                elif oppMovestackOption == ["y","Attack"]:
                    for equation in constraints:
                        if equation[-1] == "StackAttack":
                           equation[2] = wrChange
                elif oppMovestackOption == ["y","Block"]:
                    for equation in constraints:
                        if equation[-1] == "StackBlock":
                           equation[2] = wrChange
                elif oppMovestackOption == ["y","Mana"]:
                    for equation in constraints:
                        if equation[-1] == "StackMana":
                           equation[2] = wrChange
            elif movestackOption == ["n","Copy"]:
                if oppMovestackOption == ["n","Attack"]:
                    for equation in constraints:
                        if equation[-1] == "Attack":
                           equation[3] = wrChange
                elif oppMovestackOption == ["n","Block"]:
                    for equation in constraints:
                        if equation[-1] == "Block":
                           equation[3] = wrChange
                elif oppMovestackOption == ["n","Mana"]:
                    for equation in constraints:
                        if equation[-1] == "Mana":
                           equation[3] = wrChange
                elif oppMovestackOption == ["n","Copy"]:
                    for equation in constraints:
                        if equation[-1] == "Copy":
                           equation[3] = wrChange
                elif oppMovestackOption == ["y","Attack"]:
                    for equation in constraints:
                        if equation[-1] == "StackAttack":
                           equation[3] = wrChange
                elif oppMovestackOption == ["y","Block"]:
                    for equation in constraints:
                        if equation[-1] == "StackBlock":
                           equation[3] = wrChange
                elif oppMovestackOption == ["y","Mana"]:
                    for equation in constraints:
                        if equation[-1] == "StackMana":
                           equation[3] = wrChange
            elif movestackOption == ["y","Attack"]:
                if oppMovestackOption == ["n","Attack"]:
                    for equation in constraints:
                        if equation[-1] == "Attack":
                           equation[4] = wrChange
                elif oppMovestackOption == ["n","Block"]:
                    for equation in constraints:
                        if equation[-1] == "Block":
                           equation[4] = wrChange
                elif oppMovestackOption == ["n","Mana"]:
                    for equation in constraints:
                        if equation[-1] == "Mana":
                           equation[4] = wrChange
                elif oppMovestackOption == ["n","Copy"]:
                    for equation in constraints:
                        if equation[-1] == "Copy":
                           equation[4] = wrChange
                elif oppMovestackOption == ["y","Attack"]:
                    for equation in constraints:
                        if equation[-1] == "StackAttack":
                           equation[4] = wrChange
                elif oppMovestackOption == ["y","Block"]:
                    for equation in constraints:
                        if equation[-1] == "StackBlock":
                           equation[4] = wrChange
                elif oppMovestackOption == ["y","Mana"]:
                    for equation in constraints:
                        if equation[-1] == "StackMana":
                           equation[4] = wrChange
            elif movestackOption == ["y","Block"]:
                if oppMovestackOption == ["n","Attack"]:
                    for equation in constraints:
                        if equation[-1] == "Attack":
                           equation[5] = wrChange
                elif oppMovestackOption == ["n","Block"]:
                    for equation in constraints:
                        if equation[-1] == "Block":
                           equation[5] = wrChange
                elif oppMovestackOption == ["n","Mana"]:
                    for equation in constraints:
                        if equation[-1] == "Mana":
                           equation[5] = wrChange
                elif oppMovestackOption == ["n","Copy"]:
                    for equation in constraints:
                        if equation[-1] == "Copy":
                           equation[5] = wrChange
                elif oppMovestackOption == ["y","Attack"]:
                    for equation in constraints:
                        if equation[-1] == "StackAttack":
                           equation[5] = wrChange
                elif oppMovestackOption == ["y","Block"]:
                    for equation in constraints:
                        if equation[-1] == "StackBlock":
                           equation[5] = wrChange
                elif oppMovestackOption == ["y","Mana"]:
                    for equation in constraints:
                        if equation[-1] == "StackMana":
                           equation[5] = wrChange
            elif movestackOption == ["y","Mana"]:
                if oppMovestackOption == ["n","Attack"]:
                    for equation in constraints:
                        if equation[-1] == "Attack":
                           equation[6] = wrChange
                elif oppMovestackOption == ["n","Block"]:
                    for equation in constraints:
                        if equation[-1] == "Block":
                           equation[6] = wrChange
                elif oppMovestackOption == ["n","Mana"]:
                    for equation in constraints:
                        if equation[-1] == "Mana":
                           equation[6] = wrChange
                elif oppMovestackOption == ["n","Copy"]:
                    for equation in constraints:
                        if equation[-1] == "Copy":
                           equation[6] = wrChange
                elif oppMovestackOption == ["y","Attack"]:
                    for equation in constraints:
                        if equation[-1] == "StackAttack":
                           equation[6] = wrChange
                elif oppMovestackOption == ["y","Block"]:
                    for equation in constraints:
                        if equation[-1] == "StackBlock":
                           equation[6] = wrChange
                elif oppMovestackOption == ["y","Mana"]:
                    for equation in constraints:
                        if equation[-1] == "StackMana":
                           equation[6] = wrChange
    for equation in constraints:
        del equation[-1]
    return constraints

class findFrequencies():
    def __init__(self, winRateTable):
        self.winRates = np.array(winRateTable)
        self.constraints = []
        self.vars = ["a","b","m","c","sa","sb","sm","t"]

    def add_constraint(self, constraint_func):
        self.constraints.append({'type': 'ineq', 'fun':constraint_func})

    def add_equality_constraint(self, constraint_func):
        self.constraints.append({'type': 'eq', 'fun': constraint_func})
    def objective(self, vars):
        t = vars[7]
        return -t

    def build_constraints(self):
        for row in self.winRates:
            self.add_constraint(lambda vars, r=row: np.dot(r, vars[:-1]) - vars[-1])


    def optimize(self):
        initial_guess = [0,0,0,0,0,0,0,0]
        bounds = [(0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (None, None)]
        result = minimize(self.objective, initial_guess,bounds=bounds, constraints=self.constraints)
        if result.success:
            print("Success")
        else:
            print("Fail")
        # Extracting the optimized variables and multiplying by 100
        a = result.x[0] * 100
        b = result.x[1] * 100
        m = result.x[2] * 100
        c = result.x[3] * 100
        sa = result.x[4] * 100
        sb = result.x[5] * 100
        sm = result.x[6] * 100
        t = result.x[7]  # If t is part of the output and you want to scale it as well

        #print("Optimized values (multiplied by 100):\n")
        print(f"\nAttack: {a:.1f}%, Block: {b:.1f}%, Mana: {m:.1f}%, Copy: {c:.1f}%, StackAttack: {sa:.1f}%, StackBlock: {sb:.1f}%, StackMana: {sm:.1f}%")
        print(f"Exploit value: {t:.1f}\n")
        randomNumber = random.uniform(0,100)
        #print(f"Random number:{randomNumber: .1f}")
        if randomNumber <= a:
            #print("Recommended move: Attack")
            return f"Attack, {t:.1f} exploit value"
        elif randomNumber <= a+b:
            #print("Recommneded move: Block")
            return f"Block, {t:.1f} exploit value"
        elif randomNumber <= a+b+m:
            #print("Recommended move: Mana")
            return f"Mana, {t:.1f} exploit value"
        elif randomNumber <= a+b+m+c:
            #print("Recommended move: Copy")
            return f"Copy, {t:.1f} exploit value"
        elif randomNumber <= a+b+m+c+sa:
            #print("Recommended move: StackAttack")
            return f"StackAttack, {t:.1f} exploit value"
        elif randomNumber <= a+b+m+c+sa+sb:
            #print("Recommended move: StackBlock")
            return f"StackBlock, {t:.1f} exploit value"
        else:
            #print("Recommended move: StackMana")
            return f"StackMana, {t:.1f} exploit value"
class findVillainFrequencies():
    def __init__(self, winRateTable):
        self.winRates = np.array(winRateTable)
        self.constraints = []
        self.vars = ["a","b","m","c","sa","sb","sm","t"]

    def add_constraint(self, constraint_func):
        self.constraints.append({'type': 'ineq', 'fun':constraint_func})

    def add_equality_constraint(self, constraint_func):
        self.constraints.append({'type': 'eq', 'fun': constraint_func})
    def objective(self, vars):
        t = vars[7]
        return -t

    def build_constraints(self):
        for row in self.winRates:
            self.add_constraint(lambda vars, r=row: np.dot(r, vars[:-1]) - vars[-1])


    def optimize(self):
        initial_guess = [0,0,0,0,0,0,0,0]
        bounds = [(0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (None, None)]
        result = minimize(self.objective, initial_guess,bounds=bounds, constraints=self.constraints)
        if result.success:
            print("Success")
        else:
            print("Fail")
        # Extracting the optimized variables and multiplying by 100
        a = result.x[0] * 100
        b = result.x[1] * 100
        m = result.x[2] * 100
        c = result.x[3] * 100
        sa = result.x[4] * 100
        sb = result.x[5] * 100
        sm = result.x[6] * 100
        t = result.x[7]  # If t is part of the output and you want to scale it as well

        #print("Optimized values (multiplied by 100):\n")
        print(f"\nAttack: {a:.1f}%, Block: {b:.1f}%, Mana: {m:.1f}%, Copy: {c:.1f}%, StackAttack: {sa:.1f}%, StackBlock: {sb:.1f}%, StackMana: {sm:.1f}%")
        print(f"Exploit value: {t:.1f}\n")
        freqs = [a,b,m,c,sa,sb,sm]
        return freqs


def solve(player1,player2,turn,button1,button2,moveLabel):
  global center_frame
  global movestackOptions
  if player2.chosenClass == "Conjurer" and player2.stackChoice == "a":
          if player1.chosenClass == "Stunner":
              player2.attackCost = 2**player1.attackStreak
          if player1.mana > 6 * player2.mana + player2.blocks and player1.mana > player1.attackCost:
              solution = "Attack"

          elif player2.mana < player2.attackCost:
              solution = "Mana"

          elif player1.mana > player2.mana:
              solution = "Attack"

          elif player1.blocks > 0:
              solution = "Block"

          elif player1.mana > player1.attackCost:
              solution = "Attack"

          else:
              solution = "Mana"

          randColor = "#{:06x}".format(random.randint(0, 0xFFFFFF))
          hex_color = randColor.lstrip('#')
          r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
          luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255
          if luminance > 0.5:
              fgColor = "#000000"
          else:
              fgColor = "#FFFFFF"
          button1.config(bg="#e6e6e6", text="Initialize Player 1")
          button2.config(bg="#e6e6e6", text="Initialize Player 2")
          moveLabel.config(text=solution, fg=fgColor, bg=randColor)
  else:
    if player1.chosenClass == "Stunner":
        player2.attackCost = 2**player1.attackStreak
    if player2.chosenClass == "Stunner":
        player1.attackCost = 2**player2.attackStreak

    #print(player1.mana)
    #print(player2.mana)
    #print(turn)
    winRateTable = findConstraints(player1,player2,turn)
    #print("Hero")
    for row in winRateTable:
        print(f"{row}\n")
    system = findFrequencies(winRateTable)
    system.build_constraints()
    system.add_equality_constraint(lambda vars: vars[0] + vars[1] + vars[2] + vars[3] +
                                        vars[4] + vars[5] + vars[6] - 1)
    solution = system.optimize()#filter string

    villainWinRateTable = findConstraints(player2,player1,turn)
    for rrow in villainWinRateTable:
        print(f"{rrow}\n")
    villainSystem = findVillainFrequencies(villainWinRateTable)
    villainSystem.build_constraints()
    villainSystem.add_equality_constraint(lambda vars: vars[0] + vars[1] + vars[2] + vars[3] + vars[4] + vars[5] + vars[6] - 1)
    villainOptimalFreqs = villainSystem.optimize()
    print(villainOptimalFreqs)
    list_string = ', '.join(map(lambda x: str(int(round(x))), villainOptimalFreqs))
    villainOptimalFreqLabel = ttk.Label(center_frame, text=list_string, font=("Arial",20))
    villainOptimalFreqLabel.grid(row=4,column=0)





    randColor =  "#{:06x}".format(random.randint(0, 0xFFFFFF))
    hex_color = randColor.lstrip('#')
    r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
    luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255
    if luminance > 0.5:
        fgColor = "#000000"
    else:
        fgColor = "#FFFFFF"
    button1.config(bg="#e6e6e6", text = "Initialize Player 1")
    button2.config(bg="#e6e6e6", text = "Initialize Player 2")
    moveLabel.config(text=solution,fg=fgColor,bg=randColor)

    #add an enter villain freqs option and an "exploit?" button




    estimatedVillainFreqLabels = []
    for index,option in enumerate(movestackOptions): #movestackOptions are villain's options because villain is the main character from their reference frame
        print(index)
        option_string = ', '.join(map(str, option))  # Make sure villainOptimalFreqs is assigned correctly
        villainFreqLabel = ttk.Label(center_frame, text=option_string, font=("Arial", 20))
        villainFreqLabel.grid(row=5,column=index,sticky="w",padx=5,pady=10)
        villainFreqEntry = ttk.Entry(center_frame,width=5, font = ("Arial", 20))
        villainFreqEntry.grid(row=6,column=index,sticky="w",padx=5,pady=10)
        estimatedVillainFreqLabels.append(villainFreqEntry)


    exploit_button = tk.Button(center_frame, text="Exploit", font=("Arial", 20),command=lambda: exploit(villainWinRateTable,collect_entries(estimatedVillainFreqLabels)))
    exploit_button.grid(row=7,column=0,pady=50)





def collect_entries(entries):
    # Collect values from each entry and create a list
    collected_values = [float(entry.get())/100 for entry in entries]
    print("Collected Entries:", collected_values)
    # Here, you can call your exploit function with the collected values
    return collected_values


def exploit(villainWinRateTable,villainHypothesizedFreqs):
    global oppMovestackOptions #hero's options because hero is the opponent from the villain's reference frame
    #build expression for each row in winrate table and attach the hypothesized freqs
    lowestSum = 100
    lowestExpression = ["n","Mana"]
    for row_num,expression in enumerate(villainWinRateTable):
        expressionSum = 0
        for index,value in enumerate(expression):
            if index <= len(villainHypothesizedFreqs)-1:
                expressionSum += value*villainHypothesizedFreqs[index]
        print(expressionSum)
        if expressionSum < lowestSum:
            lowestSum = expressionSum
            lowestExpression = oppMovestackOptions[row_num]

    bgColor =  "#{:06x}".format(random.randint(0, 0xFFFFFF))
    hex_color = bgColor.lstrip('#')
    r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
    luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255
    if luminance > 0.5:
        fgColor = "#000000"
    else:
        fgColor = "#FFFFFF"
    bestExploitLabel = tk.Label(center_frame, text=lowestExpression, font=("Arial",20),fg=fgColor,bg=bgColor)
    bestExploitLabel.grid(row=8,column=0,pady=50)
    #find which one is the greatest
    #return that action

def initializePlayer(chosenPlayer,button,selectedClass, **kwargs):
    global player1
    global player2
    button.config(bg="#34eb37", text = f"{chosenPlayer} INITIALIZED")
    if chosenPlayer == "Player 1":
        print("Player 1 initialized.")
        player1 = player(selectedClass,**kwargs)
    elif chosenPlayer == "Player 2":
        print("Player 2 initialized.")
        player2 = player(selectedClass,**kwargs)



def continue_action(selected_hero,selected_villain,frame):
    """Action to be performed when the Continue button is pressed."""
    global player1
    global player2
    global center_frame
    print(f"Selected Hero Class: {selected_hero}")
    print(f"Selected Villain Class: {selected_villain}")
    for widget in frame.winfo_children():
        widget.destroy()

    # Optionally, you can add a label indicating the screen has refreshed
    # Create frames for dropdowns
    dropdown_frame = tk.Frame(frame)
    dropdown_frame.pack(pady=0)

    # Left dropdowns
    left_frame = tk.Frame(dropdown_frame)
    left_frame.grid(row=0, column=0, padx=0,sticky="n")

    # Center dropdown
    center_frame = tk.Frame(dropdown_frame)
    center_frame.grid(row=0, column=1, padx=100,sticky="n")

    
    turnLabel = ttk.Label(center_frame, text="Turn", font=("Arial", 20))
    turnLabel.grid(row=0,column=0)
    turn_entry = ttk.Entry(center_frame,width=5, font = ("Arial", 20))
    turn_entry.grid(row=1,column=0)


    solve_button = tk.Button(center_frame, text="Solve", font=("Arial", 20), bg="blue",fg="white",command=lambda: solve(player1,player2,int(turn_entry.get()),initializeHeroButton,initializeVillainButton,optimalMoveLabel))
    solve_button.grid(row=2,column=0,pady=50)

    optimalMoveLabel = tk.Label(center_frame, text="", font=("Arial",20))
    optimalMoveLabel.grid(row=3,column=0,pady=25)



    heroTopLabel = ttk.Label(left_frame, text = f"Hero ({selected_hero})", font=("Arial", 20))
    heroTopLabel.grid(row=0, column =1)

    heroManaLabel = ttk.Label(left_frame, text="Mana", font=("Arial", 20))
    heroManaLabel.grid(row=1, column=0, sticky="w")
    hero_entry_1 = ttk.Entry(left_frame,width=5,font=("Arial",20))
    hero_entry_1.grid(row = 1, column = 1)

    heroBlocksLabel = ttk.Label(left_frame, text="Blocks", font=("Arial", 20))
    heroBlocksLabel.grid(row=2, column=0, sticky="w")
    hero_entry_2 = ttk.Entry(left_frame,width=5,font=("Arial",20))
    hero_entry_2.grid(row = 2, column = 1)

    if selected_hero == "Last Ditch":
        hero00sLabel = ttk.Label(left_frame, text="0-0s", font=("Arial", 20))
        hero00sLabel.grid(row=3, column=0, sticky="w")
        hero_00s_entry = ttk.Entry(left_frame, width=5, font=("Arial", 20))
        hero_00s_entry.grid(row=3, column=1)

        heroXtraLabel = ttk.Label(left_frame, text="LastXtraManaAdded", font=("Arial", 20))
        heroXtraLabel.grid(row=4, column=0, sticky="w")
        heroXtraEntry = ttk.Entry(left_frame, width=5, font=("Arial", 20))
        heroXtraEntry.grid(row=4, column=1)


        initializeHeroButton = tk.Button(left_frame, text="Initialize Player 1",font=("Arial",20),command=lambda: initializePlayer("Player 1",initializeHeroButton,selected_hero, mana=int(hero_entry_1.get()), blocks = int(hero_entry_2.get()),lastDitchCounter = int(hero_00s_entry.get()),extraManaAdded = int(heroXtraEntry.get())))
        initializeHeroButton.grid(row=5,column=1)

    elif selected_hero == "Cupid":
        heroCopiesLabel = ttk.Label(left_frame, text="Copies", font=("Arial", 20))
        heroCopiesLabel.grid(row=3, column=0, sticky="w")
        heroCopiesEntry = ttk.Entry(left_frame, width=5, font=("Arial", 20))
        heroCopiesEntry.grid(row=3, column=1)

        initializeHeroButton = tk.Button(left_frame, text="Initialize Player 1",font=("Arial",20),command=lambda: initializePlayer("Player 1",initializeHeroButton,selected_hero, mana=int(hero_entry_1.get()), blocks = int(hero_entry_2.get()),copiesLeft = int(heroCopiesEntry.get())))
        initializeHeroButton.grid(row=4,column=1)

    elif selected_hero == "Juggernaut" or selected_hero == "Stunner":
        heroAttackStreakLabel = ttk.Label(left_frame, text="Attack Streak", font=("Arial", 20))
        heroAttackStreakLabel.grid(row=3, column=0, sticky="w")
        heroAttackStreakEntry = ttk.Entry(left_frame, width=5, font=("Arial", 20))
        heroAttackStreakEntry.grid(row=3, column=1)

        initializeHeroButton = tk.Button(left_frame, text="Initialize Player 1", font=("Arial", 20),
                                         command=lambda: initializePlayer("Player 1", initializeHeroButton,
                                                                          selected_hero, mana=int(hero_entry_1.get()),
                                                                          blocks=int(hero_entry_2.get()),
                                                                          attackStreak=int(heroAttackStreakEntry.get())))
        initializeHeroButton.grid(row=4, column=1)

    elif selected_hero == "Duplicator":
        heroManaStreakLabel = ttk.Label(left_frame, text="Mana Streak", font=("Arial", 20))
        heroManaStreakLabel.grid(row=3, column=0, sticky="w")
        heroManaStreakEntry = ttk.Entry(left_frame, width=5, font=("Arial", 20))
        heroManaStreakEntry.grid(row=3, column=1)

        initializeHeroButton = tk.Button(left_frame, text="Initialize Player 1", font=("Arial", 20),
                                         command=lambda: initializePlayer("Player 1", initializeHeroButton,
                                                                          selected_hero, mana=int(hero_entry_1.get()),
                                                                          blocks=int(hero_entry_2.get()),
                                                                          manaStreak=int(heroManaStreakEntry.get())))
        initializeHeroButton.grid(row=4, column=1)

    elif selected_hero == "Copywriter":
        heroCopyStreakLabel = ttk.Label(left_frame, text="Copy Streak", font=("Arial", 20))
        heroCopyStreakLabel.grid(row=3, column=0, sticky="w")
        heroCopyStreakEntry = ttk.Entry(left_frame, width=5, font=("Arial", 20))
        heroCopyStreakEntry.grid(row=3, column=1)

        heroOppLastMoveLabel = ttk.Label(left_frame, text="Villain last move?", font=("Arial", 20))
        heroOppLastMoveLabel.grid(row=4, column=0, sticky="w")
        heroOppLastMoveEntry = ttk.Entry(left_frame, width=5, font=("Arial", 20))
        heroOppLastMoveEntry.grid(row=4, column=1)

        initializeHeroButton = tk.Button(left_frame, text="Initialize Player 1", font=("Arial", 20),
                                         command=lambda: initializePlayer("Player 1", initializeHeroButton,
                                                                          selected_hero, mana=int(hero_entry_1.get()),
                                                                          blocks=int(hero_entry_2.get()),
                                                                          copyStreak=int(heroCopyStreakEntry.get()),oppLastMove = heroOppLastMoveEntry.get()))
        initializeHeroButton.grid(row=5, column=1)

    elif selected_hero == "Thief" or selected_hero == "Tax Collector" or selected_hero == "Parrymaster" or selected_hero == "Null" or selected_hero == "Conjurer" or selected_hero == "Fireborne":
        heroStacksLeftLabel = ttk.Label(left_frame, text="Stacks", font=("Arial", 20))
        heroStacksLeftLabel.grid(row=3, column=0, sticky="w")
        heroStacksLeftEntry = ttk.Entry(left_frame, width=5, font=("Arial", 20))
        heroStacksLeftEntry.grid(row=3, column=1)
        if selected_hero == "Conjurer":
            heroConjureActiveLabel = ttk.Label(left_frame, text="Opponent's move?", font=("Arial", 20))
            heroConjureActiveLabel.grid(row=4, column=0, sticky="w")
            heroConjureActiveEntry = ttk.Entry(left_frame, width=5, font=("Arial", 20))
            heroConjureActiveEntry.grid(row=4, column=1)

            initializeHeroButton = tk.Button(left_frame, text="Initialize Player 1", font=("Arial", 20),
                                             command=lambda: initializePlayer("Player 1", initializeHeroButton,
                                                                              selected_hero,
                                                                              mana=int(hero_entry_1.get()),
                                                                              blocks=int(hero_entry_2.get()),
                                                                              stacksLeft=int(
                                                                                  heroStacksLeftEntry.get()),oppMove=heroConjureActiveEntry.get()))


            initializeHeroButton.grid(row=5, column=1)
        elif selected_hero == "Fireborne":
            heroLifeTimeLeftLabel = ttk.Label(left_frame, text="LifeTimeLeft", font=("Arial", 20))
            heroLifeTimeLeftLabel.grid(row=4, column=0, sticky="w")
            heroLifeTimeLeftEntry = ttk.Entry(left_frame, width=5, font=("Arial", 20))
            heroLifeTimeLeftEntry.grid(row=4, column=1)

            initializeHeroButton = tk.Button(left_frame, text="Initialize Player 1", font=("Arial", 20),
                                             command=lambda: initializePlayer("Player 1", initializeHeroButton,
                                                                              selected_hero,
                                                                              mana=int(hero_entry_1.get()),
                                                                              blocks=int(hero_entry_2.get()),
                                                                              stacksLeft=int(
                                                                                  heroStacksLeftEntry.get()),
                                                                              extraLifetimeRemaining=
                                                                                  int(heroLifeTimeLeftEntry.get())))
            initializeHeroButton.grid(row=5, column=1)

        else:
            initializeHeroButton = tk.Button(left_frame, text="Initialize Player 1", font=("Arial", 20),
                                             command=lambda: initializePlayer("Player 1", initializeHeroButton,
                                                                              selected_hero,
                                                                              mana=int(hero_entry_1.get()),
                                                                              blocks=int(hero_entry_2.get()),
                                                                              stacksLeft=int(
                                                                                  heroStacksLeftEntry.get())))
            initializeHeroButton.grid(row=4, column=1)

    else:
        initializeHeroButton = tk.Button(left_frame, text="Initialize Player 1",font=("Arial",20),command=lambda: initializePlayer("Player 1",initializeHeroButton,selected_hero, mana=int(hero_entry_1.get()), blocks = int(hero_entry_2.get())))
        initializeHeroButton.grid(row=3,column=1)




    # Right dropdowns
    right_frame = tk.Frame(dropdown_frame)
    right_frame.grid(row=0, column=2, padx=0,sticky="n")
    villainTopLabel = ttk.Label(right_frame, text = f"Villain ({selected_villain})", font=("Arial", 20))
    villainTopLabel.grid(row=0, column =1)

    villainManaLabel = ttk.Label(right_frame, text="Mana", font=("Arial", 20))
    villainManaLabel.grid(row=1, column=0, sticky="w")
    villain_entry_1 = ttk.Entry(right_frame,width=5,font=("Arial",20))
    villain_entry_1.grid(row = 1, column = 1)

    villainBlocksLabel = ttk.Label(right_frame, text="Blocks", font=("Arial", 20))
    villainBlocksLabel.grid(row=2, column=0, sticky="w")
    villain_entry_2 = ttk.Entry(right_frame,width=5,font=("Arial",20))
    villain_entry_2.grid(row = 2, column = 1)

    if selected_villain == "Last Ditch":
        villain00sLabel = ttk.Label(right_frame, text="0-0s", font=("Arial", 20))
        villain00sLabel.grid(row=3, column=0, sticky="w")
        villain_00s_entry = ttk.Entry(right_frame, width=5, font=("Arial", 20))
        villain_00s_entry.grid(row=3, column=1)

        villainXtraLabel = ttk.Label(right_frame, text="LastXtraManaAdded", font=("Arial", 20))
        villainXtraLabel.grid(row=4, column=0, sticky="w")
        villainXtraEntry = ttk.Entry(right_frame, width=5, font=("Arial", 20))
        villainXtraEntry.grid(row=4, column=1)


        initializeVillainButton = tk.Button(right_frame, text="Initialize Player 2",font=("Arial",20),command=lambda: initializePlayer("Player 2",initializeVillainButton,selected_villain, mana=int(villain_entry_1.get()), blocks = int(villain_entry_2.get()),lastDitchCounter = int(villain_00s_entry.get()),extraManaAdded = int(villainXtraEntry.get())))
        initializeVillainButton.grid(row=5,column=1)

    elif selected_villain == "Cupid":
        villainCopiesLabel = ttk.Label(right_frame, text="Copies", font=("Arial", 20))
        villainCopiesLabel.grid(row=3, column=0, sticky="w")
        villainCopiesEntry = ttk.Entry(right_frame, width=5, font=("Arial", 20))
        villainCopiesEntry.grid(row=3, column=1)

        initializeVillainButton = tk.Button(right_frame, text="Initialize Player 2",font=("Arial",20),command=lambda: initializePlayer("Player 2",initializeVillainButton,selected_villain, mana=int(villain_entry_1.get()), blocks = int(villain_entry_2.get()),copiesLeft = int(villainCopiesEntry.get())))
        initializeVillainButton.grid(row=4,column=1)

    elif selected_villain == "Juggernaut" or selected_villain == "Stunner":
        villainAttackStreakLabel = ttk.Label(right_frame, text="Attack Streak", font=("Arial", 20))
        villainAttackStreakLabel.grid(row=3, column=0, sticky="w")
        villainAttackStreakEntry = ttk.Entry(right_frame, width=5, font=("Arial", 20))
        villainAttackStreakEntry.grid(row=3, column=1)

        initializeVillainButton = tk.Button(right_frame, text="Initialize Player 2", font=("Arial", 20),
                                         command=lambda: initializePlayer("Player 2", initializeVillainButton,
                                                                          selected_villain, mana=int(villain_entry_1.get()),
                                                                          blocks=int(villain_entry_2.get()),
                                                                          attackStreak=int(villainAttackStreakEntry.get())))
        initializeVillainButton.grid(row=4, column=1)

    elif selected_villain == "Duplicator":
        villainManaStreakLabel = ttk.Label(right_frame, text="Mana Streak", font=("Arial", 20))
        villainManaStreakLabel.grid(row=3, column=0, sticky="w")
        villainManaStreakEntry = ttk.Entry(right_frame, width=5, font=("Arial", 20))
        villainManaStreakEntry.grid(row=3, column=1)

        initializeVillainButton = tk.Button(right_frame, text="Initialize Player 2", font=("Arial", 20),
                                         command=lambda: initializePlayer("Player 2", initializeVillainButton,
                                                                          selected_villain, mana=int(villain_entry_1.get()),
                                                                          blocks=int(villain_entry_2.get()),
                                                                          manaStreak=int(villainManaStreakEntry.get())))
        initializeVillainButton.grid(row=4, column=1)

    elif selected_villain == "Copywriter":
        villainCopyStreakLabel = ttk.Label(right_frame, text="Copy Streak", font=("Arial", 20))
        villainCopyStreakLabel.grid(row=3, column=0, sticky="w")
        villainCopyStreakEntry = ttk.Entry(right_frame, width=5, font=("Arial", 20))
        villainCopyStreakEntry.grid(row=3, column=1)

        villainOppLastMoveLabel = ttk.Label(right_frame, text="Hero last move?", font=("Arial", 20))
        villainOppLastMoveLabel.grid(row=4, column=0, sticky="w")
        villainOppLastMoveEntry = ttk.Entry(right_frame, width=5, font=("Arial", 20))
        villainOppLastMoveEntry.grid(row=4, column=1)


        initializeVillainButton = tk.Button(right_frame, text="Initialize Player 2", font=("Arial", 20),
                                         command=lambda: initializePlayer("Player 2", initializeVillainButton,
                                                                          selected_villain, mana=int(villain_entry_1.get()),
                                                                          blocks=int(villain_entry_2.get()),
                                                                          copyStreak=int(villainCopyStreakEntry.get()),oppLastMove=villainOppLastMoveEntry.get()))
        initializeVillainButton.grid(row=5, column=1)

    elif selected_villain == "Thief" or selected_villain == "Tax Collector" or selected_villain == "Parrymaster" or selected_villain == "Null" or selected_villain == "Conjurer" or selected_villain == "Fireborne":
        villainStacksLeftLabel = ttk.Label(right_frame, text="Stacks", font=("Arial", 20))
        villainStacksLeftLabel.grid(row=3, column=0, sticky="w")
        villainStacksLeftEntry = ttk.Entry(right_frame, width=5, font=("Arial", 20))
        villainStacksLeftEntry.grid(row=3, column=1)
        if selected_villain == "Conjurer":
            villainConjureActiveLabel = ttk.Label(right_frame, text="Conjure active? (a/i)", font=("Arial", 20))
            villainConjureActiveLabel.grid(row=4, column=0, sticky="w")
            villainConjureActiveEntry = ttk.Entry(right_frame, width=5, font=("Arial", 20))
            villainConjureActiveEntry.grid(row=4, column=1)

            initializeVillainButton = tk.Button(right_frame, text="Initialize Player 2", font=("Arial", 20),
                                             command=lambda: initializePlayer("Player 2", initializeVillainButton,
                                                                              selected_villain,
                                                                              mana=int(villain_entry_1.get()),
                                                                              blocks=int(villain_entry_2.get()),
                                                                              stacksLeft=int(
                                                                                  villainStacksLeftEntry.get()),stackChoice=villainConjureActiveEntry.get()))

            initializeVillainButton.grid(row=5, column=1)
        elif selected_villain == "Fireborne":
            villainLifeTimeLeftLabel = ttk.Label(right_frame, text="LifeTimeLeft", font=("Arial", 20))
            villainLifeTimeLeftLabel.grid(row=4, column=0, sticky="w")
            villainLifeTimeLeftEntry = ttk.Entry(right_frame, width=5, font=("Arial", 20))
            villainLifeTimeLeftEntry.grid(row=4, column=1)

            initializeVillainButton = tk.Button(right_frame, text="Initialize Player 2", font=("Arial", 20),
                                             command=lambda: initializePlayer("Player 2", initializeVillainButton,
                                                                              selected_villain,
                                                                              mana=int(villain_entry_1.get()),
                                                                              blocks=int(villain_entry_2.get()),
                                                                              stacksLeft=int(
                                                                                  villainStacksLeftEntry.get()),
                                                                              extraLifetimeRemaining=
                                                                                  int(villainLifeTimeLeftEntry.get())))
            initializeVillainButton.grid(row=5, column=1)

        else:
            initializeVillainButton = tk.Button(right_frame, text="Initialize Player 2", font=("Arial", 20),
                                             command=lambda: initializePlayer("Player 2", initializeVillainButton,
                                                                              selected_villain,
                                                                              mana=int(villain_entry_1.get()),
                                                                              blocks=int(villain_entry_2.get()),
                                                                              stacksLeft=int(
                                                                                  villainStacksLeftEntry.get())))
            initializeVillainButton.grid(row=4, column=1)

    else:
        initializeVillainButton = tk.Button(right_frame, text="Initialize Player 2",font=("Arial",20),command=lambda: initializePlayer("Player 2",initializeVillainButton,selected_villain, mana=int(villain_entry_1.get()), blocks = int(villain_entry_2.get())))
        initializeVillainButton.grid(row=3,column=1)



def unoptimalWinRatesFinder(player1,player2,turn):
    numbGames = 2500
    initialTurn = turn
    player1StartingState = player(player1.chosenClass)
    player2StartingState = player(player2.chosenClass)
    wins = 0
    for i in range(numbGames):
        thePlayer1Copy = player1.deep_copy()
        thePlayer2Copy = player2.deep_copy()
        winner = main_simul(thePlayer1Copy, thePlayer2Copy, player1StartingState, player2StartingState,
                            turn)  # we will have the main_game function return the winner
        turn = initialTurn
        if winner == "Player 1":
            wins += 1
    winRate = wins / numbGames
    return winRate
def main():
    root = tk.Tk()
    root.title("ABM Solver")

    # Set the default size of the window larger
    default_width = 2000
    default_height = 800
    root.geometry(f"{default_width}x{default_height}")

    # Create a frame to hold widgets
    frame = tk.Frame(root, width=default_width, height=default_height)
    frame.pack(fill=tk.BOTH, expand=True)

    # Bind the resize event to the function

    # Add a label with larger text size
    label = ttk.Label(frame, text="Select Classes:", font=("Arial", 20))  # Font size set to 20
    label.pack(pady=20)

    # Create a frame for the dropdowns
    dropdown_frame = tk.Frame(frame)
    dropdown_frame.pack(pady=20)

    # Hero Class dropdown on the left
    hero_label = ttk.Label(dropdown_frame, text="Hero Class", font=("Arial", 20))
    hero_label.grid(row=0, column=0, padx=10)

    hero_dropdown = ttk.Combobox(dropdown_frame, values=options, font=("Arial", 14))
    hero_dropdown.grid(row=1, column=0, padx=10)

    # Villain Class dropdown on the right
    villain_label = ttk.Label(dropdown_frame, text="Villain Class", font=("Arial", 20))
    villain_label.grid(row=0, column=1, padx=10)

    villain_dropdown = ttk.Combobox(dropdown_frame, values=options, font=("Arial", 14))
    villain_dropdown.grid(row=1, column=1, padx=10)

    continue_button = tk.Button(frame, text="Continue", font=("Arial", 20), command=lambda: continue_action(hero_dropdown.get(),villain_dropdown.get(),frame))
    continue_button.pack(pady=30)

    # Start the main loop
    root.mainloop()


def testWRs(player1,player2,turn):
    #print(player1.mana)
    #print(player2.mana)
    #print(turn)
    winRateTable = findConstraints(player1,player2,turn)
    #for row in winRateTable:
    #   print(f"{row}\n")
    system = findFrequencies(winRateTable)
    system.build_constraints()
    system.add_equality_constraint(lambda vars: vars[0] + vars[1] + vars[2] + vars[3] +
                                        vars[4] + vars[5] + vars[6] - 1)
    solution = system.optimize()
    return solution

if __name__ == "__main__":
    main()





