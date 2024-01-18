"""Fits resistance from an IV curve."""
from typing import Any
import numpy as np
from matplotlib import pyplot as plt

import doplaydo.dodata as dd


def run(
    device_data_id: int, min_i: float | None = None, max_i: float | None = None
) -> dict[str, Any]:
    """Fits resistance from an IV curve.

    Args:
        device_data_id: id of the device data to analyze.
        min_i: minimum intensity. If None, the minimum intensity is the minimum of the data.
        max_i: maximum intensity. If None, the maximum intensity is the maximum of the data.
    """
    data = dd.get_data_by_id(device_data_id)

    if "i" not in data.columns:
        raise ValueError("Data does not have a i column.")

    if "v" not in data.columns:
        raise ValueError("Data does not have a v column.")

    i = data.i
    v = data.v

    min_i = min_i or np.min(i)
    max_i = max_i or np.max(i)

    i2 = i[(i > min_i) & (i < max_i)]
    v2 = v[(i > min_i) & (i < max_i)]
    i, v = i2, v2

    p = np.polyfit(i, v, deg=1)

    i_fit = np.linspace(min_i, max_i, 3)
    v_fit = np.polyval(p, i_fit)
    resistance = p[0]

    fig = plt.figure()
    plt.plot(i, v, label="iv", zorder=0)
    plt.plot(i_fit, v_fit, label="fit", zorder=1)
    plt.xlabel("I (A)")
    plt.ylabel("V (V)")
    plt.legend()
    plt.title(f"Resistance {resistance:.2f} Ohms")
    plt.close()

    return dict(
        output={
            "resistance": float(resistance),
        },
        summary_plot=fig,
        device_data_id=device_data_id,
    )


if __name__ == "__main__":
    d = run(79366)
    print(d["output"]["resistance"])
