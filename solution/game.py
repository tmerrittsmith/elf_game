"""
                                Elf Game

        Players run a business sending elves out to chop down wood.
        They can send their elves to three locations:

        * Woods - always returns $10 for each elf.

        * Forest - returns $20 if the weather is good, $0 if it is bad.

        * Mountain - returns $50 if the weather is good, $0 if bad.
                     Bad weather on the mountain will also kill your elves.

        The weather is bad with probability 1/3.

        If the player has enough funds, they can hire an extra elf at a
        cost of $75 per elf.

        The game lasts over ten days and the aim is to maximise your
        revenue. Players can choose how many elves to send to each
        location on a day by day basis.

"""
from collections import namedtuple
from random import choice


# ==============================================================================
#                               Game Simulator
# ==============================================================================

# Data Types to hold the information
# A game represents the current state of a particular player's game.
# day takes the values 1 to 10.
Game = namedtuple("game", "elves funds day")
NEW_GAME = Game(12, 0, 1)

# A Turn contains the number of elves the player would like to hire,
# and where to send all his elves.
Turn = namedtuple("Turn", "hired wood forest mountain")

# Weather options - 2 : 1 Good : Bad
WEATHER = ["Good", "Good", "Bad"]

def play_round(game, turn, weather):
    """ Play a single round of the game, and return an updated game state. """

    # Check for cheating
    if turn.hired * 75 > game.funds:
        raise Exception

    # Check we've got enough elves
    elves = game.elves + turn.hired
    if turn.wood + turn.forest + turn.mountain > elves:
        raise Exception

    if weather == "Bad":
        elves -= turn.mountain
        funds = game.funds + turn.wood * 10
        return Game(elves, funds, game.day + 1)
    else:
        funds = game.funds + 10*turn.wood + 20*turn.forest + 50*turn.mountain
        return Game(elves, funds, game.day + 1)


def play_game(bot, weather):
    """ Play all 10 rounds of the game. """

    game = NEW_GAME
    for n in range(10):
        turn = bot(game)
        game = play_round(game, turn, weather[n])

    return game


def simulation(bots):
    """ Play a single simulation, pitting all bots against
        each other with consistent weather conditions.
    """

    # Randomly generate a set of weather
    weather = [choice(WEATHER) for _ in range(10)]
    print(weather)
    
    results = {}

    for name, b in bots.items():
        results[name] = play_game(b, weather)

    return results



def run_simulation(bots, N):
    """ Run simulation N times and record the winners """

    winners = {name: 0 for name in bots}
    totals = {name: 0 for name in bots}

    for _ in range(N):
        results = simulation(bots)

        # Find the winner
        winner = ""
        winning_funds = 0
        for name, r in results.items():
            totals[name] += r.funds
            if r.funds > winning_funds:
                winner = name
                winning_funds = r.funds

        winners[winner] += 1

    print("Winners:", winners)
    print("Totals:", totals)




# ==============================================================================
#                               Bot Definitions
# ==============================================================================

"""
    A Bot is a function which should accept a 'Game' tuple
    and return the 'Turn' that they would like to take
    based upon the current state of the game.
"""


def Andy_Bot(g):
    """
    Optimal? strategy - on the last two turns, send all
    elves to the mountain, otherwise always send them
    to the forest.
    Hire as many elves as possible for the first 6 turns.
    then none after that.
    """

    if g.day >= 8:
        return Turn(0, 0, 0, g.elves)
    else:
        elves = g.elves + g.funds // 75
        return Turn(g.funds // 75, 0, elves, 0)


def Phil_Bot(g):
    #in the first third of the game, hire as many elves as possible
    #hit the forest every day
    #kick back and watch the green roll in

    hired = 0
    if g.day <= 3:
        hired = g.funds // 75

    return Turn(hired, 0, g.elves + hired, 0)


def tms_bot(g):
    # a more complex strategy involving elf hires, a proportion 
    # of elves going to the mountain and the forest
    
    hire = 0
    if g.funds>=300 and g.day <= 4:
        hire = g.funds // 75    
    elif g.elves == 0 and funds > 75:
        hire = 1

    elves = g.elves + hire
    #Hail Mary send all elves to the mountain on the last day
    if g.day == 10:
        return Turn(hire, 0, 0, elves)

    # send 20% of elves to the mountains when you have more than 30 elves
    if elves > 30:
        forest = 5*elves // 6
        return Turn(hire, 0, forest, elves - forest)
    else:
        return Turn(hire, 0, elves, 0)
    

def woodland_bot(g):
    # send all elves to the woods

    hire = 0
    if g.funds >= 75 and g.day < 2:
        hire = funds // 75

    return Turn(hire, g.elves + hire, 0, 0)


def jon_bot(g):
    # In the first half of the game, hire as many elves as possible
    #send 60% of elves to the woods, 10% forest and 30% mountains
    
    hire = 0
    if g.funds >= 75 and g.day < 5:
        hire = g.funds // 75

    wood = 6*(g.elves + hire) // 10
    forest = (g.elves + hire) // 10
    mountain = g.elves - wood - forest

    return Turn(hire, wood, forest, mountain)


def mountain_bot(g):
    #all elves to the mountain
    
    hire = 0
    if g.funds >= 75 and g.day < 2:
        hire = g.funds // 75
    
    return Turn(hire, 0, 0, g.elves + hire)


Bots = {
    "Andy": Andy_Bot,
    "Phil": Phil_Bot,
    "TMS" : tms_bot,
    "Jon":  jon_bot,
    "Woodland": woodland_bot,
    "Mountain": mountain_bot,
}


if __name__ == "__main__":
    run_simulation(Bots, 10)
