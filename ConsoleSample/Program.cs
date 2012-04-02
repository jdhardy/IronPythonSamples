using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using IronPython.Hosting;
using System.Reflection;
using System.IO;

namespace ConsoleSample {
    class Program {
        static void Main(string[] args) {
            var engine = Python.CreateEngine();
            engine.SetSearchPaths(new[] { "FlippingGame" });
            var scope = engine.ExecuteFile("ConsoleGame.py");
            dynamic main = scope.GetVariable("main");
            main();
        }
    }
}
