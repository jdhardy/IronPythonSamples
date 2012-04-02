using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using IronPython.Hosting;

namespace ConsoleSample {
    class Program {
        static void Main(string[] args) {
            var engine = Python.CreateEngine();
            engine.ExecuteFile("FlippingGame/FlippingGame.py");
        }
    }
}
