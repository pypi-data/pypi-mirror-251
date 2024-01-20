import numpy as np
from scipy import optimize

from amlensing.astrometry import epoch_prop_px, angular_separation, \
    pos_sun, cart2spher, parallax_correction, epoch_predef, pos_sun_predef


def estimate_Closest_parallax(row):
    data1 = estimate_Closest_parallax_gaia(row, gaia=False)
    data2 = estimate_Closest_parallax_gaia(row, gaia=True)
    return data1 + data2


def estimate_Closest_parallax_gaia(row, gaia=False):
    """
    units see docs/INPUT.md
    """
    # Define distance function with and with out parallax

    lens_ra = row['ra']
    lens_dec = row['dec']
    lens_pmra = row['pmra']
    lens_pmdec = row['pmdec']
    lens_parallax = row['parallax']
    lens_epoch = row['epoch']

    obj_ra = row['ob_ra']
    obj_dec = row['ob_dec']
    obj_epoch = row['ob_epoch']

    # set DR2 displacement as guess if ob_pm not known
    if 'ob_pmra_prop' in row.colnames:
        obj_pmra = row['ob_pmra_prop']
        obj_pmdec = row['ob_pmdec_prop']
        obj_parallax = row['ob_parallax_prop']
    else:
        obj_pmra = row['ob_pmra']
        obj_pmdec = row['ob_pmdec']
        obj_parallax = row['ob_parallax']

    lens_astrometric_params = (lens_ra, lens_dec, lens_pmra, lens_pmdec, lens_parallax)
    obj_astrometric_params = (obj_ra, obj_dec, obj_pmra, obj_pmdec, obj_parallax)

    def dist2(t):
        return 3.6e6 * angular_separation(
            epoch_prop_px(*lens_astrometric_params, t, lens_epoch, gaia=gaia),
            epoch_prop_px(*obj_astrometric_params, t, obj_epoch, gaia=gaia))

    def dist_pre(i):
        return 3.6e6 * angular_separation(
            epoch_prop_px(*lens_astrometric_params, epoch_predef[i], lens_epoch,
                          earth_coord=pos_sun_predef.T[i], gaia=gaia),
            epoch_prop_px(*obj_astrometric_params, epoch_predef[i], obj_epoch,
                          earth_coord=pos_sun_predef.T[i], gaia=gaia))

    Mu_tot = np.sqrt((lens_pmra - obj_pmra)**2 + (lens_pmdec - obj_pmdec)**2)
    # finde minima limit to approx 1 week
    t_0 = row['approx_tca']
    tlim = max(2.0, (3 * lens_parallax) / Mu_tot)
    t_min = t_0 - tlim
    t_max = t_0 + tlim

    nn = np.where((epoch_predef > t_min) & (epoch_predef < t_max))[0]

    dist = list(map(dist_pre, nn))
    number_list = range(len(nn) - 2)
    a = list(filter(lambda x: dist[x+1] - dist[x] < 0
             and dist[x+1] - dist[x+2] < 0, number_list))

    # initialize a array to store the closest points
    # (in order to compare multiple minima)
    closest_approaches = np.full((4), np.nan, dtype=[('time', float), ('dist', float)])
    # ensure there is at least one result, in case no minima found in the epoch span
    closest_approaches[0] = (t_0, dist2(t_0))
    # evaluate all minima
    for j in nn[a]:
        t1 = epoch_predef[j - (0 if gaia else 1)]
        t2 = epoch_predef[j + (2 if gaia else 3)]
        closest_time = optimize.golden(dist2, brack=(t1, t2), tol=1e-10)
        closest_approaches[-1] = closest_time, dist2(closest_time)
        closest_approaches.sort(axis=0, order='dist')

    return list(closest_approaches[0])


def tca_error(dt, da, dd, vas, vds, val, vdl, eda2, edd2, evas2, evds2, eval2, evdl2):
    '''
    minDate = (delta_ra * delta_pmra + delta_dec * delta_pmdec) / delta_pmtot ** 2
    '''
    dva = vas - val
    dvd = vds - vdl
    dv2 = dva**2 + dvd**2
    return np.sqrt(
        pow((dvd**2 - dva**2) * (da - val * dt) - 2 * dva * dvd * (dd - vdl * dt), 2) / dv2**4 * evas2 +
        pow((dvd**2 - dva**2) * (da + vas * dt) - 2 * dva * dvd * (dd + vds * dt), 2) / dv2**4 * eval2 +
        pow((dva**2 - dvd**2) * (dd - vdl * dt) - 2 * dva * dvd * (da - val * dt), 2) / dv2**4 * evds2 +
        pow((dva**2 - dvd**2) * (dd + vds * dt) - 2 * dva * dvd * (da + vas * dt), 2) / dv2**4 * evdl2 +
        pow(dva / dv2, 2) * eda2 + pow(dvd / dv2, 2) * edd2)


def dca_error(dt, da, dd, val, vas, vdl, vds, eda2, edd2, evas2, evds2, eval2, evdl2):
    '''
    minDist = abs(delta_ra * delta_pmdec - delta_dec * delta_pmra) / delta_pmtot
    '''
    dva = vas - val
    dvd = vds - vdl
    dv2 = dva**2 + dvd**2
    return np.sqrt(
        pow((dd - vdl * dt) * dvd**2 + (da - val * dt) * dvd * dva, 2) * evas2 / dv2**3 +
        pow((dd + vds * dt) * dvd**2 + (da + vas * dt) * dvd * dva, 2) * eval2 / dv2**3 +
        pow((da - val * dt) * dva**2 + (dd - vdl * dt) * dva * dvd, 2) * evds2 / dv2**3 +
        pow((da + vas * dt) * dva**2 + (dd + vds * dt) * dva * dvd, 2) * evdl2 / dv2**3 +
        eda2 * dvd**2 / dv2 + edd2 * dva**2 / dv2)


def estimate_errors_parallax(tab, delta_t_approx=1 / 26., gaia=False):
    '''
    _error estimation considering parallax also
    '''

    cd, sd = map(lambda x: x(np.deg2rad(tab["dec"])), (np.cos, np.sin))
    ca, sa = map(lambda x: x(np.deg2rad(tab["ra"])), (np.cos, np.sin))
    ocd, osd = map(lambda x: x(np.deg2rad(tab["ob_dec"])), (np.cos, np.sin))
    oca, osa = map(lambda x: x(np.deg2rad(tab["ob_ra"])), (np.cos, np.sin))

    obj_pmra, obj_pmdec, obj_parallax = \
        tab['ob_pmra', 'ob_pmdec', "ob_parallax"].copy().itercols()
    lens_pmra, lens_pmdec, lens_parallax = \
        tab["pmra", "pmdec", "parallax"].itercols()
    lens_parallax_err, lens_ra_err, lens_dec_err, lens_pmra_err, lens_pmdec_err = \
        tab["parallax_error", "ra_error", "dec_error", "pmra_error", "pmdec_error"].itercols()
    obj_parallax_err, obj_ra_err, obj_dec_err, obj_pmra_err, obj_pmdec_err = \
        tab["ob_parallax_error", "ob_ra_error", "ob_dec_error", "ob_pmra_error", "ob_pmdec_error"].itercols()

    # set DR2 displacement as guess if ob_pm not known
    # TODO: use mask instead of checking value == 0
    if 'ob_pmra_prop' in tab.colnames:
        obj_pmra[obj_pmra == 0] = tab[obj_pmra == 0]['ob_pmra_prop']
        obj_pmdec[obj_pmdec == 0] = tab[obj_pmdec == 0]['ob_pmdec_prop']
        obj_parallax[obj_parallax == 0] = tab[obj_parallax == 0]['ob_parallax_prop']

    # !!!! change to exact value
    if gaia:
        minDate = tab['L2_TCA']
    else:
        minDate = tab['TCA']
    obj_bary_coord = np.array([ocd * oca, ocd * osa, osd])
    lens_bary_coord = np.array([cd * ca, cd * sa, sd])
    earth_coord = pos_sun(minDate.data)

    lens_ra, lens_dec = cart2spher(
        parallax_correction(lens_bary_coord, earth_coord, lens_parallax * (gaia * .01 + 1)))
    obj_ra, obj_dec = cart2spher(
        parallax_correction(obj_bary_coord, earth_coord, obj_parallax * (gaia * .01 + 1)))

    delta_ra = (lens_ra - obj_ra) * cd * 3.6e6
    delta_dec = (lens_dec - obj_dec) * 3.6e6
    delta_epoch = tab['ob_epoch'] - tab['epoch']

    delta_ra_err2 = np.square(lens_ra_err) + np.square(obj_ra_err)
    delta_dec_err2 = np.square(lens_dec_err) + np.square(obj_dec_err)

    minDate_err = tca_error(
        delta_epoch, delta_ra, delta_dec, obj_pmra, obj_pmdec, lens_pmra, lens_pmdec,
        delta_ra_err2, delta_dec_err2,
        obj_pmra_err**2, obj_pmdec_err**2, lens_pmra_err**2, lens_pmdec_err**2)
    minDate_err2 = np.minimum(minDate_err, 0.25)

    earth_coord2 = pos_sun(minDate.data + minDate_err2.data)

    # relative parallax_error
    parallax_err = np.sqrt(np.square(lens_parallax_err)
                           + np.square(obj_parallax_err))

    # calculate position at silightly different parallax and epoch, unit = deg
    lens_ra2, lens_dec2 = cart2spher(parallax_correction(
        lens_bary_coord, earth_coord2, (lens_parallax - obj_parallax) * (gaia * .01 + 1)))
    lens_ra3, lens_dec3 = cart2spher(parallax_correction(
        lens_bary_coord, earth_coord, (lens_parallax - obj_parallax + parallax_err) *
        (gaia * .01 + 1)))

    dvra = (lens_ra - lens_ra2) * 3.6e6 * cd / minDate_err2 * minDate_err
    dvdec = (lens_dec - lens_dec2) * 3.6e6 / minDate_err2 * minDate_err
    dpx_ra = (lens_ra - lens_ra3) * 3.6e6 * cd
    dpx_dec = (lens_dec - lens_dec3) * 3.6e6

    delta_ra_err2 = delta_ra_err2 + dpx_ra**2 + dvra**2
    delta_dec_err2 = delta_dec_err2 + dpx_dec**2 + dvdec**2

    minDate_err = tca_error(
        delta_epoch, delta_ra, delta_dec, obj_pmra, obj_pmdec, lens_pmra, lens_pmdec,
        delta_ra_err2, delta_dec_err2,
        obj_pmra_err**2, obj_pmdec_err**2, lens_pmra_err**2, lens_pmdec_err**2)

    minDist_err = dca_error(
        delta_epoch, delta_ra, delta_dec, obj_pmra, obj_pmdec, lens_pmra, lens_pmdec,
        delta_ra_err2, delta_dec_err2,
        obj_pmra_err**2, obj_pmdec_err**2, lens_pmra_err**2, lens_pmdec_err**2)

    return minDate_err, minDist_err
