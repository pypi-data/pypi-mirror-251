"""
Test that the version number exists and is valid.
"""
import packaging.version

import coopgt


def test_version_is_str():
    assert type(coopgt.__version__) is str


def test_version_is_valid():
    assert (
        type(packaging.version.parse(coopgt.__version__)) is packaging.version.Version
    )
