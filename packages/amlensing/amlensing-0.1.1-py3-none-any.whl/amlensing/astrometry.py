import numpy as np
import astropy.units as u
from astropy.coordinates import get_sun
from astropy.time import Time

from amlensing import config


def cart2spher(cart):
    """Cartesian to spherical"""
    alpha = np.arctan2(cart[1], cart[0])
    delta = np.arcsin(cart[2] / np.linalg.norm(cart, axis=0))
    alpha[alpha < 0] += 2 * np.pi
    return np.rad2deg(alpha), np.rad2deg(delta)


def angular_separation(pos1, pos2):
    """returns the distance along a great circle between two points
    The distance is in degrees, and assume it's small angle.
    """
    # NOTE: don't use arccos(dot(pos1, pos2)), not accurate for small angles
    pos1norm = pos1 / np.linalg.norm(pos1, axis=0)
    pos2norm = pos2 / np.linalg.norm(pos2, axis=0)
    dist = np.linalg.norm(pos1norm - pos2norm, axis=0)
    angsep = 2 * np.arcsin(dist / 2)
    return np.rad2deg(angsep)


def epoch_prop(raDeg, decDeg, pmra, pmdec, timeGaia):
    """Calculate coordinate after specific epoch

    returns cartesian coordinates for an object with pos ra, dec
    and pm pmra after Gaia epoch.
    pmra has to have cos(dec) applied, position in deg prop.motion in mas
    the time unit is yours to choose.
    """
    ra, dec = np.deg2rad([raDeg, decDeg])
    sd, cd = np.sin(dec), np.cos(dec)
    sa, ca = np.sin(ra), np.cos(ra)
    # mas to rad
    pmra, pmdec = np.deg2rad([pmra, pmdec]) / 3.6e6
    pmtot = np.sqrt(pmra**2 + pmdec**2)

    dirA = pmra / pmtot
    dirD = pmdec / pmtot
    sinMot = np.sin(pmtot * timeGaia)
    cosMot = np.cos(pmtot * timeGaia)
    dest = np.array([
        -sd * ca * dirD * sinMot - sa * dirA * sinMot + cd * ca * cosMot,
        -sd * sa * dirD * sinMot + ca * dirA * sinMot + cd * sa * cosMot,
        +cd * dirD * sinMot + sd * cosMot])
    return dest


def parallax_correction(bary_coord, earth_coord, parallax):
    """ annual parallax corrected cartesian Coordinates

    Input:
        bary_coord is a near-unit vector
        earth_coord is in au (also near-unit vector)
        parallax in mas
    """
    parallax = parallax.reshape((1, *parallax.shape))
    geo_coord = bary_coord + earth_coord * np.deg2rad(parallax / 3.6e6)
    return geo_coord


def epoch_prop_px(ra, dec, pmra, pmdec, parallax, t, t_ep,
                  earth_coord=None, gaia=False):
    """Calculate coordinate after specific epoch with parallax correction

    Input:
        astrometric info at epoch t_ep
        ra, dec: in degree
        pmra, pmdec: in mas/yr
        parallax: in mas

    Return:
        Cartesian coordinates of unit vector at epoch t
    """
    bary_coord = epoch_prop(ra, dec, pmra, pmdec, t - t_ep)
    if parallax >= config['general'].getfloat('zeropoint'):
        if earth_coord is None:
            earth_coord = pos_sun(t)
        if gaia is True:
            geo_coord = parallax_correction(bary_coord, earth_coord, parallax * 1.01)
        else:
            geo_coord = parallax_correction(bary_coord, earth_coord, parallax)
        return geo_coord
    else:
        return bary_coord


def pos_sun(t):
    """earth positions in AU at time t in Julian years"""
    t = np.array(t)
    pos = np.zeros((3, *t.shape))
    # return 0 for epoch outside 1900-2100, pyerfa will issue warnings
    # thus, neglect parallax effect for very ancient or future time
    valid = (t > 1900) & (t < 2100)
    # specifying TDB time scale is only to suppress the pyerfa warnings
    # the difference between TDB and default TT is negligible here
    pos[:, valid] = get_sun(Time(
        t[valid], format='jyear', scale='tdb'
    )).cartesian.xyz.to(u.au).value
    return pos


# time points every week
epoch_start = config['epoch'].getfloat('epoch_start')
epoch_end = config['epoch'].getfloat('epoch_end')
epoch_predef = np.arange(epoch_start - 10, epoch_end + 10, 1 / 52)
pos_sun_predef = pos_sun(epoch_predef)
