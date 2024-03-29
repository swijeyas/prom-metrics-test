import os
os.environ["PROMETHEUS_MULTIPROC_DIR"] = "/tmp/metrics"

import glob
import logging
import pytest
import time
import unittest.mock as mock

logger = logging.getLogger(__name__)

pid = 1
def mock_pid():
    global pid
    return pid

class TestMetric:
    @pytest.mark.parametrize(
        "metrics", [
            [100, 200, 300],
            [3, 2, 1],
        ]
    )
    @mock.patch("os.getpid", mock_pid)
    def test_metric(self, metrics):
        import prom
        from prometheus_client.multiprocess import MultiProcessCollector
        from prometheus_client import CollectorRegistry

        global pid

        pids = [1, 2]

        for p in pids:
            pid = p
            pm = prom.Metric("abc", CollectorRegistry())
            for m in metrics:
                pm.update(m)
                time.sleep(0.1) # adding little delay to ensure timestamps are different
                logger.info(f"m1 ts: {pm.g._value._timestamp}")

        files = glob.glob(os.path.join(os.environ["PROMETHEUS_MULTIPROC_DIR"], '*.db'))
        logger.info("DB files:")
        logger.info(files)

        scraped_metrics = list(MultiProcessCollector.merge(files))
        logger.info("DB metrics:")
        logger.info(scraped_metrics)

        assert len(scraped_metrics) == 1
        assert scraped_metrics[0].samples[0].value == metrics[-1]

        for f in files:
            os.remove(f)
