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
    higher_spec: float,
    value: float | None = None,
    metric: str = "propagation_loss_dB_cm",
) -> Figure:
    """Plot a wafermap of the losses.

    Args:
        losses: Dictionary of losses.
        key: Key of the parameter to analyze.
        lower_spec: Lower specification limit.
        higher_spec: Higher specification limit.
        value: Value of the parameter to analyze.
        metric: Metric to analyze.
    """
    # Calculate radius and data array
    radius = int(
        np.max(np.ceil(np.sqrt(np.sum(np.square(list(losses.keys())), axis=1))))
    )
    data = np.full((2 * radius + 1, 2 * radius + 1), np.nan)
    for (i, j), v in losses.items():
        data[j + radius, i + radius] = v

    # Create a figure and axis
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6.8))

    # First subplot: Heatmap
    ax1.set_xlabel("Die X", fontsize=18)
    ax1.set_ylabel("Die Y", fontsize=18)
    title = f"{metric} {key}={value} loss" if value else f"{metric} loss"
    ax1.set_title(title, fontsize=18, pad=10)

    # Use 'viridis' colormap
    cmap = plt.get_cmap("viridis")
    vmin, vmax = (
        min(filter(lambda v: not np.isnan(v), losses.values())),
        max(losses.values()),
    )

    # Create the heatmap with 'viridis' colormap
    heatmap = ax1.imshow(
        data, cmap=cmap, extent=[-radius, radius, -radius, radius], vmin=vmin, vmax=vmax
    )

    # Add the ellipse (circle)
    ellipse = patches.Circle((0, 0), radius, color="black", fill=False)
    ax1.add_artist(ellipse)

    # Set axis limits to ensure the circle and triangle are visible
    ax1.set_xlim(-radius, radius)
    ax1.set_ylim(-radius, radius)

    # Add number annotations to the heatmap
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

    # Add a colorbar to the heatmap
    plt.colorbar(heatmap, ax=ax1)

    # Second subplot: Binary map based on specifications
    binary_map = np.where(
        np.isnan(data),
        np.nan,
        np.where((data >= lower_spec) & (data <= higher_spec), 1, 0),
    )

    cmap_binary = mcolors.ListedColormap(["red", "green"])
    heatmap_binary = ax2.imshow(
        binary_map,
        cmap=cmap_binary,
        extent=[-radius, radius, -radius, radius],
        vmin=0,
        vmax=1,
    )

    # Add the ellipse (circle)
    ellipse2 = patches.Circle((0, 0), radius, color="black", fill=False)
    ax2.add_artist(ellipse2)

    ax2.set_xlim(-radius, radius)
    ax2.set_ylim(-radius, radius)

    # Add number annotations to the heatmap
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

    # Set labels and title for ax2
    ax2.set_xlabel("Die X", fontsize=18)
    ax2.set_ylabel("Die Y", fontsize=18)
    ax2.set_title('KGD "Pass/Fail"', fontsize=18, pad=10)

    # Add a colorbar to the binary map
    cbar_binary = plt.colorbar(heatmap_binary, ax=ax2, ticks=[0, 1])
    cbar_binary.set_ticklabels(["Outside Spec", "Within Spec"])

    return fig


def run(
    wafer_id: int,
    key: str = "width_um",
    value: float | None = None,
    lower_spec: float = 0.3,
    higher_spec: float = 0.5,
    function_name: str = "die_loss_cutback",
    metric: str = "propagation_loss_dB_cm",
) -> dict[str, Any]:
    """Returns wafer map of metric after function_name.

    Args:
        wafer_id: ID of the wafer to analyze.
        key: Key of the parameter to analyze.
        value: Value of the parameter to analyze.
        lower_spec: Lower specification limit.
        higher_spec: Higher specification limit.
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
        higher_spec=higher_spec,
        metric=metric,
    )
    return dict(
        output={"losses": [5, 5]},
        summary_plot=summary_plot,
        wafer_id=wafer_id,
    )


if __name__ == "__main__":
    d = run(6, key="components", metric="component_loss", function_name="cutback")
    print(d["output"]["losses"])
