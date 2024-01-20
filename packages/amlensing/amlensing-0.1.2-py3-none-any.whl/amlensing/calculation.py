import numpy as np
from tqdm import tqdm

from amlensing.find_closest import estimate_Closest_parallax, estimate_errors_parallax
from amlensing.microlensing import add_lensing_effects


def parallel(part, raw_cands):
    # loop over row to finde closest approach
    result_closest = np.array(list(map(
        estimate_Closest_parallax,
        tqdm(raw_cands, position=part, desc=f"#{part:02d}", leave=False)
    ))).reshape((len(raw_cands), 4))

    # add closest approach at earth to table
    raw_cands['TCA'] = result_closest[:, 0]
    raw_cands['dist'] = result_closest[:, 1]
    error_earth = estimate_errors_parallax(raw_cands)
    raw_cands['TCA_error'] = error_earth[0]
    raw_cands['dist_error'] = error_earth[1]

    # FIXME: hack to drop nans, find out why they are nan
    result_closest = result_closest[~np.isnan(raw_cands['ThetaE_error']) & ~np.isnan(raw_cands['dist_error'])]
    raw_cands.remove_rows(np.isnan(raw_cands['ThetaE_error']))
    raw_cands.remove_rows(np.isnan(raw_cands['dist_error']))

    # calculate effect
    add_lensing_effects(raw_cands)

    # add closest approach at L2 to table
    raw_cands['L2_TCA'] = result_closest[:, 2]
    raw_cands['L2_dist'] = result_closest[:, 3]
    error_L2 = estimate_errors_parallax(raw_cands, gaia=True)
    raw_cands['L2_TCA_error'] = error_L2[0]
    raw_cands['L2_dist_error'] = error_L2[1]

    # calculate effect at L2
    add_lensing_effects(raw_cands, gaia=True)

    return raw_cands
