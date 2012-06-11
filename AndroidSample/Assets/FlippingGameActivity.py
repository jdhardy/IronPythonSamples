from AndroidSample import Resource

class FlippingGameActivity(object):
    def __init__(self, main):
        self.main = main
        self.count = 1

    def OnCreate(self, bundle):
        # Set our view from the "main" layout resource
        self.main.SetContentView(Resource.Layout.Main);

        self.resultLabel = self.main.FindViewById(Resource.Id.resultLabel)
        self.resultLabel.Text = str(self.count)

        # Get our button from the layout resource,
        # and attach an event to it
        self.flipButton = self.main.FindViewById(Resource.Id.flipButton)
        self.flipButton.Click += lambda sender, e: self.button_Click(sender, e)

    def button_Click(self, sender, e):
        self.count += 1
        self.resultLabel.Text = str(self.count)
