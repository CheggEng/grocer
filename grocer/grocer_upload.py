import sys
from lib import utils
import logging
import argparse
import grocer_test


def setup_logging(args):
    log = logging.getLogger('grocer')
    log.setLevel(getattr(logging, args.log_level.upper()))
    ch = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    log.addHandler(ch)
    return log


def upload(args, log):
    r = utils.get_file_types(args.path)
    log.info('Starting upload process')
    # berks install
    log.info('Running Berks Update')
    if sys.platform != 'darwin':
        berks_bin = '/opt/chef/embedded/bin/berks'
    else:
        berks_bin = args.berks_bin
    t = utils.berks(berks_bin, args.path, action="update")
    log.debug("{0}".format(t))
    if t[2] > 0:
        log.error(t[0]+t[1])
        sys.exit(1)
    log.info("{0}".format(t[0]))

    # berks upload
    log.info('Running Berks Upload')
    t = utils.berks(berks_bin, args.path, action='upload')
    log.debug("{0}".format(t))
    if t[2] > 0:
        log.error(t[0]+t[1])
        sys.exit(1)
    log.info("{0}".format(t[0]))
    log.info('Upload process complete')


def main():
    parser = argparse.ArgumentParser(description='Tool for uploading code to chef servers')
    parser.add_argument("-p", "--path", help="The path to the repo. Default is CWD", default='.', required=False)
    parser.add_argument("-b", "--berks_bin", help="The path to the berkshelf binary",
                        default='/opt/chefdk/bin/berks', required=False)
    parser.add_argument("--run_rubocop", help="Run Rubocop style tests?", action="store_true",
                        default=False, required=False)
    parser.add_argument('--run_rspec', help='Run Rspec?', action='store_true', default=False, required=False)
    parser.add_argument("--fc_strict", help="Should a FC issue cause grocer to fail?",
                        action='store_true', default=False)
    parser.add_argument("-f", "--foodcritic_bin", help="The path to the foodcritic binary",
                        default='/opt/chefdk/bin/foodcritic', required=False)
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
    l = setup_logging(args)
    grocer_test.test_all_the_things(args, l)
    upload(args, l)


if __name__ == '__main__':
    main()
