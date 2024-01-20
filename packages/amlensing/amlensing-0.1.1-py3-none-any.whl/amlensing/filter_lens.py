import numpy as np
from astropy.table import Table

from amlensing import config, logger


def load_lens(lens_ids):
    """load gaia data for specified souice_id"""
    logger.info('Load lens data')
    lens = Table.read(config['files']['lens_data'])
    lens = Table(lens, masked=True, copy=False)

    if any(~np.isin(lens_ids, lens['source_id'])):
        logger.error('Lens data file does not contain all candidate lenses.\n'
                     'Use amlensing-dl to download them algain.')
        exit(1)
    # find queried IDs in bgs data
    lens.sort(keys=['source_id'])
    indices = np.searchsorted(lens['source_id'], lens_ids)
    lens = lens[indices]

    logger.info('Unique lens: %d', len(lens))
    return lens


def filter_px(lens):
    """check if parallax significance"""
    limit = config['lens_limit'].getfloat('px')
    good_px = lens['parallax_over_error'] > limit
    logger.info('Lens parallax: %d/%d', np.sum(good_px), len(good_px))
    # Treat masked (those lack parallax) lens to have bad quality
    # TODO: it may be no masked array
    return good_px


def filter_ruwe(lens):
    """check if ruwe below limit"""
    limit = config['lens_limit'].getfloat('ruwe')
    good_ruwe = lens['ruwe'] < limit
    logger.info('Lens RUWE: %d/%d', np.sum(good_ruwe), len(good_ruwe))
    # Treat masked (those lack RUWE) lens to have bad quality
    return good_ruwe


def filter_flux(lens):
    """check n_obs / flux_over_error"""
    power = config['lens_limit'].getfloat('n_obs_sig_g_flux_power'),
    limit = config['lens_limit'].getfloat('n_obs_sig_g_flux')
    flux = lens['phot_g_mean_flux_over_error']
    n = lens['phot_g_n_obs']
    good = flux * n**power > limit
    logger.info('Lens NvsF: %d/%d', np.sum(good), len(good))
    return good.filled(False)


def filter_gcns(lens):
    # check low GNCS probability in it's reject catalogue
    bad = lens['gcns_prob_rej'] < 0.38
    good = (~bad).filled(True)
    logger.info('Lens GCNS: %d/%d', np.sum(good), len(good))
    return good


def filter_phot(lens):
    # check if phot_G brighter than the limit
    limit = config['lens_limit'].getfloat('mag')
    good = lens['phot_g_mean_mag'] < limit
    logger.info('Lens G mag: %d/%d', np.sum(good), len(good))
    return good


def main(lens_ids):
    lens = load_lens(lens_ids)

    filter_result = Table()
    good_all = np.full(len(lens_ids), True)
    for filter in [filter_px, filter_ruwe, filter_gcns, filter_phot, filter_flux]:
        good_f = filter(lens)
        good_all &= good_f
        name = 'filter_lens_' + filter.__name__.partition('_')[2]
        filter_result.add_column(good_f, name=name)
    filter_result.add_column(good_all, name='filter_lens_all')

    logger.info('Lens good: %d/%d', np.sum(good_all), len(good_all))

    return filter_result
