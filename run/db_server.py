
import 

arg_parser = argparse.ArgumentParser(description='Start the Reactive database server')
arg_parser.add_argument('--port', help='TCP Port on which to listen')
arg_parser.add_argument('--srap', help='Service Registry address:port')

args = arg_parser.parse_args()

main(args.port, args.srap)