"""
Crossmatch given sources with Gaia DR3 sources by simple cone search
"""
import argparse


def parse_args():
    parser = argparse.ArgumentParser(
        description='')
    parser.add_argument('raw_cands_file', nargs='?',
                        help='Specify another file as raw candidate file, '
                        'fallback to config file option if not specified')
    parser.add_argument('-R', '--radius', metavar='<radius>', default=10,
                        help='Radius of cone search. E.g., 1 arcmin or 30". '
                        'If no unit are specified, arcsec is assumed. '
                        'Default is %(default)s arcsec.')
    parser.add_argument('-d', '--debug', action='store_true')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-b', '--bgs-data', metavar='<bgs_data>',
                       help='Provide source data and download lens data.')
    group.add_argument('-l', '--lens-data', metavar='<lens_data>',
                       help='Provide lens data and download source data.')
    return parser.parse_args()


def crossmatch(args):
    # laxy load these modules, to reduce script start-up time
    from astroquery.gaia import Gaia
    from astropy.table import Table
    from astropy.coordinates import Angle
    from amlensing import config

    radius = Angle(args.radius, unit='arcsec').deg
    cols = [
        "source_id",
        "ra", "dec", "ra_error", "dec_error",
        "pmra", "pmdec", "pmra_error", "pmdec_error",
        "parallax", "parallax_error",
        "phot_g_mean_mag", "phot_rp_mean_mag", "phot_bp_mean_mag"
    ]

    # Query construct step 1: lens and bgs columns
    local = Table.read(args.bgs_data or args.lens_data)
    if args.lens_data:
        lens_query = 'local.*'
        bgs_query = ', '.join([f'gaia.{c} AS ob_{c}' for c in cols])
        bgs_query += ', gaia.ref_epoch AS ob_epoch'
    else:
        lens_query = ', '.join([f'gaia.{c}' for c in cols])
        lens_query += ', gaia.ref_epoch AS epoch'
        bgs_query = ', '.join([f'local.{c} AS ob_{c}' for c in local.colnames])

    # Query construct step 2: exclude identical sources
    # if the source_id could be Gaia source id
    if local['source_id'].dtype.kind in 'iu':
        id_compare = 'AND local.source_id <> gaia.source_id'
    else:
        id_compare = '1 = 1'

    # Query construct
    query = f'''
        SELECT {lens_query}, {bgs_query}
        FROM gaiadr3.gaia_source as gaia
        JOIN tap_upload.local as local
            ON 1 = CONTAINS(
                POINT(local.ra, local.dec),
                CIRCLE(gaia.ra, gaia.dec, {radius}))
            AND {id_compare}'''

    table = Gaia.launch_job_async(
        query=query,
        upload_resource=local,
        upload_table_name='local',
        verbose=args.debug
    ).get_results()

    target = args.raw_cands_file or config['files']['raw_cands_table']
    table.write(target)


def main():
    args = parse_args()
    crossmatch(args)


if __name__ == '__main__':
    main()
