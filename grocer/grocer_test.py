from lib import utils
import argparse
import logging
import os
import sys


def setup_logging(args):
    log = logging.getLogger('grocer')
    log.setLevel(getattr(logging, args.log_level.upper()))
    ch = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    log.addHandler(ch)
    return log


def test_all_the_things(args, log):
    """
    Execute each test resource
    :param args: arguments from argparse
    :param log: logger object for this module
    :return: none
    """

    r = utils.get_file_types(args.path)

    log.info('Starting test process')

    # Run foodcritic
    log.info('Running Foodcritic')
    if sys.platform != 'darwin':
        fc_bin = '/opt/chef/embedded/bin/foodcritic'
    else:
        fc_bin = '/opt/chefdk/bin/foodcritic'
    t = utils.foodcritic(fc_bin, args.path, args.fc_strict)
    log.debug("{0}".format(t))
    if args.fc_strict:
        log.info("Friendly reminder: You've told foodcritic to be strict, so it will fail this job "
                 "if any of it's checks fail")
    if t[2] > 0:
        log.error(t[0]+t[1])
        sys.exit(1)
    log.info("{0}".format(t[0]))

    if args.run_rubocop:
        # Run rubocop
        log.info('Running Rubocop')
        t = utils.rubocop(args.rubocop_bin, args.path)
        log.debug("{0}".format(t))
        if t[2] > 0:
            log.error(t[0]+t[1])
            sys.exit(1)
        log.info("{0}".format(t[0]))

    # Run ruby config check
    log.info('Running Ruby Syntax Checks')
    for rfile in r[0]:
        log.info("Testing syntax for file {0}".format(rfile))
        t = utils.ruby_syntax(args.ruby_bin, os.path.join(args.path, rfile))
        log.debug("{0}".format(t))
        if t[2] > 0:
            log.error(t[0]+t[1])
            sys.exit(1)
    if args.run_rspec:
        # Run rspec tests
        log.info('Running rspec tests')
        t = utils.rspec_test(args.rspec_bin, args.test_path)
        log.debug("{0}".format(t))
        if t[2] > 0:
            log.error(t[0]+t[1])
            sys.exit(1)
        log.info("{0}".format(t[0]))

    log.info('Test process complete!')


def main():
    parser = argparse.ArgumentParser(description='Tool for running tests on a cookbook repo')
    parser.add_argument("-p", "--path", help="The path to the repo. Default is CWD", default='.', required=False)
    parser.add_argument("--run_rubocop", help="Run Rubocop style tests?", action="store_true",
                        default=False, required=False)
    parser.add_argument("--fc_strict", help="Should a FC issue cause grocer to fail?",
                        action='store_true' ,default=False)
    parser.add_argument("-f", "--foodcritic_bin", help="The path to the foodcritic binary",
                        default='/opt/chefdk/bin/foodcritic', required=False)
    parser.add_argument('--run_rspec', help='Run Rspec?', action='store_true', default=False, required=False)

    parser.add_argument("-r", "--ruby_bin", help="The path to the ruby binary",
                        default='/usr/bin/ruby', required=False)
    parser.add_argument("-s", "--rspec_bin", help="The path to the rspec binary",
                        default='/usr/bin/rspec', required=False)
    parser.add_argument("--rubocop_bin", help="The path to the rubocop binary",
                        default='/opt/chefdk/bin/rubocop', required=False)
    parser.add_argument("--test_path", help="The path to rspec tests",
                        default='.', required=False)
    parser.add_argument("-l", "--log_level", required=False, default='INFO')

    args = parser.parse_args()
    test_all_the_things(args, setup_logging(args))

if __name__ == '__main__':
    main()
