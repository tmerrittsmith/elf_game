"""
                Strategy 2 - More Advanced Solution

    This strategy is based upon similar assumptions to my
    1st strategy:

        * Hiring is more valuable at the start of the
          game. There will be some cut-off point at
          which hiring no longer makes sense, but
          before that, we should hire as many elves
          as possible.

        * The risk of sending elves to the mountains,
          namely the risk of losing future income from
          those elves, becomes less as the game goes
          on. At some point, we should start sending
          elves to the mountains exclusively; before
          that they should go to forest.


    The solution below calculates the expected outcomes of
    a particular strategy based upon all of the possible
    paths that could be taken dependant on the weather.

    An expected outcome is then calculated, to produce an
    overall comparison of strategies. This solution produces
    an indentical strategy to strategy1 - perhaps
    unsurprisingly given the same inital assumptions, but
    this shows that even when the impact of hiring is taken
    into account, the solution still holds.

    The recursive implementation here is hardly optimal
    but with the limited number of turns, it should suffice.
"""

from collections import defaultdict

class Strategy:

    def __init__(self, hire_before, forest_before):

        self.h = hire_before
        self.f = forest_before

        # cached values
        self.cached_outcomes = None


    def recurse(self, turn, elves, funds):

        # Check whether we should hire
        if turn <= self.h:
            elves += funds // 75
            funds = funds % 75

        # Stop once we get to the finish
        if turn == 11:
            yield funds

        else:

            # Send elves to the forest
            if turn <= self.f:

                # Good weather
                for x in self.recurse(turn+1, elves, funds + 20*elves):
                    yield x
                    yield x

                # Bad weather
                for x in self.recurse(turn+1, elves, funds):
                    yield x

            # Send elves to the mountain
            else:

                # Good weather
                for x in self.recurse(turn+1, elves, funds + 50*elves):
                    yield x
                    yield x

                # Bad weather
                for x in self.recurse(turn+1, 0, funds):
                    yield x
                        

    def outcomes(self):

        if self.cached_outcomes is not None:
            return self.cached_outcomes

        outcomes = defaultdict(int)
        for x in self.recurse(1, 12, 0):
            outcomes[x] += 1

        self.cached_outcomes = outcomes
        return outcomes


    def expected(self):
        """ Calculates average outcome """

        total, num = 0, 0
        for o, n in self.outcomes().items():
            total += o*n
            num += n

        return total / num




if __name__ == "__main__":

    # Print out a list of the top strategies
    expected = []
    for h in range(11):
        for f in range(11):
            s = Strategy(h, f)
            exp = s.expected()
            expected.append((h, f, exp))

    expected.sort(key = lambda x: x[2], reverse=True)
    for e in expected[:5]:
        print(e)


    winner = expected[0]
    s = Strategy(winner[0], winner[1])
    print(s.outcomes())



