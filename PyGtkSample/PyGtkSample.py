# IronPython sample using Gtk#
# Released to Public Domain, 2012
# Doug Blank <doug.blank@gmail.com>
# -------------------------------------------
# To run on Linux:
# mono --runtime=v4.0 ipy.exe PyGtkSample.py

import clr
clr.AddReference("gtk-sharp")
clr.AddReference("gdk-sharp") # for colors
import Gtk
import Gdk # for colors

import FlippingGame

class GtkSampleWindow(Gtk.Window):
    def __init__(self, title):
        self.game = FlippingGame.FlippingGame()
        self.table = Gtk.Table(7, 2, True)
        self.table.Attach( Gtk.Label("Bankroll:"), 0, 1, 0, 1)
        self.bankrollLabel = Gtk.Label("")
        self.table.Attach( self.bankrollLabel, 1, 2, 0, 1)
        self.table.Attach( Gtk.Label("Wager:"), 0, 1, 1, 2)
        self.wagerBox = Gtk.Entry()
        self.table.Attach( self.wagerBox, 1, 2, 1, 2)
        self.table.Attach( Gtk.Label("Guess:"), 0, 1, 2, 3)
        self.guessHeadsButton = Gtk.RadioButton("Heads")
        self.table.Attach(self.guessHeadsButton, 1, 2, 2, 3)
        self.guessTailsButton = Gtk.RadioButton(self.guessHeadsButton, "Tails")
        self.table.Attach(self.guessTailsButton, 1, 2, 3, 4)
        self.flipButton = Gtk.Button("Flip!")
        self.flipButton.Clicked += self.flipButton_Click
        self.table.Attach( self.flipButton, 0, 2, 4, 5)
        self.resultLabel = Gtk.Label("")
        self.table.Attach( self.resultLabel, 0, 2, 5, 6)
        self.errorLabel = Gtk.Label("")
        self.table.Attach( self.errorLabel, 0, 2, 6, 7)
        self.Add(self.table)
        self.table.ShowAll()
        self._showBankroll()

    def flipButton_Click(self, sender, e):
        wager = self._getWager()
        if not wager:
            return

        guess = "H" if self.guessHeadsButton.Active else "T"
        won, toss = self.game.flip(guess, wager)

        self._showToss(won, toss)
        self._showBankroll()
        self._maybeEndGame()

    def _getWager(self):
        try:
            wager = int(self.wagerBox.Text)
        except ValueError as v:
            self.wagerBox.ModifyBase(Gtk.StateType.Normal, Gdk.Color(255, 0, 0))
            self._showError("Wager must be a number.")
            return
        else:
            self._hideError()
            self.wagerBox.ModifyBase(Gtk.StateType.Normal, Gdk.Color(255, 255, 255))

        if wager < 1:
            self.wagerBox.ModifyBase(Gtk.StateType.Normal, Gdk.Color(255, 0, 0))
            self._showError("Wager must be at least 1 credit.")
            return

        if wager > self.game.bankroll:
            self.wagerBox.ModifyBase(Gtk.StateType.Normal, Gdk.Color(255, 0, 0))
            self._showError("Wager cannot be more than your bankroll.")
            return

        return wager
    
    def _showError(self, error):
        self.errorLabel.Text = error
        self.errorLabel.ModifyFg(Gtk.StateType.Normal, Gdk.Color(255, 0, 0))
        self.errorLabel.Visible = True

    def _hideError(self):
        self.errorLabel.Visible = False

    def _showToss(self, won, toss):
        self.resultLabel.Text = toss
        self.resultLabel.ModifyFg(Gtk.StateType.Normal,
            Gdk.Color(0, 255, 0) if won else Gdk.Color(255, 0, 0))

    def _showBankroll(self):
        self.bankrollLabel.Text = str(self.game.bankroll)

    def _maybeEndGame(self):
        if self.game.bankroll <= 0:
            self._showToss(False, 'X')

            self.flipButton.Sensitive = False
            self.wagerBox.Sensitive = False
            self.guessHeadsButton.Sensitive = False
            self.guessTailsButton.Sensitive = False

    def OnDeleteEvent(self, event):
        Gtk.Application.Quit()

if __name__ == '__main__':
    Gtk.Application.Init()
    win = GtkSampleWindow("Coin Flipping")
    win.Show()
    Gtk.Application.Run()
