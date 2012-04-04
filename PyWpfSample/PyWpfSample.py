import wpf

import FlippingGame

from System.Windows import Application, Window, Visibility
from System.Windows.Media import Brushes

class WpfSampleWindow(Window):
    def __init__(self):
        wpf.LoadComponent(self, 'PyWpfSample.xaml')
        self.game = FlippingGame.FlippingGame()
    
    def flipButton_Click(self, sender, e):
        wager = self._getWager()
        if not wager:
            return

        guess = "H" if self.guessHeadsButton.IsChecked else "T"
        won, toss = self.game.flip(guess, wager)

        self._showToss(won, toss)
        self._showBankroll()
        self._maybeEndGame()
    
    def Window_Loaded(self, sender, e):
        self._showBankroll()

    def _getWager(self):
        try:
            wager = int(self.wagerBox.Text)
        except ValueError as v:
            self.wagerBox.Foreground = Brushes.Red
            self._showError("Wager must be a number.")
            return
        else:
            self._hideError()
            self.wagerBox.Foreground = Brushes.Black

        if wager < 1:
            self.wagerBox.Foreground = Brushes.Red
            self._showError("Wager must be at least 1 credit.")
            return

        if wager > self.game.bankroll:
            self.wagerBox.Foreground = Brushes.Red
            self._showError("Wager cannot be more than your bankroll.")
            return

        return wager
    
    def _showError(self, error):
        self.errorLabel.Content = error
        self.errorLabel.Visibility = Visibility.Visible

    def _hideError(self):
        self.errorLabel.Visibility = Visibility.Collapsed

    def _showToss(self, won, toss):
        self.resultLabel.Content = toss
        self.resultLabel.Foreground = Brushes.Green if won else Brushes.Red

    def _showBankroll(self):
        self.bankrollLabel.Content = str(self.game.bankroll)

    def _maybeEndGame(self):
        if self.game.bankroll <= 0:
            self._showToss(False, 'X')

            self.flipButton.IsEnabled = False
            self.wagerBox.IsEnabled = False
            self.guessHeadsButton.IsEnabled = False
            self.guessTailsButton.IsEnabled = False
    
    def wagerBox_GotFocus(self, sender, e):
        sender.Foreground = Brushes.Black

if __name__ == '__main__':
    Application().Run(WpfSampleWindow())
