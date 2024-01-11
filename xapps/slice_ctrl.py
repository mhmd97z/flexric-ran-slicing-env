import time, argparse, logging
import xapp_sdk as ric
from utils import set_slice
logging.basicConfig(level=logging.INFO) # DEBUG INFO 

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--create", action="store_true", 
                    help="bring up slices")
    parser.add_argument("--reset", action="store_true", 
                    help="tear down slices")
    args = parser.parse_args() 
    
    
    if args.create:
        set_slice()

    elif args.reset:
        set_slice(reset=True)

    else:
        logging.info('Are you serious?!')
    
    logging.info('Exiting ... ')