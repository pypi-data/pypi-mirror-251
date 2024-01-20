"""
GAML, Gaia-based Astrometric Gravitational Micro-Lensing Prediction
Copyright (C) 2022 Lu Xu
Based on amlensing
Copyright (C) 2021 Klüter
See LICENSE for details
"""

import os
import time
from multiprocessing import Pool

from astropy.table import Table, vstack
import numpy as np

from amlensing import approx, raw_data, mass, microlensing, calculation, config, logger


def determine_einstein_radii(cand):
    # calculate Einstein Radii (see microlensing.py)
    ThetaE, ThetaE_error = microlensing.einstein_radius(cand)
    cand['ThetaE'] = ThetaE
    cand['ThetaE_error'] = ThetaE_error
    logger.info('-------------------------')


def approx_filter(cand):
    # calculate_approx_date (see find_closest.py)
    logger.info('calc approx shift')
    approx.apply(cand)

    # filter n approximated effect
    cand = cand[(cand['approx_shift'] > config['lensing_limit'].getfloat('approx_shift_limit')) |
                (cand['approx_dist'] < 2 * cand['parallax'])]
    logger.info('Candidates with large approximated shifts and small separation: %d', len(cand))
    epoch_start = config['epoch'].getfloat('epoch_start')
    epoch_end = config['epoch'].getfloat('epoch_end')
    if not config['record_filters'].getboolean('epoch'):
        cand = cand[(cand['approx_tca'] > epoch_start) & (cand['approx_tca'] < epoch_end)]
    logger.info('Candidates with closest approach time between %.1f and %.1f: %d',
                epoch_start, epoch_end, len(cand))
    logger.info('-------------------------')
    return cand


def calc(cand):
    n_core = min(config['general'].getint('n_core'), len(cand))
    logger.info('calculate_Effect')
    logger.info('Split process on %i Cores', n_core)

    # parallel computing
    with Pool(n_core) as pool:
        # split raw_data into multiple parts for parallel computing
        sub_tables = enumerate(map(Table, np.array_split(cand, n_core)))
        table_out = vstack(pool.starmap(calculation.parallel, sub_tables))
    logger.info('-------------------------')
    return table_out


def filter_events(table_out):
    logger.info('Filter events')
    outfmt = config['general']['output_format']
    prefix = config['general']['prefix']

    # filter results
    shift_limit = config['lensing_limit'].getfloat('shift_limit')  # in mas
    mag_limit = config['lensing_limit'].getfloat('mag_limit')  # in mas
    shift_01 = table_out['shift_plus'] > shift_limit
    shift_L2_01 = table_out['L2_shift_plus'] > shift_limit
    mag = table_out['magnification'] > mag_limit
    # either mag or shift or shift_L2 meets the requirement
    FF = mag | shift_01 | shift_L2_01

    # save results
    logger.info('save filtered results')
    logger.info(f'Results/amlensing.{prefix}.{outfmt}')
    if outfmt == 'fits':
        for j, i in enumerate(table_out.keys().copy()):
            table_out.meta['TCOMM%i' % (j + 1)] = table_out[i].description
    # TODO: record filter
    table_out[FF].write(f'Results/amlensing.{prefix}.{outfmt}', overwrite=True)
    logger.info('-------------------------')

    return table_out[FF]


def add_description(tab):
    information = [
        ('t_E', 'yr', 'Einstein time scale of the event'),
        ('approx_tca', 'year', 'Approximated date of the closest appoach '),
        ('approx_dist', 'mas', 'Approximated separation at the closest appoach '),
        ('approx_shift', 'mas', 'Approximated centroid shift without parallax effect'),
        ('ddt_timedelay', '1/s', 'Second derivative of Shapiro time delay at closest approach'),
        ('TCA', 'year', 'Epoch of the closest approch'),
        ('dist', 'mas', 'Closest distance'),
        ('ThetaE', 'mas', 'Einstein radius of the event'),
        ('star_type', '', 'Type of the lensing star'),
        ('mass', 'M_sun', 'Mass of the lensing star'),
        ('t_aml', 'yr', 'Expected duration of the event (shift > 1muas)'),
        ('t_thres', 'yr', 'Time scale of variation by a threshold (shift > 1muas'),
        ('nonlinearity', 'mas', 'Difference of the non-linear centroid trajectory from linear motion.'),
        ('u', '', 'Closest distance in Einstein radii'),
        ('shift', 'mas', 'Expected shift of the center of light'),
        ('shift_plus', 'mas', 'Expected shift of image (+)'),
        ('shift_lum', 'mas', 'Expected shift including luminous-lens effect'),
        ('magnification', 'mag', 'Magnification in magnitudes'),
        ('ob_pmra_prop', 'mas', 'Proper motion along RA calculated from DR2 and DR3 positions.'),
        ('ob_pmdec_prop', 'mas', 'Proper motion along dec calculated from DR2 and DR3 positions.')
    ]
    for col, unit, desc in information:
        for L2 in [False, True]:
            if L2:
                col = 'L2_' + col
                desc = desc + ' for Lagrange point L2'
            if col in tab.colnames:
                tab[col].unit = unit
                tab[col].description = desc
            if col + '_error' in tab.colnames:
                tab[col + '_error'].unit = unit
                tab[col + '_error'].description = 'Error of ' + desc
            if col + '_error_p' in tab.colnames:
                tab[col + '_error_p'].unit = unit
                tab[col + '_error_p'].description = 'Positive error of ' + desc
            if col + '_error_m' in tab.colnames:
                tab[col + '_error_m'].unit = unit
                tab[col + '_error_m'].description = 'Negative Error of ' + desc


def main():
    tt1 = time.time()
    if not os.path.isdir('Results'):
        os.mkdir('Results')

    # load and filter Raw Candidates
    good_raw_cands = raw_data.main()
    # determine stellar mass based on their color and magnitude
    mass.determine_mass(good_raw_cands)
    # replace masked values
    good_raw_cands = raw_data.fill_value(good_raw_cands)

    # add Einstein radius to the table
    determine_einstein_radii(good_raw_cands)
    # add aproximated parameters to the table
    good_raw_cands = approx_filter(good_raw_cands)

    # do precise calculations
    table_out = calc(good_raw_cands)
    # filter events according to lensing effects
    table_out = filter_events(table_out)
    # add description and unit information
    add_description(table_out)

    tt2 = time.time()
    logger.info('Duration: %im:%fs', (tt2 - tt1) // 60, (tt2 - tt1) % 60)
    logger.info('Number of events: %d', len(table_out))
    logger.info('-------------------------')
    logger.info('DONE')
