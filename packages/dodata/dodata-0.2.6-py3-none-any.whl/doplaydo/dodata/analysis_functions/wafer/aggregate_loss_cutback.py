"""Aggregate analysis."""

from typing import Any
import matplotlib.colors as mcolors
import matplotlib.patches as patches
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.figure import Figure

import doplaydo.dodata as dd


def plot_wafermap(
    losses: dict[tuple[int, int], float],
    key: str,
    lower_spec: float,
    upper_spec: float,
    value: float | None = None,
    metric: str = "propagation_loss_dB_cm",
) -> Figure:
    """Plot a wafermap of the losses."""
    # Calculate the bounds and center of the data
    die_xs, die_ys = zip(*losses.keys())
    die_x_min, die_x_max = min(die_xs), max(die_xs)
    die_y_min, die_y_max = min(die_ys), max(die_ys)
    die_center_x, die_center_y = (
        (die_x_max + die_x_min) / 2,
        (die_y_max + die_y_min) / 2,
    )
    radius = max(die_x_max - die_x_min, die_y_max - die_y_min) / 2 + 0.5

    # Create the data array
    data = np.full((die_y_max - die_y_min + 1, die_x_max - die_x_min + 1), np.nan)
    for (i, j), v in losses.items():
        data[j - die_y_min, i - die_x_min] = v

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6.8))

    # First subplot: Heatmap
    ax1.set_xlabel("Die X", fontsize=18)
    ax1.set_ylabel("Die Y", fontsize=18)
    title = f"{metric} {key}={value}" if value else f"{metric}"
    ax1.set_title(title, fontsize=18, pad=10)

    cmap = plt.get_cmap("viridis")
    vmin, vmax = (
        min(v for v in losses.values() if not np.isnan(v)),
        max(losses.values()),
    )

    heatmap = ax1.imshow(
        data,
        cmap=cmap,
        extent=[die_x_min - 0.5, die_x_max + 0.5, die_y_min - 0.5, die_y_max + 0.5],
        origin="lower",
        vmin=vmin,
        vmax=vmax,
    )

    ellipse = patches.Circle(
        (die_center_x, die_center_y), radius, color="black", fill=False
    )
    ax1.add_artist(ellipse)
    ax1.set_xlim(die_x_min - 0.5, die_x_max + 0.5)
    ax1.set_ylim(die_y_min - 0.5, die_y_max + 0.5)

    for (i, j), v in losses.items():
        if not np.isnan(v):
            ax1.text(
                i,
                j,
                f"{v:.2f}",
                ha="center",
                va="center",
                color="black",
                weight="bold",
                fontsize=10,
            )

    plt.colorbar(heatmap, ax=ax1)

    # Second subplot: Binary map based on specifications
    binary_map = np.where(
        np.isnan(data),
        np.nan,
        np.where((data >= lower_spec) & (data <= upper_spec), 1, 0),
    )

    cmap_binary = mcolors.ListedColormap(["red", "green"])
    heatmap_binary = ax2.imshow(
        binary_map,
        cmap=cmap_binary,
        extent=[die_x_min - 0.5, die_x_max + 0.5, die_y_min - 0.5, die_y_max + 0.5],
        origin="lower",
        vmin=0,
        vmax=1,
    )

    ellipse2 = patches.Circle(
        (die_center_x, die_center_y), radius, color="black", fill=False
    )
    ax2.add_artist(ellipse2)
    ax2.set_xlim(die_x_min - 0.5, die_x_max + 0.5)
    ax2.set_ylim(die_y_min - 0.5, die_y_max + 0.5)

    for (i, j), v in losses.items():
        if not np.isnan(v):
            ax2.text(
                i,
                j,
                f"{v:.2f}",
                ha="center",
                va="center",
                color="black",
                weight="bold",
                fontsize=10,
            )

    ax2.set_xlabel("Die X", fontsize=18)
    ax2.set_ylabel("Die Y", fontsize=18)
    ax2.set_title('KGD "Pass/Fail"', fontsize=18, pad=10)
    plt.colorbar(heatmap_binary, ax=ax2, ticks=[0, 1]).set_ticklabels(
        ["Outside Spec", "Within Spec"]
    )

    return fig


def run(
    wafer_id: int,
    key: str = "width_um",
    value: float | None = None,
    lower_spec: float = 0.3,
    upper_spec: float = 0.5,
    function_name: str = "die_loss_cutback",
    metric: str = "propagation_loss_dB_cm",
) -> dict[str, Any]:
    """Returns wafer map of metric after function_name.

    Args:
        wafer_id: ID of the wafer to analyze.
        key: Key of the parameter to analyze.
        value: Value of the parameter to analyze.
        lower_spec: Lower specification limit.
        upper_spec: Upper specification limit.
        function_name: Name of the die function to analyze.
        metric: Metric to analyze.
    """
    device_datas = dd.get_data_by_query([dd.Wafer.id == wafer_id])

    if device_datas is None:
        raise ValueError(f"Wafer with {wafer_id} doesn't exist in the database.")

    dies = [data[0].die for data in device_datas]

    # Get individual die analysis results without duplicates
    die_ids = {die.id: die for die in dies}
    losses = {}

    for die in die_ids.values():
        losses[(die.x, die.y)] = np.nan
        for analysis in die.analysis:
            if (die.x, die.y) not in losses:
                losses[(die.x, die.y)] = np.nan
            if (
                value
                and analysis.parameters.get("key") == key
                and analysis.parameters.get("value") == value
                and analysis.analysis_function.name == function_name
            ):
                losses[(die.x, die.y)] = analysis.output[metric]

            if (
                analysis.parameters.get("key") == key
                and analysis.analysis_function.name == function_name
            ):
                losses[(die.x, die.y)] = analysis.output[metric]

    numeric_values = [
        value for value in losses.values() if isinstance(value, int | float)
    ]
    numeric_array = np.array(numeric_values)
    if np.any(np.isnan(numeric_array)):
        raise ValueError(
            f"No analysis with key={key!r} and value={value} and function_name={function_name!r} found."
        )

    summary_plot = plot_wafermap(
        losses,
        value=value,
        key=key,
        lower_spec=lower_spec,
        upper_spec=upper_spec,
        metric=metric,
    )
    return dict(
        output={"losses": [5, 5]},
        summary_plot=summary_plot,
        wafer_id=wafer_id,
    )


if __name__ == "__main__":
    d = run(466, key="components", metric="component_loss", function_name="cutback")
    print(d["output"]["losses"])
