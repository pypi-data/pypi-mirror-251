from __future__ import absolute_import

import logging

# support CurationService
try:
    from wells_data_pipeline_cores.services.curation.curation_service import (
        CurationService,
    )
except Exception as ex:
    logging.warning("Export CurationService error - %s", ex)
