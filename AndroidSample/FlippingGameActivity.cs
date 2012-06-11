using System;

using Android.App;
using Android.Content;
using Android.Runtime;
using Android.Views;
using Android.Widget;
using Android.OS;
using Microsoft.Scripting.Hosting;
using IronPython.Hosting;
using System.IO;

namespace AndroidSample {
    [Activity(Label = "AndroidSample", MainLauncher = true, Icon = "@drawable/icon")]
    public class FlippingGameActivity : Activity {
        int count = 1;

        ScriptEngine engine = Python.CreateEngine();
        ScriptScope scope = null;
        object shadow;

        public FlippingGameActivity() {
            this.scope = this.engine.CreateScope();
            this.engine.Runtime.LoadAssembly(typeof(Resource).Assembly);
        }

        protected override void OnCreate(Bundle bundle) {
            base.OnCreate(bundle);

            InitShadow();
            this.engine.Operations.InvokeMember(this.shadow, "OnCreate", bundle);
        }

        private void InitShadow() {
            string code = null;
            using(var shadowStream = new StreamReader(this.Assets.Open("FlippingGameActivity.py"))) {
                code = shadowStream.ReadToEnd();
            }

            this.engine.Execute(code, this.scope);

            object shadowClass = this.scope.GetVariable("FlippingGameActivity");
            this.shadow = this.engine.Operations.CreateInstance(shadowClass, this);
        }
    }
}

