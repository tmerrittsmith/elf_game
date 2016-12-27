"""
            How much is an elf worth?

    My stratgy is based on the expected value of an elf
    at each stage of the game. For each terrain type we
    can calculate how much an elf is going to earn on
    average:

        * Woods: $10
        * Forest: $20 * 2/3 = $13.33
        * Mountain: $50 * 2/3 = $33.33

    Clearly, the mountain is the most profitable.
    However, we also need to take into account the future
    profitability of an elf, and the chance of losing that
    when sending it to the mountain. There is no good
    reason to ever send any elves to the woods.

    If E(n) is the expected value of an elf on turn n, we
    can calculate the expected value of the elves on turn
    (n - 1), given that we send a proportion m to the
    mountains and (1 - m) to the forest:

    For elves that go to the forest, we can expect 2/3 of $20 plus
    the future value of all of the elves.

    For elves that go to the mountain, we can expect 2/3 of $50
    but only 2/3 of the the future value of the elves.

    Exp = m * (2/3 * 50 + 2/3 * E(n)) + (1-m)*(2/3 * 20 + E(n))

    Simplifying, we get:

    Exp = [ 100m + 2m*E(n) + 40 - 40m + 3*E(n) - 3m*E(n) ] / 3
        = [ 60m - m*E(n) + 40 + 3*E(n) ] / 3
        = [ m(60 - E(n)) + 40 + 3*E(n) ] / 3

    If we want to maximise this, we need to send all of the
    elves to the mountain if E(n) < 60, otherwise, send them
    all to the forest.

    Now, we have a strategy, we can calculate the expected value
    at each stage working backwards from turn 11, where elves are
    worth 0 because there are no more turns left.

    Running the code below tells us that the only turns where the
    future value of an elf is worth less than $60 is on the last
    three turns.

    The last question to ask is about when we should hire elves. It
    costs $75 to hire an elf, so if we expect the elves to return
    more than $75, we should hire as many as possible. We can see
    that hiring elves is worthwhile on the first 7 turns.

    So, on the last three turns - keep your cash and send all of your
    elves to the mountains. Otherwise, get them to the forest and
    hire as many extras as possible.

    There are undoubtedly better strategies out there but I will
    leave those as an exercise to the reader ;).

"""


def calc_exp():

    exp = 0
    for turn in range(10, 0, -1):

        if exp < 60:
            # Send all to the mountain
            exp = (100 + 2*exp) / 3
        else:
            exp = (40 + 3*exp) / 3

        print("Turn:", turn, "Value:", exp)


if __name__ == "__main__":
    calc_exp()
