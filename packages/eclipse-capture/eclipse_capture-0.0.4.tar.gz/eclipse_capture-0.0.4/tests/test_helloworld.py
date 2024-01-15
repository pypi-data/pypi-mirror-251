import pytest
from eclipse_capture import EclipseCapture

def test_hello_world():
    capture = EclipseCapture()
    assert capture.hello_world() == "Hello World!"