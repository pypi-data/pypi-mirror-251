import numpy as np
from numpy.polynomial.polynomial import polyval

from amlensing import logger


def determine_mass(tab):
    '''
    determine a approximated mass for the lens based on Gaia data
    '''
    # if the data contains mass information, skip this
    if 'mass' in tab.colnames:
        logger.info('Data already provides mass, skip calculating estimated mass.')
        return

    logger.info('Determine approximate Mass')
    """
    estimate the mass of an lense from photometric properties
    classify star in White Dwarfs, Red Giant and Main Sequence
    For MS determine approximatly Mass using an rough M-G_abs relation.
    """
    # Absolut Bp & G magnitude
    no_bprp = np.isnan(tab['phot_bp_mean_mag']) | np.isnan(tab['phot_rp_mean_mag'])
    B_abs = tab['phot_bp_mean_mag'].value + 5 * np.log10(tab['parallax'].value / 100)
    G_abs = tab['phot_g_mean_mag'].value + 5 * np.log10(tab['parallax'].value / 100)
    # G - Rp color
    g_rp = tab['phot_g_mean_mag'].value - tab['phot_rp_mean_mag'].value

    # Mass - G_abs function
    popt = [7.8623e-03, -2.9089e-01, 1.1825e+00, -3.0118e-01, 1.8895e+00]
    mass = np.exp((popt[0] * G_abs + popt[1]) * G_abs + popt[2])
    mass[G_abs > 8.85] = np.exp(popt[3] * G_abs[G_abs > 8.85] + popt[4])

    # set BD to 0.07 Msun
    mass = np.maximum(mass, 0.07)
    mass_err = 0.1 * mass
    mass_err[mass < 0.1] = 0.03

    star_type = np.repeat('MS', len(tab))
    star_type[mass == 0.07] = 'BD'

    # Define WD
    WD_Terms = [7.4, 4.5, 4]
    WD = (polyval(g_rp, WD_Terms) < B_abs) & (~no_bprp)
    mass[WD] = 0.65
    mass_err[WD] = 0.15
    star_type[WD] = 'WD'
    # Define RG
    RG_Terms = [-20, 70, -50.]
    RG = (polyval(g_rp, RG_Terms) > B_abs) & (~no_bprp)

    mass[RG] = 1
    mass_err[RG] = 0.5
    star_type[RG] = 'RG'

    tab['star_type'] = star_type
    tab['mass'] = mass
    tab['mass_error'] = mass_err
