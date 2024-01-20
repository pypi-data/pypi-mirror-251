import argparse
import os


def download_plc3(number):
    '''download all the default raw data from "klueter et al 2021"'''
    import pyvo as vo

    lens_cols = [
        "source_id",
        "ra", "dec", "ra_error", "dec_error",
        "pmra", "pmdec", "pmra_error", "pmdec_error",
        "parallax", "parallax_error",
        "phot_g_mean_mag", "phot_rp_mean_mag", "phot_bp_mean_mag"
    ]
    bgs_cols = [f'ob_{c}' for c in lens_cols]
    # use int() to force check number is a number
    count = '' if number == 'all' else f'TOP {int(number)}'

    data = vo.dal.TAPService('http://dc.g-vo.org/tap').search(
        f'SELECT {count} * FROM plc3.rawcands'
    ).to_table()
    data.keep_columns(lens_cols + bgs_cols)

    return data


def query_lens(lens_id, verbose=False):
    from astroquery.gaia import Gaia

    columns = [
        "source_id", "parallax", "parallax_over_error",
        "phot_g_mean_flux_over_error", "phot_g_mean_mag",
        "phot_g_n_obs", "ruwe"
    ]
    lens = Gaia.launch_job_async(
        query='''
        SELECT
            {dr3_data},
            spur.fidelity_v2,
            tablec1.gcns_prob AS gcns_prob_main,
            tabler1.gcns_prob AS gcns_prob_rej
        FROM tap_upload.lens_id AS local
        LEFT JOIN gaiadr3.gaia_source AS dr3
            USING (source_id)
        LEFT JOIN external.gaiaedr3_spurious AS spur
            USING (source_id)
        LEFT JOIN external.gaiaedr3_gcns_main_1 as tablec1
            USING (source_id)
        LEFT JOIN external.gaiaedr3_gcns_rejected_1 as tabler1
            USING (source_id)
        '''.format(
            dr3_data=', '.join([f'dr3.{c}' for c in columns]),
        ),
        upload_resource=lens_id,
        upload_table_name='lens_id',
        verbose=verbose
    ).get_results()

    return lens


def query_bgs(src_id, verbose=False):
    """Query information for background sources

    Accept a list of source_id. Query the Gaia database for all required
    information and return a single table. Unavailble data will be empty.

    No 'WHERE' statement is used in the main query (but maybe in subquery) to
    keep the length of the query result to have the same length as the input.
    """
    from astroquery.gaia import Gaia

    dr3_columns = [
        'ra', 'ra_error', 'dec', 'dec_error',
        'pmra', 'pmdec', 'parallax', 'parallax_error',
        'phot_g_mean_mag', 'ruwe',
        'astrometric_n_good_obs_al',
        'astrometric_gof_al',
        'astrometric_sigma5d_max'
    ]
    dr2_columns = ['ra', 'dec', 'pmra', 'pmdec']

    # NOTE: dr2_neighbourhood is joined after a subquery, the reason is to
    # keep the final result length to be the same as input 'src_id',
    # otherwise, a outermost 'WHERE' will reduce the final number of result.
    # NOTE: angular_distance < 400 mas will select most true counterparts
    bgs = Gaia.launch_job_async(
        query='''
        SELECT
            local.source_id,
            {dr3_data},
            {dr2_data},
            bn.angular_distance,
            bn.magnitude_difference
        FROM tap_upload.src_id AS local
        LEFT JOIN gaiadr3.gaia_source AS dr3
            USING (source_id)
        LEFT JOIN (SELECT *
                   FROM gaiadr3.dr2_neighbourhood
                   WHERE angular_distance < 400) AS bn
            ON local.source_id = bn.dr3_source_id
        LEFT JOIN gaiadr2.gaia_source AS dr2
            ON bn.dr2_source_id = dr2.source_id
        '''.format(
            dr3_data=', '.join([f'dr3.{c}' for c in dr3_columns]),
            dr2_data=', '.join([f'dr2.{c} AS dr2_{c}' for c in dr2_columns])
        ),
        upload_resource=src_id,
        upload_table_name='src_id',
        verbose=verbose
    ).get_results()

    return bgs


def main():
    parser = argparse.ArgumentParser(
        epilog='Note: uses "ob_source_id" as bgs id and "source_id" as lens id')
    parser.add_argument('-r', '--raw_cands_file', metavar='<raw_cands>',
                        help='Specify another file as raw candidate file, '
                        'fallback to what\'s defined in config file')
    parser.add_argument('-d', '--debug', action='store_true')
    parser.add_argument('-b', '--bgs', action='store_true',
                        help='Download Gaia data using "ob_source_id" in <raw_cands>')
    parser.add_argument('-l', '--lens', action='store_true',
                        help='Download Gaia data using "source_id" in <raw_cands>')
    parser.add_argument('-K', '--plc3-rawcands', metavar='[<int>|all]',
                        help='Download (a subset of) data from Kluter 2022 and save '
                        'as <raw_cands>. The argument specifies the size of the '
                        'subset. Recommend a small number like 1000 for testing. '
                        'Specify "all" to download all the data (202070 items).')
    args = parser.parse_args()

    from astropy.table import unique
    from astropy.table import Table
    from amlensing import config, logger

    rawcands_file = args.raw_cands_file or config['files']['raw_cands_table']

    if args.plc3_rawcands:
        if os.path.exists(rawcands_file):
            res = input(f"{rawcands_file} already exists. Overwrite? [y]/n ")
            if res != '' and res not in 'yY':
                exit()
        rawcands = download_plc3(args.plc3_rawcands)
        logger.info("Saving plc3.rawcands data to %s", rawcands_file)
        rawcands.write(rawcands_file, overwrite=True)
    elif os.path.exists(rawcands_file):
        logger.info("Using raw candidate file %s", rawcands_file)
        rawcands = Table.read(rawcands_file)
    else:
        logger.error('Raw cands file %s does not exists', rawcands_file)
        exit(1)

    if args.lens:
        lens_id = unique(rawcands['source_id', ])
        logger.info('Unique lens: %d', len(lens_id))
        logger.info('Download lens quality data')
        lens = query_lens(lens_id, verbose=args.debug)
        lens.write("lens.fits", overwrite=True)

    if args.bgs:
        src_id = unique(rawcands['ob_source_id', ])
        src_id = Table(src_id, names=['source_id'])
        logger.info('Unique bgs: %d', len(src_id))
        logger.info('Download bgs quality data')
        bgs = query_bgs(src_id, verbose=args.debug)
        bgs.write("bgs.fits", overwrite=True)


if __name__ == '__main__':
    main()
