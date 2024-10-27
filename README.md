Since the game-tree is infinite due to the game not having a turn-limit, I used monte-carlo simulatinos to estimate the winrates of different positions.

To run these simluations, I first had to code the base-game logic. With 21 classes, this was one of the most time-consuming parts of the project.

After coding the base game, I began to code the monte-carlo simulations by forcing each player to select a random action that was available to them.

After this came the most challenging part. I needed to ensure that the agents in the simulation were not making any mistakes. If an action could not possibly benefit the player more than another action they could take, they should not take it.
This was by far the most difficult part of the simulations, because the unique class interactions created an unthinkable amount of these situations where a pure mistake should be avoided.

Finally, after completing the monte carlo simulations, I was able to estimate the winrate of any given position. However, since the players were still choosing their action at random, they still weren't playing optimally; they just weren't making any pure mistakes.
Consequently, the winrates were not completely accurate. I needed the winrates in order to find the best possible strategy for a given position.

Remember how in RPS the unexploitable frequencies are 33.33% for each? Well, to find the unexploitable frequencies for this game, I needed to find the winrate of each given position that could possbily result from you and your opponent's actions.

After finding these winrates, you create an expression for each action your opponent could take, with each expression having a variable for each action you could take.

The coefficients of these variables represent the frequency at which you take each action available to you. The goal is to maximize the lowest-valued expression. This is to make your exploitability as low as possible.

Doing this ensures that, no matter how your opponent tries to exploit you, their maximium winrate is 100% minus your win rate on that expression.

However, since my winrates were not accurate due to the players not playing optimally, this whole system was somewhat flawed.

What I realized was that I might not need accurate winrates. Instead, I could find the difference in winrate between the original position and the new possible positions. Using this, I was able to find more accurate solutions.
