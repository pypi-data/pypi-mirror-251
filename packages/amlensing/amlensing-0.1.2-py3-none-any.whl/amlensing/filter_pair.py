import numpy as np
from astropy.table import Table

from amlensing import logger, config


def filter_px(pair, limit):
    """non similar parallax"""
    good_px = pair['ob_parallax'] < limit.getfloat('px') * pair['parallax']
    return good_px.filled(True)


def filter_pm(pair, limit):
    """non similar proper motion"""
    pm_lens = pair['pmdec']**2 + pair['pmra']**2
    pm_bgs = pair['ob_pmdec']**2 + pair['ob_pmra']**2
    pm_rel = (pair['pmra'] - pair['ob_pmra'])**2 + \
             (pair['pmdec'] - pair['ob_pmdec'])**2
    good_pm = pm_bgs < limit.getfloat('pm_sim_1')**2 * pm_lens
    good_pm &= pm_rel > limit.getfloat('pm_sim_2')**2 * pm_lens
    # Filter is not used for bgs without 5-parameter solution
    return good_pm.filled(True)


def filter_pm_dr2(pair, limit):
    """non similar proper motion for 2-parameter sources with help of
    proper motion deduced from dr2-dr3 displacement"""
    pm_lens = pair['pmdec']**2 + pair['pmra']**2
    pm_bgs = pair['ob_pmra_prop']**2 + pair['ob_pmdec_prop']**2
    pm_rel = (pair['pmra'] - pair['ob_pmra_prop'])**2 + \
             (pair['pmdec'] - pair['ob_pmdec_prop'])**2
    good_pm = pm_bgs < limit.getfloat('pm_sim_1')**2 * pm_lens
    good_pm &= pm_rel > limit.getfloat('pm_sim_2')**2 * pm_lens
    # Filter is not used for bgs with an 5-parameter solution
    good_pm.mask = ~good_pm.mask
    return good_pm.filled(True)


def filter_pm_tot_dr2(pair, limit):
    """ Filter on the absolute dr2 propermotion"""
    pm_bgs = pair['ob_pmra_prop']**2 + pair['ob_pmdec_prop']**2
    good_pm = pm_bgs < limit.getfloat('pm_tot')**2
    # Filter is not used for bgs with an 5-parameter solution
    good_pm.mask = ~good_pm.mask
    return good_pm.filled(True)


def main(cands):
    filter_result = Table()
    good_all = np.full(len(cands), True)
    if config['general'].getboolean('filter_bgs'):
        all_filters = [filter_pm, filter_px, filter_pm_dr2]
    else:
        all_filters = [filter_pm, filter_px]
    for filter in all_filters:
        good_f = filter(cands, config['Pair_limit'])
        good_all &= good_f
        name = 'filter_pair_' + filter.__name__.partition('_')[2]
        logger.info('%s: %d good, %d bad, %d total',
                    name, sum(good_all), sum(~good_all), len(good_all))
        filter_result.add_column(good_f, name=name)
    filter_result.add_column(good_all, name='filter_pair_all')

    logger.info('Pairs good: %d/%d', np.sum(good_all), len(good_all))

    return filter_result
