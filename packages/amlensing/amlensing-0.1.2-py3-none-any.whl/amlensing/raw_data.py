import numpy as np
from astropy.table import Table
from amlensing import filter_pair, filter_lens, filter_bgs, config, logger


def fill_value(tab):
    """ Fill in missing data with default values

    See configuration file for default values
    If data does not have the column, then create one
    """
    all_columns = [
        'source_id', 'epoch', 'ra', 'ra_error', 'dec', 'dec_error',
        'pmra', 'pmra_error', 'pmdec', 'pmdec_error', 'parallax', 'parallax_error',
        'phot_g_mean_mag', 'phot_rp_mean_mag', 'phot_bp_mean_mag'
    ]
    all_columns += ['ob_' + c for c in all_columns]

    tab['discarded'] = False
    for colname in all_columns:
        if colname in config['mask_values']:
            mask_value = config['mask_values'].getfloat(colname)
            if colname not in tab.colnames:
                tab[colname] = mask_value
            else:
                tab[colname].fill_value = mask_value
        elif colname in tab.colnames:
            tab['discarded'] |= tab[colname].mask
            if sum(tab[colname].mask):
                logger.error('%d candidates discarded due to lacking of %s',
                             sum(tab[colname].mask), colname)

    tab.remove_rows(tab['discarded'])
    tab.remove_column('discarded')
    return tab.filled()


def load_raw_pairs():
    raw_cands_table = config['files']['raw_cands_table']
    logger.info(f'Load raw pairs from {raw_cands_table}')
    raw_cands = Table.read(raw_cands_table)

    # mask None values
    if 'roi' in raw_cands.colnames:
        raw_cands.remove_column("roi")
    # make sure the table data is masked, for convenience
    raw_cands = Table(raw_cands, masked=True, copy=False)
    for i in raw_cands.colnames:
        if i.endswith('source_id'):
            pass
        elif any(np.isnan(raw_cands[i].astype(float))):
            raw_cands[i].mask |= np.isnan(raw_cands[i].astype(float))
    return raw_cands


def apply_lens_filter(tab):
    logger.info('-------------------------')
    if not config['general'].getboolean('filter_lens'):
        logger.info('Not filtering lens objects')
        return

    logger.info('Filter lens objects')
    lens_ids, inverse = np.unique(tab['source_id'], return_inverse=True)
    filters = filter_lens.main(lens_ids)[inverse]

    if not config['record_filters'].getboolean('lens'):
        tab.remove_rows(np.where(~filters['filter_lens_all'])[0])
    else:
        tab.update(filters)


def apply_bgs_filter(tab):
    # TODO: whitelist/blacklist
    # TODO: add propagated pm if not filtering?
    logger.info('-------------------------')
    if not config['general'].getboolean('filter_bgs'):
        logger.info('Not filtering background sources')
        return

    logger.info('Filter background sources')
    bgs_ids, inverse = np.unique(tab['ob_source_id'], return_inverse=True)
    pm_prop, filters = filter_bgs.main(bgs_ids)
    filters = filters[inverse]

    # include DR2-DR3 propermotion
    tab['ob_pmra_prop'] = pm_prop[inverse]['pmra_prop']
    tab['ob_pmdec_prop'] = pm_prop[inverse]['pmra_prop']
    tab['ob_parallax_prop'] = pm_prop[inverse]['parallax_prop']

    if not config['record_filters'].getboolean('bgs'):
        tab.remove_rows(np.where(~filters['filter_bgs_all'])[0])
    else:
        tab.update(filters)


def apply_pair_filter(tab):
    # filter pairs based on the comparison between lens and source data
    # i.e exclude binary stars
    logger.info('-------------------------')
    logger.info('Filter lens-bgs pairs')
    # apply filters for event pairs (lens + bgs)
    filters = filter_pair.main(tab)
    if not config['record_filters'].getboolean('pair'):
        tab.remove_rows(np.where(~filters['filter_pair_all'])[0])
    else:
        tab.update(filters)


def main():
    """load the raw_cands table and apply all filters"""
    logger.info('Load RawData:')

    raw_cands = load_raw_pairs()
    apply_lens_filter(raw_cands)
    apply_bgs_filter(raw_cands)
    apply_pair_filter(raw_cands)

    logger.info('-------------------------')
    logger.info('Good raw cands: %d', len(raw_cands))
    logger.info('-------------------------')

    return raw_cands
