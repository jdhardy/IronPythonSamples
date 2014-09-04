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
            return w

def get_guess():
    while True:
        guess = raw_input("Guess [T/H]: ")
        guess = guess.upper()
        if len(guess) != 1 or guess not in "TH":
            print "Enter only T or H."
        else:
            return guess

def spin():
    for i in "|\-/" * 4:
        print i, '\r',
        Thread.Sleep(60)
    
    print '\r'

def turn(game):
    print "Bankroll:", game.bankroll

    while True:
        wager = get_wager(game)
        msg = game.check_wager(wager)
        if msg:
            print msg
        else:
            break

    guess = get_guess()

    result, toss = game.flip(guess, wager)

    spin()
    
    print "Toss:", toss
    if result:
        print "YOU WIN!"
    else:
        print "Sorry, better luck next time."

    print

    if game.bankroll == 0:
        return False

    again = raw_input("Play again? [Y/n]")
    print
    return len(again) == 0 or again[0] in "Yy"

def main():
    playing = greeting()

    game = FlippingGame()

    while playing:
        playing = turn(game)

    print "Thanks for playing!"

if __name__ == '__main__':
    main()
