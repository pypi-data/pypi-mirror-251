import pytest
import os
from datetime import datetime
from pytz import timezone
import eclipse_capture as ec
from eclipse_capture import EclipseCaptureFile

def test_parse_file(datadir):
    capture_file = EclipseCaptureFile.load(os.path.join(datadir, "capture.csv"))
    assert capture_file

    assert capture_file.info.start == datetime(2024, 4, 8, 15, 13, 45, tzinfo=timezone("EST"))
    assert capture_file.info.end == datetime(2024, 4, 8, 15, 17, 45, tzinfo=timezone("EST"))

def test_bad_header(datadir):
    with pytest.raises(Exception) as e:
        capture_file = EclipseCaptureFile.load(os.path.join(datadir, "capture_bad_header.csv"))

    assert e.match("Invalid header")

