import argparse
from .agent import CodingHarness

def main():
    p=argparse.ArgumentParser(); p.add_argument("--task", default="Create hello.txt containing Hello harness"); p.add_argument("--live", action="store_true")
    args=p.parse_args(); result=CodingHarness(".", live=args.live).run(args.task); print(result)
if __name__ == "__main__": main()
