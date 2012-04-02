from FlippingGame import FlippingGame
from System.Threading import Thread

def greeting():
    print "Welcome to Coin Flipping"
    print "------------------------"
    print

    return True

def get_wager(game):
    while True:
        wager = raw_input("Wager: ")
        try:
            w = int(wager)
        except ValueError:
            print "Wager must be a number (was '%s')." % wager
        else:
            if w < 1:
                print "You must wager at least 1 credit."
            elif w > game.bankroll:
                print "You cannot wager more than your bankroll."
            else:
                return w

def get_guess():
    while True:
        guess = raw_input("Guess [T/F]: ")
        guess = guess.upper()
        if len(guess) != 1 or guess not in "TF":
            print "Enter only T or F."
        else:
            return guess

def spin():
    for i in "|\-/" * 4:
        print i, '\r',
        Thread.Sleep(60)
    
    print

def turn(game):
    print
    print "Bankroll:", game.bankroll

    wager = get_wager(game)
    guess = get_guess()

    spin()

    result, toss = game.flip(guess, wager)

    print "Toss:", toss
    if result:
        print "YOU WIN!"
    else:
        print "Sorry, better luck next time."

    if game.bankroll == 0:
        return False

    again = raw_input("Play again? [Y/n]")
    return len(again) == 0 or again[0] in "Yy"

def main():
    playing = greeting()

    game = FlippingGame()

    while playing:
        playing = turn(game)

    print "Thanks for playing!"

if __name__ == '__main__':
    main()
