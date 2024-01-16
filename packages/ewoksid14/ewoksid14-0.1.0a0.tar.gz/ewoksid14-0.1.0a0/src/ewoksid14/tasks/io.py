import numbers
from typing import Sequence


def array_to_mcaformat_string(mca: Sequence[float]) -> str:
    mcastring = "@A"
    length = len(mca)
    nchan_per_line = 16
    if isinstance(mca[0], numbers.Integral):
        fmt = " %d"
    else:
        # fmt = " %.4f"
        fmt = " %.8g"
    for idx in range(0, length, nchan_per_line):
        if idx + nchan_per_line - 1 < length:
            for i in range(0, nchan_per_line):
                mcastring += fmt % mca[idx + i]
            if idx + nchan_per_line != length:
                mcastring += "\\"
        else:
            for i in range(idx, length):
                mcastring += fmt % mca[i]
        mcastring += "\n"
    return mcastring
