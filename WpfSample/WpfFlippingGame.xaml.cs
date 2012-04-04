using System.Windows;
using System.Windows.Media;
using IronPython.Hosting;
using Microsoft.Scripting.Hosting;

namespace WpfSample {
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class WpfFlippingGame : Window {
        ScriptEngine engine;
        ScriptScope scope;
        dynamic game;

        public WpfFlippingGame() {
            InitializeComponent();

            this.engine = Python.CreateEngine();
            this.engine.SetSearchPaths(new[] { "FlippingGame" });
            this.scope = this.engine.CreateScope();
        }

        private void Window_Loaded(object sender, RoutedEventArgs e) {
            this.scope.ImportModule("FlippingGame");
            this.engine.Execute("game = FlippingGame.FlippingGame()", this.scope);
            this.game = this.scope.GetVariable("game");

            ConstrainWager();
            ShowBankroll();

            ShowResult();
        }

        private void flipButton_Click(object sender, RoutedEventArgs e) {
            var wager = GetWager();
            if (wager <= 0)
                return;

            var guess = guessHeadsButton.IsChecked.Value ? "H" : "T";

            var result = game.flip(guess, wager);
            var won = result[0];
            var toss = result[1];

            SetToss(toss.ToString(), (bool)won);
            ShowResult();

            ConstrainWager();
            ShowBankroll();

            //ShowSpinner();

            //var timer = new Timer() { Interval = rand.Next(350, 1000) };
            //timer.Tick += (t_sender, t_e) => {
            //    flippingBox.Visible = false;
            //    SetToss(toss.ToString(), (bool)won);
            //    ShowResult();

            //    ConstrainWager();
            //    ShowBankroll();

            //    ((Timer)t_sender).Stop();
            //};

            //timer.Start();
        }

        private void wagerBox_GotFocus(object sender, RoutedEventArgs e) {
            wagerBox.Foreground = Brushes.Black;
        }

        private int GetWager() {
            int wager;
            if (!int.TryParse(wagerBox.Text, out wager)) {
                wagerBox.Foreground = Brushes.Red;
                ShowError("Wager must be a number.");

                return -1;
            }
            
            if (wager < 1) {
                wagerBox.Foreground = Brushes.Red;
                ShowError("Wager must be at least one credit.");

                return -1;
            }
            
            if (wager > game.bankroll) {
                wagerBox.Foreground = Brushes.Red;
                ShowError("Wager cannot be more than your bankroll.");

                return -1;
            }

            HideError();
            return wager;
        }

        private void ShowError(string error) {
            errorLabel.Content = error;
            errorLabel.Visibility = System.Windows.Visibility.Visible;
        }

        private void HideError() {
            errorLabel.Visibility = System.Windows.Visibility.Collapsed;
        }

        private void ShowBankroll() {
            bankrollLabel.Content = game.bankroll.ToString();
        }

        private void ShowResult() {
            //resultLabel.Visible = true;
            //flippingBox.Visible = false;
        }

        private void ShowSpinner() {
            //resultLabel.Visible = false;
            //flippingBox.Visible = true;
        }

        private void SetToss(string toss, bool won) {
            //resultLabel.Visibility = Visibility.Visible;
            resultLabel.Content = toss;
            resultLabel.Foreground = won ? Brushes.Green : Brushes.Red;
        }

        private void ConstrainWager() {
            var bankroll = game.bankroll;

            if (bankroll <= 0) {
                wagerBox.IsEnabled = false;
                flipButton.IsEnabled = false;
                guessHeadsButton.IsEnabled = guessTailsButton.IsEnabled = false;

                SetToss("X", false);
                ShowResult();
            }
        }
    }
}
