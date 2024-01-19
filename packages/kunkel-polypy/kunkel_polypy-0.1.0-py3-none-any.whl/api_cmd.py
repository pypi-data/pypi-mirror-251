# Just an example and basic test tool for the 'example.py' module that will test each api endpoint individually by command.

import cmd
import os
import example as test

file_paths = "file_paths.yaml"
   

class TestCmdInterface(cmd.Cmd):
    """command interface"""

    prompt = "PolygonTestCMD$"

    def do_help(self, arg):
        keywords =  ["rsi - relative strength index",
                     "sma - simple moving average",
                     "ema - exponential moving average",
                     "tickers - view tickers (defaults to all)",
                     "contracts - display options contracts (defaults to all)",
                     "contract - display one select options contract",
                     "macd = moving average convergence/divergence",
                    ]
        print("Type keyword > Enter to test api endpoint. Customize request parameters in request_parameters.yaml! " + "\n")
        print("\n" + "KEYWORDS: " + "\n")
        for keyword in keywords:
            print(keyword)


    def do_rsi(self, arg):
        test.test("relative_strength_index")
        test.test_pagination("relative_strength_index")
        return
    
    def do_sma(self, arg):
        test.test("simple_moving_average")
        test.test_pagination("simple_moving_average")
        return
    
    def do_ema(self, arg):
        test.test("exponential_moving_average")
        test.test_pagination("exponential_moving_average")
        return

    def do_macd(self, arg):
        test.test("macd")
        test.test_pagination("macd")
        return
    
    def do_constracts(self, arg):
        test.test("options_contracts")
        test.test_pagination("options_contracts")
        return
    
    def do_contract(self, arg):
        test.test("options_contract")
        return

    def do_tickers(self, arg):
        test.test("view_tickers")
        test.test_pagination("view_tickers")
        return
    
    def do_tickerv3(self, arg):
        test.test("tickers_v3")
        return

    def do_cwd(self, arg):
        print(os.getcwd())

    
cli = TestCmdInterface()
cli.cmdloop()

