import safe_tester
import datetime
from datetime import date
import argparse

##Parser
parser = argparse.ArgumentParser()
parser.add_argument('-tng', type=str, required=True, help="What TNG-run do you want to process?")
parser.add_argument('-id', type=str, default = "none", help="Test run id. The output will have this id-tag.")
parser.add_argument('-n', '--name', type=str, default = "test", help="Test name. The output will have this name.")

args = parser.parse_args()
##Variables
if args.id != "none":
    test_name = args.name + "_" + args.id
else:
    test_name = args.name

##Processes to run, uncomment those that should be run.
#safe_tester.find_centrals(args.tng)
#safe_tester.simple_test_last_ten(args.tng, test_name, 99)
safe_tester.simple_test_all(args.tng, test_name, 99)
safe_tester.rotation_test(args.tng, test_name, 99)
