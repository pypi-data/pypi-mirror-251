import numpy as np
import astropy.constants as ac
import astropy.units as u


def approx_date_dist(tab):
    """Estimate data and distance between lens and source at closest approach.

    The epochs of lens and source can be different. This is different from original
    code base. The key point in the implementation is replace RA and dec with a pair
    of new variables, i.e., delta_ra_gen and delta_dec_gen. See the source code for
    details.
    """
    cd = np.cos(np.deg2rad(tab['dec']))
    delta_ra = (tab['ob_ra'] - tab['ra']) * cd * 3.6e6
    delta_dec = (tab['ob_dec'] - tab['dec']) * 3.6e6

    lens_epoch = tab['epoch']
    lens_pmra = tab['pmra']
    lens_pmdec = tab['pmdec']
    obj_epoch = tab['ob_epoch']
    obj_pmra = tab['ob_pmra'].copy()
    obj_pmdec = tab['ob_pmdec'].copy()

    # set DR2 displacement as guess if ob_pm not known
    if 'ob_pmra_prop' in tab.colnames:
        obj_pmra[obj_pmra == 0] = tab[obj_pmra == 0]['ob_pmra_prop']
        obj_pmdec[obj_pmdec == 0] = tab[obj_pmdec == 0]['ob_pmdec_prop']

    # corrections due to different epochs
    delta_ra_gen = delta_ra - obj_pmra * obj_epoch + lens_pmra * lens_epoch
    delta_dec_gen = delta_dec - obj_pmdec * obj_epoch + lens_pmdec * lens_epoch
    delta_pmra = obj_pmra - lens_pmra
    delta_pmdec = obj_pmdec - lens_pmdec
    delta_pmtot = np.sqrt(delta_pmdec * delta_pmdec + delta_pmra * delta_pmra)
    minDate = - (delta_ra_gen * delta_pmra + delta_dec_gen * delta_pmdec) / delta_pmtot ** 2
    minDist = np.abs(delta_ra_gen * delta_pmdec - delta_dec_gen * delta_pmra) / delta_pmtot

    return minDate, minDist


def apply(tab):
    """Calculate some lensing effects and append them to the candidate table

    Columns added:
        - t_E: Einstein time scale
        - approx_tca: epoch of the closest approach
        - approx_dist: angular distance of the closest approach
        - approx_shift: maximum centroid shift
        - ddt_timedelay: second derivative of Shapiro time delay
    """
    # Einstein time scale
    mu_rel = np.sqrt((tab['pmra']-tab['ob_pmra'])**2+(tab['pmdec']-tab['ob_pmdec'])**2)
    tE = tab['ThetaE'] / mu_rel
    tab['t_E'] = tE

    minDate, minDist = approx_date_dist(tab)
    tab['approx_tca'] = minDate
    tab['approx_dist'] = minDist

    # calculate approximated effect (see microlensing.py)
    shift_plus = (np.sqrt(tab['approx_dist']**2 + 4 * tab['ThetaE']**2) - tab['approx_dist'])/2
    tab['approx_shift'] = shift_plus

    # second derivative of time delay
    ddt_timedelay = - (4 * tab['mass'] * ac.GM_sun / ac.c**3 * (mu_rel / u.year)**2 / tab['approx_dist']**2).si.value
    tab['ddt_timedelay'] = ddt_timedelay
