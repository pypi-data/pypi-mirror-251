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
    width_value: float,
    lower_spec: float,
    higher_spec: float,
) -> Figure:
    """Plot a wafermap of the losses.

    Args:
        losses: Dictionary of losses.
        width_value: Width of the waveguide to analyze.
        lower_spec: Lower specification limit.
        higher_spec: Higher specification limit.
    """
    fig = plt.figure()

    radius = int(
        np.max(np.ceil(np.sqrt(np.sum(np.square([loss for loss in losses]), axis=1))))
    )
    # Create an array of random values for the heatmap
    data = np.zeros((2 * radius + 1, 2 * radius + 1))
    data = np.full((2 * radius + 1, 2 * radius + 1), np.nan)
    for (i, j), value in losses.items():
        data[j + radius, i + radius] = value

    # Create a figure and axis
    fig = plt.figure(figsize=(16, 6.8))
    ax1 = fig.add_subplot(121)
    plt.xlabel("Die X", fontsize=18)
    plt.ylabel("Die Y", fontsize=18)
    plt.title(
        f"Propagation loss waveguide width {width_value} [µm]", fontsize=18, pad=10
    )

    # Create a custom colormap going from green to red
    cmap = mcolors.LinearSegmentedColormap.from_list(
        "blue_yellow_red", ["blue", "yellow", "red"]
    )

    # Create the heatmap with the custom colormap

    extent = np.array([-radius - 0.5, radius + 0.5, -radius - 0.5, radius + 0.5])
    heatmap = ax1.imshow(data, cmap=cmap, extent=extent, vmin=0)

    # Create an ellipse (circle)
    ellipse = patches.Circle((0, 0), radius + 0.5, color="black", fill=False)

    # Add the ellipse to the plot
    ax1.add_artist(ellipse)

    # Calculate the position for the triangle at the bottom of the circle
    triangle_x = 0  # Centered with the circle
    triangle_y = -radius  # Aligned with the lowest part of the circle
    triangle_size = 0.5  # Smaller size

    # Create a small filled triangle at the bottom
    triangle = patches.Polygon(
        np.array(
            [
                [triangle_x, triangle_y],
                [triangle_x - triangle_size, triangle_y - triangle_size],
                [triangle_x + triangle_size, triangle_y - triangle_size],
            ]
        ),
        closed=True,
        facecolor="white",
        edgecolor="black",
    )

    # Add the triangle to the plot
    ax1.add_patch(triangle)

    # Set axis limits to ensure the circle and triangle are visible
    ax1.set_xlim(-radius - 1, radius + 1)
    ax1.set_ylim(-radius - 1, radius + 1)
    ax1.grid(which="both")
    ax1.set_xticks(np.arange(-radius - 0.5, radius + 0.5, 1))
    ax1.set_yticks(np.arange(-radius - 0.5, radius + 0.5, 1))
    ax1.set_xticklabels([""] * len(ax1.get_xticks()))
    ax1.set_yticklabels([""] * len(ax1.get_yticks()))

    # Add number annotations to the heatmap
    for i, j in losses:
        d = data[j + radius, i + radius]
        if ~np.isnan(d):
            # breakpoint()
            ax1.text(
                i,
                j,
                f"{d:.2f}\n({i},{j})",
                ha="center",
                va="center",
                color="white",
                weight="bold",
                fontsize=18,
            )

    # Add a colorbar to the heatmap
    cbar = plt.colorbar(heatmap)
    cbar.set_label("[dB/cm]", fontsize=18)
    cbar.ax.set_yticklabels(cbar.ax.get_yticklabels(), fontsize=18)

    # Create a figure and axis
    ax2 = fig.add_subplot(122)
    plt.xlabel("Die X", fontsize=18)
    plt.ylabel("Die Y", fontsize=18)
    plt.title(
        f"KGD width {width_value} [µm], low={lower_spec} high={higher_spec} [dB]",
        fontsize=18,
        pad=10,
    )
    # plt.close()

    # Create a custom colormap going from green to red
    cmap = mcolors.ListedColormap(["red", "green"])

    # Create the heatmap with the custom colormap

    extent = [-radius - 0.5, radius + 0.5, -radius - 0.5, radius + 0.5]
    heatmap = ax2.imshow(
        np.where(
            np.isnan(data),
            data,
            np.where(
                np.logical_and(data <= higher_spec, data >= lower_spec),
                1,
                0,
            ),
        ),
        cmap=cmap,
        extent=extent,
        vmin=0,
        vmax=1,
    )

    # Create an ellipse (circle)
    ellipse = patches.Circle((0, 0), radius + 0.5, color="black", fill=False)

    # Add the ellipse to the plot
    ax2.add_artist(ellipse)

    # Calculate the position for the triangle at the bottom of the circle
    triangle_x = 0  # Centered with the circle
    triangle_y = -radius  # Aligned with the lowest part of the circle
    triangle_size = 0.5  # Smaller size

    # Create a small filled triangle at the bottom
    triangle = patches.Polygon(
        np.array(
            [
                [triangle_x, triangle_y],
                [triangle_x - triangle_size, triangle_y - triangle_size],
                [triangle_x + triangle_size, triangle_y - triangle_size],
            ]
        ),
        closed=True,
        facecolor="white",
        edgecolor="black",
    )

    # Add the triangle to the plot
    ax2.add_patch(triangle)

    # Set axis limits to ensure the circle and triangle are visible
    ax2.set_xlim(-radius - 1, radius + 1)
    ax2.set_ylim(-radius - 1, radius + 1)
    ax2.grid(which="both")
    ax2.set_xticks(np.arange(-radius - 0.5, radius + 0.5, 1))
    ax2.set_yticks(np.arange(-radius - 0.5, radius + 0.5, 1))
    ax2.set_xticklabels(ax1.get_xticks(), fontsize=18)
    ax2.set_yticklabels(ax1.get_yticks(), fontsize=18)
    ax2.set_xticklabels([""] * len(ax2.get_xticks()))
    ax2.set_yticklabels([""] * len(ax2.get_yticks()))

    # Add number annotations to the heatmap
    for i, j in losses:
        d = data[j + radius, i + radius]
        if ~np.isnan(d):
            ax2.text(
                i,
                j,
                f"{d:.2f}\n({i},{j})",
                ha="center",
                va="center",
                color="white",
                weight="bold",
                fontsize=18,
            )

    # Add a colorbar to the heatmap
    cbar = plt.colorbar(heatmap, ticks=[0, 1])
    cbar.ax.set_yticklabels(cbar.ax.get_yticklabels(), fontsize=18)
    cbar.set_ticklabels(["Bad", "Good"])
    plt.close()

    return fig


def run(
    wafer_id: int,
    key: str = "width_um",
    value: float = 0.3,
    lower_spec: float = 0.3,
    higher_spec: float = 0.5,
    function_name: str = "die_loss_cutback",
) -> dict[str, Any]:
    """Returns propagation loss in dB/cm.

    Args:
        wafer_id: ID of the wafer to analyze.
        key: Key of the parameter to analyze.
        value: Value of the parameter to analyze.
        lower_spec: Lower specification limit.
        higher_spec: Higher specification limit.
        function_name: Name of the die function to analyze.
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
                analysis.parameters.get("key") == key
                and analysis.parameters.get("value") == value
                and analysis.analysis_function.name == function_name
            ):
                losses[(die.x, die.y)] = analysis.output["propagation_loss_dB_cm"]

    summary_plot = plot_wafermap(
        losses, value, lower_spec=lower_spec, higher_spec=higher_spec
    )
    return dict(
        output={"losses": [5, 5]},
        summary_plot=summary_plot,
        wafer_id=wafer_id,
    )


if __name__ == "__main__":
    d = run(2)
    print(d["output"]["losses"])
