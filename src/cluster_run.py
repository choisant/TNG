import safe_tester
import argparse

##Parser

parser = argparse.ArgumentParser()
parser.add_argument('-tng', type=str, required=True, help="What TNG-run do you want to process?")
parser.add_argument('-sub', '--subhalo', type=int, required=True, help="Subalo index")
parser.add_argument('-id', type=str, default = "none", help="Test run id. The output will have this id-tag.")
parser.add_argument('-n', '--name', type=str, default = "test", help="Test name. The output will have this name.")



args = parser.parse_args()


##Variables
if args.id != "none":
    test_name = args.name + "_" + args.id
else:
    test_name = args.name

##Processes to run, uncomment those that should be run.
print("Processing subhalo ", int(args.subhalo))
safe_tester.velocities(args.tng, test_name, int(args.subhalo), 99)
