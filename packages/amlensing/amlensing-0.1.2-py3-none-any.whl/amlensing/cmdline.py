#!/usr/bin/env python3
import argparse
import datetime
import logging
import os
from pathlib import Path

from amlensing import config, logger, set_loglevel


def get_args():
    parser = argparse.ArgumentParser(
        epilog="Default parameters are defined in the amlensing.cfg file.")
    parser.add_argument('-c', '--conf', metavar='<conf_file>',
                        help='Configuration file for one project')
    parser.add_argument('-C', '--dump-config', metavar='<conf_file>',
                        nargs='?', const='amlensing.cfg',
                        help='Dump a commented configuration file to <conf_file>. '
                        'Default to amlensing.cfg')
    parser.add_argument("-r", "--raw-cands-table", metavar="<rawcands_file>",
                        help="Use the given file as raw candidate")
    parser.add_argument("-n", "--jobs", type=int, metavar="<int>",
                        help="Threads to use for parallel computing")
    parser.add_argument("-p", "--prefix", metavar="<str>",
                        help="prefix in the name of output file")
    parser.add_argument("-L", "--no-lens-filter", action='store_true',
                        help="Do not apply lens filter, filter_lens = False")
    parser.add_argument("-B", "--no-bgs-filter", action='store_true',
                        help="Do not apply bgs filter, filter_bgs = False")
    parser.add_argument("-q", "--quiet", action='count',
                        help="Specify once to suppress information log messages, "
                        "twice to suppress warning and error log messages, "
                        "three times to suppress all log messages.")
    return parser.parse_args()


def set_config(args):
    # configuration file first, let cli args override later
    if args.conf and os.path.exists(args.conf):
        config.read(args.conf)
    if args.quiet in [1, 2, 3]:
        set_loglevel(['WARNING', 'CRITICAL', 99][args.quiet])

    if args.no_bgs_filter:
        config.set('general', 'filter_bgs', 'false')
    if args.no_lens_filter:
        config.set('general', 'filter_lens', 'false')
    if args.jobs:
        config.set('general', 'n_core', args.jobs)
    if args.prefix:
        config.set('general', 'prefix', args.prefix)
    if args.raw_cands_table:
        config.set('files', 'raw_cands_table', args.raw_cands_table)


def dump_default_config(filename):
    if os.path.exists(filename):
        print(f"{filename} already exists.")
        return

    print("Generating amlensing.cfg")
    package_config = Path(__file__).with_name("amlensing.cfg")
    with open(filename, "w") as conf_file:
        conf_file.write("# amlensing.cfg file\n")
        conf_file.write("# remove ';' to uncomment options\n\n")
        for line in open(package_config):
            if line[0] in '#[\n':  # comments or section header
                conf_file.write(line)
            else:
                conf_file.write(f';{line}')


def main():
    args = get_args()
    if args.dump_config:
        dump_default_config(args.dump_config)
        exit()

    set_config(args)

    if not os.path.exists("Results"):
        os.mkdir("Results")

    datetime_now = datetime.datetime.now()
    timestamp = datetime_now.strftime('%y-%m-%d_%H-%M-%S')
    logfile_basename = f"amlensing.{config['general']['prefix']}.{timestamp}.log"
    logfile = os.path.join("Results", logfile_basename)
    logfile_handler = logging.FileHandler(logfile)
    logger.addHandler(logfile_handler)

    for section in config:
        logger.debug(f"{section} {dict(config[section])}")

    try:
        from amlensing.main import main as amlensing_main
        amlensing_main()
    except FileNotFoundError as ve:
        logger.warning(ve)
        logger.warning('If you intend to use the default files, '
                       'you might want to run "download_data" sub-command first.')


if __name__ == "__main__":
    main()
