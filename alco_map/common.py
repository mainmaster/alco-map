from functools import partial

import backoff


alco_map_backoff = partial(
    backoff.on_exception,
    wait_gen=backoff.constant,
    exception=Exception,
    jitter=None,
)
