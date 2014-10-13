"""Naval Fate.

Usage:
  naval_fate.py ship --speed=<kn> [--pcap=<file>] new <name>...
  naval_fate.py ship --speed=<kn> <name> move <x> <y> [--speed=<kn>]
  naval_fate.py ship --speed=<kn> shoot <x> <y>
  naval_fate.py mine --speed=<kn> (set|remove) <x> <y> [--moored | --drifting]
  naval_fate.py (-h | --help)
  naval_fate.py --version

Options:
  -h --help     Show this screen.
  --version     Show version.
  --speed=<kn>  Speed in knots [default: 10].
  --moored      Moored (anchored) mine.
  --drifting    Drifting mine.

"""
from docopt import docopt


if __name__ == '__main__':
    arguments = docopt(__doc__, version='Naval Fate 2.0')
    print(arguments)
    print('Speed = ', arguments['--speed'])
