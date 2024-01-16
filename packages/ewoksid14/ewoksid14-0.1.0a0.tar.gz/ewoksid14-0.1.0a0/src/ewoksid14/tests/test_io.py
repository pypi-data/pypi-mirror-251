import numpy
from ..tasks import io


def test_io_mca():
    mca = numpy.arange(6)
    mca_string = io.array_to_mcaformat_string(mca)
    expected = [
        "@A 0 1 2 3 4 5",
        "",
    ]
    assert mca_string.split("\n") == expected

    mca = numpy.arange(16)
    mca_string = io.array_to_mcaformat_string(mca)
    expected = [
        "@A 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15",
        "",
    ]
    assert mca_string.split("\n") == expected

    mca = numpy.arange(32)
    mca_string = io.array_to_mcaformat_string(mca)
    expected = [
        "@A 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15\\",
        " 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31",
        "",
    ]
    assert mca_string.split("\n") == expected

    mca = numpy.arange(33)
    mca_string = io.array_to_mcaformat_string(mca)
    expected = [
        "@A 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15\\",
        " 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31\\",
        " 32",
        "",
    ]
    assert mca_string.split("\n") == expected
