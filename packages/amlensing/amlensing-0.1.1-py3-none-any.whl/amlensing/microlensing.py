import numpy as np
from astropy.table import Table
from scipy.stats import truncnorm

from amlensing import config

const_Einsteinradius = 2.854062733172987  # (mas/Msun)**0.5


def quantile(array_e):
    """
    return median and 1-sigma errors of asymmetric samples
    """
    percentiles = np.percentile(array_e, [15.866, 50, 84.134])
    return percentiles[1], percentiles[2] - percentiles[1], percentiles[0] - percentiles[1]


def einstein_radius(tab):
    """
    calculate the Einstein radius in unit mas from Mass in SolarMasses,
    and parallax in mas
    ThetaE[rad] = sqrt(4GM/c^2)*sqrt(d_LS/(d_L*d_S))
    ThetaE[mas] = const *sqrt(M/M_sun *((Lensparallax[mas]-Objparallax[mas]))
    const = 180/pi * 3.6e6 *sqrt(4GM_sun / (c^2* 1pc[m]*1000))
    """
    ob_parallax = np.where(tab['ob_parallax'] > 0, tab['ob_parallax'], 0)
    ThetaE = const_Einsteinradius * \
        np.sqrt(tab['mass'] * (tab['parallax'] - ob_parallax))
    ThetaE_error = ThetaE * 0.5 * np.sqrt(
        np.square(tab['mass_error'] / tab['mass'])
        + (np.square(tab['parallax_error']) + np.square(tab['ob_parallax_error']))
        / np.square(tab['parallax'] - tab['ob_parallax']))
    return ThetaE, ThetaE_error


def calc_shift(dist, ThetaE):
    '''
    calculate the expected shift of the centeroid
    expect dist and ThetaE in the same unit
    return shift in the same unit as dist and ThetaE
    '''
    u = dist / ThetaE
    # maximum shift at u = sqrt(2)
    u = np.maximum(u, np.sqrt(2))
    shift = u / (u ** 2 + 2) * ThetaE

    return shift


def calc_shift_error(dist, ThetaE, dist_error, ThetaE_error):
    shift = calc_shift(dist, ThetaE)

    # calculate error propatation
    shift_error = shift**2 * np.sqrt(
        np.square((2 / dist**2 - 1 / ThetaE**2) * dist_error) +
        np.square(2 * dist / ThetaE**3 * ThetaE_error))
    return shift, shift_error


def calc_shift_plus(dist, ThetaE):
    '''
    calculate the expected shift of the bright image
    expect dist and ThetaE in the same unit
    return shift in the same unit as dist and ThetaE
    '''
    shift_plus = (np.sqrt(dist**2 + 4 * ThetaE**2) - dist) / 2
    return shift_plus


def calc_shift_plus_error(dist, ThetaE, dist_error, ThetaE_error):
    shift_plus = calc_shift_plus(dist, ThetaE)

    # calculate error propatation
    shift_plus_error = np.sqrt(
        np.square((dist / np.sqrt(dist**2 + 4 * ThetaE**2) - 1) / 2 * dist_error) +
        np.square(4 * ThetaE / 2 / np.sqrt(dist**2 + 4 * ThetaE**2) * ThetaE_error))
    return shift_plus, shift_plus_error


def calc_shift_lum(dist, ThetaE, FL_FS=0):
    '''
    calculate the expected shift of combined center of light
    including luminous lens effects
    expect dist and ThetaE in the same unit
    return shift in the same unit as dist and ThetaE
    if dist_error != 0 also the error is propagated
    '''
    u = dist / ThetaE
    # maximum shift at u = sqrt(2) / (1+FL_FS)
    u = np.maximum(u, np.sqrt(2) / (1 + FL_FS))

    shift_lum = u * ThetaE / (1 + FL_FS) \
        * (1 + FL_FS * (u**2 + 3 - u * np.sqrt(u**2 + 4))) \
        / (u**2 + 2 + FL_FS * u * np.sqrt(u**2 + 4))
    return shift_lum


def calc_shift_lum_error(dist, ThetaE, dist_error, ThetaE_error, FL_FS=0):
    u = dist / ThetaE
    shift_lum = calc_shift_lum(dist, ThetaE, FL_FS)

    # calculate error propatation
    u_error = u * np.sqrt(np.square(dist_error / dist) +
                          np.square(ThetaE_error / ThetaE))
    # d shift_lum / du
    nn = (ThetaE * FL_FS * u * (-u**2 / np.sqrt(u**2 + 4)
                                - np.sqrt(u**2 + 4) + 2 * u)) \
        / ((FL_FS + 1) * (FL_FS * np.sqrt(u**2 + 4) * u + u**2 + 2)) \
        + (ThetaE * (FL_FS * (u**2 - np.sqrt(u**2 + 4) * u + 3) + 1)) \
        / ((FL_FS + 1) * (FL_FS * np.sqrt(u**2 + 4) * u + u**2 + 2)) \
        - (ThetaE * u * ((FL_FS * u**2) / np.sqrt(u**2 + 4) + FL_FS
                         * np.sqrt(u**2 + 4) + 2 * u)
           * (FL_FS * (u**2 - np.sqrt(u**2 + 4) * u + 3) + 1)) \
        / (FL_FS + 1) / np.square(FL_FS * np.sqrt(u**2 + 4) * u + u**2 + 2)

    shift_lum_error = np.sqrt(nn**2 * u_error**2 +
                              shift_lum**2 / ThetaE**2 * ThetaE_error**2)
    return shift_lum, shift_lum_error


def calc_magnification(dist, ThetaE, FL_FS):
    '''
    calculate the expected magnification including luminous lens effects
    expect dist and ThetaE in the same unit
    return shift in the same unit as dist and ThetaE
    if dist_error != 0 also the error is propagated
    '''
    u = dist / ThetaE
    # flux ratio with dark lens
    A = (u**2 + 2) / (u * np.sqrt(u**2 + 4))
    # magnification with luminous lens
    magnification = 5 * np.log((FL_FS + A) / (FL_FS + 1)) / np.log(100)
    return magnification


def calc_magnification_error(dist, ThetaE, dist_error, ThetaE_error, FL_FS):
    u = dist / ThetaE
    A = (u**2 + 2) / (u * np.sqrt(u**2 + 4))
    magnification = calc_magnification(dist, ThetaE, FL_FS)

    # calculate error
    u_error = u * np.sqrt(np.square(dist_error / dist) +
                          np.square(ThetaE_error / ThetaE))
    '''
    (u^2 + 2)/(u*sqrt(u^2+4))'
    = ((u^2 + 2)' (u*sqrt(u^2+4)) - (u^2 + 2) (u*sqrt(u^2+4))')
        /(u^2*(u^2+4))
    = (2*u^2 - (u^2+2)* (1+ u^2/u^2+4 )/(u^2*sqrt(...))
    = ((u^2-2)* (u^2+4) - (u^2+2)*u^2)/(u^2*sqrt...^3)
    = -8/(u^2*sqrt(u^2+4)^3)
    '''
    A_error = 8 / (u**2 * pow(u**2 + 4, 3/2)) * u_error
    magnification_error = 5 / np.log(100) * A_error / (FL_FS + A)
    return magnification, magnification_error


def add_lensing_effects(tab, gaia=False):
    """
    calculate the microlensing effect for an given distance and Einsteinradius
     both in mas
    It return the distance in values of the Einstein radius, the
    shift in mas, the magnification in delta mag as well as their errors in
    the same units.
    if gaia: use L2 distance and Epoch, and include L2 in table discription
    """
    error_percentile = config['general'].getboolean('use_sampling')
    name_prefix = 'L2_' if gaia else ''

    # get distance
    dist = tab[name_prefix + 'dist']
    dist_error = tab[name_prefix + 'dist_error']
    # einstein angular radius
    ThetaE = tab['ThetaE']
    ThetaE_error = tab['ThetaE_error']
    # determine Flux Ratio
    diff_g_mag = tab['ob_phot_g_mean_mag'] - tab['phot_g_mean_mag']
    diff_g_mag[diff_g_mag > 50] = 50  # avoid overflow
    # TODO: filter out those who don't have G mag
    FL_FS = pow(100.0, diff_g_mag / 5)

    def var_error(var, error, name):
        return ((var, name), (error, f'{name}_error'))

    def var_error_pm(var, error, error_p, error_m, name):
        return ((var, name),
                (error, f'{name}_error'),
                (error_p, f'{name}_error_p'),
                (error_m, f'{name}_error_m'))

    # determine normed impact parameter u
    u = dist / ThetaE
    sample_size = config['general'].getint('sample_size')
    if error_percentile:
        dist_pdf, dist_pdf_error, dist_pdf_error_p, dist_pdf_error_m, \
            ThetaE_pdf, ThetaE_pdf_error, ThetaE_pdf_error_p, ThetaE_pdf_error_m, \
            u, u_error, u_error_p, u_error_m, \
            shift, shift_error, shift_error_p, shift_error_m, \
            shift_plus, shift_plus_error, shift_plus_error_p, shift_plus_error_m, \
            shift_lum, shift_lum_error, shift_lum_error_p, shift_lum_error_m, \
            mag, mag_error, mag_error_p, mag_error_m = \
            (np.zeros(len(tab)) for _ in range(28))

        for i, item in enumerate(tab):
            source_ids = item['source_id']
            ob_source_ids = item['ob_source_id']

            dist_sample = truncnorm.rvs(-dist[i] / dist_error[i], np.infty,
                                        dist[i], dist_error[i], sample_size).T
            dist_pdf[i], dist_pdf_error_p[i], dist_pdf_error_m[i] = quantile(dist_sample)
            ThetaE_sample = truncnorm.rvs(-ThetaE[i] / ThetaE_error[i], np.infty,
                                          ThetaE[i], ThetaE_error[i], sample_size).T
            ThetaE_pdf[i], ThetaE_pdf_error_p[i], ThetaE_pdf_error_m[i] = quantile(ThetaE_sample)

            u_e = dist_sample / ThetaE_sample
            u[i], u_error_p[i], u_error_m[i] = quantile(u_e)

            shift_e = calc_shift(dist_sample, ThetaE_sample)
            shift[i], shift_error_p[i], shift_error_m[i] = quantile(shift_e)

            shift_plus_e = calc_shift_plus(dist_sample, ThetaE_sample)
            shift_plus[i], shift_plus_error_p[i], shift_plus_error_m[i] = quantile(shift_plus_e)

            shift_lum_e = calc_shift_lum(dist_sample, ThetaE_sample, FL_FS[i])
            shift_lum[i], shift_lum_error_p[i], shift_lum_error_m[i] = quantile(shift_lum_e)

            mag_e = calc_magnification(dist_sample, ThetaE_sample, FL_FS[i])
            mag[i], mag_error_p[i], mag_error_m[i] = quantile(mag_e)

            if (len(dist_sample) > 0 and gaia is False and config['general'].getboolean('export_samples')):
                names = ['dist', 'ThetaE', 'u', 'shift', 'shift_plus', 'shift_lum']
                # for i in range(len(dist_sample)):
                # print(len(dist_sample), dist_sample.shape, source_ids, ob_source_ids)
                single_sample_table = Table([
                    dist_sample,
                    ThetaE_sample,
                    u_e,
                    shift_e,
                    shift_plus_e,
                    shift_lum_e], names=names)
                fn = f"Results/samples/{source_ids}.{ob_source_ids}.sample.csv"
                single_sample_table.write(fn, format="ascii.csv", overwrite=True)

        ThetaE_pdf_error = np.maximum(ThetaE_pdf_error_p, -ThetaE_pdf_error_m)
        dist_pdf_error = np.maximum(dist_pdf_error_p, -dist_pdf_error_m)
        u_error = np.maximum(u_error_p, -u_error_m)
        shift_error = np.maximum(shift_error_p, -shift_error_m)
        shift_plus_error = np.maximum(shift_plus_error_p, -shift_plus_error_m)
        shift_lum_error = np.maximum(shift_lum_error_p, -shift_lum_error_m)
        mag_error = np.maximum(mag_error_p, -mag_error_m)

        variables = [
            *var_error_pm(dist_pdf, dist_pdf_error, dist_pdf_error_p, dist_pdf_error_m, 'dist_truncated'),
            *var_error_pm(ThetaE_pdf, ThetaE_pdf_error, ThetaE_pdf_error_p, ThetaE_pdf_error_m, 'ThetaE_truncated'),
            *var_error_pm(u, u_error, u_error_p, u_error_m, 'u'),
            *var_error_pm(shift, shift_error, shift_error_p, shift_error_m, 'shift'),
            *var_error_pm(shift_plus, shift_plus_error, shift_plus_error_p, shift_plus_error_m, 'shift_plus'),
            *var_error_pm(shift_lum, shift_lum_error, shift_lum_error_p, shift_lum_error_m, 'shift_lum'),
            *var_error_pm(mag, mag_error, mag_error_p, mag_error_m, 'magnification'),
        ]
    else:
        u_error = u * np.sqrt((dist_error/dist)**2 + (ThetaE_error/ThetaE)**2)

        # calculate effects
        shift, shift_error = calc_shift_error(dist, ThetaE, dist_error, ThetaE_error)
        shift_plus, shift_plus_error = calc_shift_plus_error(dist, ThetaE, dist_error, ThetaE_error)
        shift_lum, shift_lum_error = calc_shift_lum_error(dist, ThetaE, dist_error, ThetaE_error, FL_FS)
        mag, mag_error = calc_magnification_error(dist, ThetaE, dist_error, ThetaE_error, FL_FS)

        variables = [
            *var_error(u, u_error, 'u'),
            *var_error(shift, shift_error, 'shift'),
            *var_error(shift_plus, shift_plus_error, 'shift_plus'),
            *var_error(shift_lum, shift_lum_error, 'shift_lum'),
            *var_error(mag, mag_error, 'magnification'),
        ]

    theta_min = 1e-3
    # TODO: look into this, is this right?
    shift_trunc = np.copy(shift)
    shift_trunc[shift <= theta_min] = np.nan
    tab['t_aml'] = 2 * u * tab['t_E'] * np.sqrt(shift_trunc**2 / theta_min**2 - 1)
    tab['t_thres'] = u * tab['t_E'] / np.sqrt(shift_trunc**2 / theta_min**2 - 1)

    # approximated u0, when the exact value is not yet known
    u0 = tab['approx_dist'] / tab['ThetaE']
    u02tE2 = u0**2 * tab['t_E']**2
    t1 = config['epoch'].getfloat('epoch_start') - tab['approx_tca']
    t2 = config['epoch'].getfloat('epoch_end') - tab['approx_tca']
    u12tE2 = u02tE2 + t1**2
    u22tE2 = u02tE2 + t2**2
    # non-linearity of the astrometric trajectory of centroid
    tab['nonlinearity'] = shift * (1 - (u02tE2 + t1 * t2) / np.sqrt(u12tE2 * u22tE2))

    for var, name in variables:
        tab.add_column(var, name=name_prefix+name)
