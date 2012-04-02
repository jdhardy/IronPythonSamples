using System;
using System.Drawing;
using System.Windows.Forms;
using IronPython.Hosting;
using Microsoft.Scripting.Hosting;

namespace WinFormsSample {
    public partial class FlippingGame : Form {
        ScriptEngine engine;
        ScriptScope scope;
        dynamic game;
        Random rand = new Random();

        public FlippingGame() {
            InitializeComponent();

            this.engine = Python.CreateEngine();
            this.engine.SetSearchPaths(new[] { "FlippingGame" });
            this.scope = this.engine.CreateScope();
        }

        private void FlippingGame_Load(object sender, EventArgs e) {
            this.scope.ImportModule("FlippingGame");
            this.engine.Execute("game = FlippingGame.FlippingGame()", this.scope);
            this.game = this.scope.GetVariable("game");

            ConstrainWager();
            ShowBankroll();

            ShowResult();
        }

        private void ShowBankroll() {
            bankrollLabel.Text = game.bankroll.ToString();
        }

        private void flipButton_Click(object sender, EventArgs e) {
            var wager = wagerBox.Value;
            var guess = guessHeadsRadio.Checked ? "H" : "T";

            var result = game.flip(guess, wager);
            var won = result[0];
            var toss = result[1];

            ShowSpinner();

            var timer = new Timer() {Interval = rand.Next(350, 1000)};
            timer.Tick += (t_sender, t_e) => {
                flippingBox.Visible = false;
                SetToss(toss.ToString(), (bool)won);
                ShowResult();
                
                ConstrainWager();
                ShowBankroll();

                ((Timer)t_sender).Stop();
            };

            timer.Start();
        }

        private void ShowResult() {
            resultLabel.Visible = true;
            flippingBox.Visible = false;
        }

        private void ShowSpinner() {
            resultLabel.Visible = false;
            flippingBox.Visible = true;
        }

        private void SetToss(string toss, bool won) {
            resultLabel.Visible = true;
            resultLabel.Text = toss;
            resultLabel.ForeColor = won ? Color.Green : Color.Red;
        }

        private void ConstrainWager() {
            var bankroll = game.bankroll;

            if (bankroll > 0) {
                wagerBox.Maximum = bankroll;
            } else {
                wagerBox.Enabled = false;
                flipButton.Enabled = false;
                guessHeadsRadio.Enabled = guessTailsRadio.Enabled = false;
                resultLabel.Text = "X";
                ShowResult();
            }
        }
    }
}
