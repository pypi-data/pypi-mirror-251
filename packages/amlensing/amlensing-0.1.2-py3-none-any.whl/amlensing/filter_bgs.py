import numpy as np
from astropy.table import Table

from amlensing import config, logger


def load_bgs(src_ids):
    """load gaia data for specified souice_id"""
    logger.info('Loading BGS data')
    bgs = Table.read(config['files']['bgs_data'])
    bgs = Table(bgs, masked=True, copy=False)

    if any(~np.isin(src_ids, bgs['source_id'])):
        logger.error('BGS data file does not contain all candidate sources.\n'
                     'Use amlensing-dl to download them algain.')
        exit(1)
    # find queried IDs in bgs data
    bgs.sort(keys=['source_id'])
    indices = np.searchsorted(bgs['source_id'], src_ids)
    bgs = bgs[indices]

    limit = config['bgs_limit'].getfloat('mag')
    bgs['filter_bgs_phot'] = bgs['phot_g_mean_mag'] < limit
    logger.info('Unique BGS: %d', len(bgs))
    return bgs


def filter_ruwe(bgs):
    """check if ruwe below limit for 5-parameter sources"""
    limit = config['bgs_limit'].getfloat('ruwe')

    good_ruwe = bgs['ruwe'] < limit
    # 'ruwe' column will have masked rows for 2-parameter sources
    # NOTE: do not use sum(good_px.mask) to count mask, the mask could be a single value
    logger.info('BGS Ruwe: %d/%d (+%d 2-param)',
                sum(good_ruwe.filled(False)),
                len(good_ruwe) - np.ma.count_masked(good_ruwe),
                np.ma.count_masked(good_ruwe))
    # assign two parameter sources (masked) to true
    return good_ruwe.filled(True)


def filter_gof(bgs):
    """Check if gof/n_good_obs below corresponding ruwe limit

    All sources have gof and n_good_obs, applicable also for sources with
    only a two parameter solution
    """
    ruwe_limit = config['bgs_limit'].getfloat('ruwe')

    def gof_from_ruwe(x):
        """translate ruwe limit to GoF limit. f(2) = 1.24; f(1.4) = 0.532"""
        return -4.80459 + 0.000520143 * np.sqrt(4.964e7 * x + 3.57727e7)

    gof = bgs['astrometric_gof_al']
    n_good = bgs['astrometric_n_good_obs_al']
    good = gof / np.sqrt(n_good) < gof_from_ruwe(ruwe_limit)

    logger.info('BGS GoF: %d/%d', np.sum(good), len(good))
    return good


def filter_px(bgs):
    """check if parallax is not signigicant negative
    only for source with a five parameter solution"""
    px_limit = config['bgs_limit'].getfloat('px')
    px_zero = config['general'].getfloat('zeropoint')

    px = bgs['parallax']
    px_error = bgs['parallax_error']
    good_px = (px - px_zero) / px_error > px_limit
    logger.info('BGS px: %d/%d (+%d 2-param)',
                sum(good_px.filled(False)),
                len(good_px) - np.ma.count_masked(good_px),
                np.ma.count_masked(good_px))
    # return True for two parameter sources
    return good_px.filled(True)


def filter_psi(bgs):
    """check if PSI value is above 1
    only for sources with G < 18
    see P. McGill et al. 2020"""
    # not used to filter data, since most are true Gaia_eDR3 sources
    dark = bgs['phot_g_mean_mag'] > 18
    gamma = np.maximum(10**(0.2 * (bgs['phot_g_mean_mag'] - 18)), 1)
    psi = bgs['astrometric_sigma5d_max'] / (1.2 * gamma)
    good_psi = psi < 1
    logger.info('BGS PSI: %d/%d', sum(~dark & good_psi), sum(~dark))

    return good_psi | dark


def filter_dr2(bgs):
    """filter dr3-dr2 crossmatches with their magnitude and angular differences"""
    mag_limit = config['DR2_limit'].getfloat('mag')
    good = bgs['magnitude_difference']**2 < \
        mag_limit**2 * bgs['angular_distance']**0.4

    # good.filled(True/False) will mark miss matches to True/False
    logger.info('BGS in DR2:')
    logger.info('  -found matches:  %d', len(good) - np.ma.count_masked(good))
    logger.info('    -good matches: %d', sum(good.filled(False)))
    logger.info('    -bad matches:  %d', sum(~good.filled(True)))
    logger.info('  -miss matches:   %d', np.ma.count_masked(good))
    # Description: only exclude close crossmatches with large mag differences (bad)
    return good.filled(True)


def dr2_dr3_propermotion(bgs):
    """use DR3-DR2 position distance to deduce missing proper motion"""
    pm_limit = config['bgs_limit'].getfloat('pm')
    pm_limit_bad = config['DR2_limit'].getfloat('pm_bad')
    dt = 0.5  # epoch difference between dr2 (2015.5) and dr3 (2016.0)
    cosdec = np.cos(np.deg2rad(bgs['dec']))

    pmra = (bgs['ra'] - bgs['dr2_ra']) * 3.6e6 * cosdec / dt
    pmdec = (bgs['dec'] - bgs['dr2_dec']) * 3.6e6 / dt
    pm2 = pmra**2 + pmdec**2
    # parallax
    parallax = 4.740 * pm2**0.5 / 75

    good = pm2 < pm_limit**2
    bad = ~good & (pm2 < pm_limit_bad**2)
    miss_match = ~good & ~bad
    pmra[miss_match] = pmdec[miss_match] = 0

    pm_prop = Table([good, bad, pmra, pmdec, parallax],
                    names=['pm_good', 'pm_bad', 'pmra_prop', 'pmdec_prop', 'parallax_prop'])

    logger.info('BGS proper motion in DR2: %d', len(pm2) - np.ma.count_masked(pm2))
    logger.info('  good matches: %d', np.sum(good))
    logger.info('  bad matches:  %d', np.sum(bad))
    logger.info('  miss matches: %d', np.sum(miss_match))
    return pm_prop


def filter_pos(bgs):
    """check positional error"""
    # Positional error better than 100
    limit = config['bgs_limit'].getfloat('pos_err')
    good_pos = bgs['ra_error']**2 + bgs['dec_error']**2 < limit**2

    logger.info('BGS pos: %d/%d', np.sum(good_pos), len(good_pos))
    return good_pos


def main(src_ids):
    bgs = load_bgs(src_ids)

    filter_result = Table()
    good_all = np.full(len(src_ids), True)
    for filter in [filter_gof, filter_pos, filter_px, filter_ruwe, filter_dr2]:
        good_f = filter(bgs)
        good_all &= good_f
        name = 'filter_bgs_' + filter.__name__.partition('_')[2]
        filter_result.add_column(good_f, name=name)
    filter_result.add_column(good_all, name='filter_bgs_all')

    pm_prop = dr2_dr3_propermotion(bgs)

    logger.info('BGS good: %d/%d', np.sum(good_all), len(good_all))

    return pm_prop, filter_result
