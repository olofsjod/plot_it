"""
.. plot_it.py v0.3
    written by Olof Sjödin <olsj@kth.se> 2025-07-17
"""

import argparse
import matplotlib.pyplot as plt
import numpy as np

from pathlib import Path


def main():
    parser = argparse.ArgumentParser(
        description="Program to quickly plot from csv files."
    )
    parser.add_argument(
        "csv_filename", type=str, nargs="+", help="The csv files which we want to plot"
    )

    parser.add_argument(
        "--csv-delimiter",
        type=str,
        help="The CSV delimiter. Default: Any consecutive whitespaces act as delimeter",
        default=None,
    )

    parser.add_argument(
        "--x",
        type=int,
        help="The column number which we want to have on the x-axis. Default: 1",
        default=1,
    )

    parser.add_argument(
        "--x-label", type=str, help="The label on the x-axis. Default: None"
    )

    parser.add_argument(
        "--x-lim",
        type=float,
        nargs=2,
        help="Minimum and maximum limits. Default: [min(x), max(x)]",
    )

    parser.add_argument("--x-num-ticks", type=float, default=10)

    parser.add_argument(
        "--y",
        type=int,
        nargs="+",
        help="The column number which we want to have on the y-axis. Default: Everything but column x.",
    )

    parser.add_argument(
        "--y-label", type=str, help="The label on the x-axis. Default: None"
    )

    parser.add_argument(
        "--y-lim",
        type=float,
        nargs=2,
        help="Minimum and maximum limits. Default: [min(y), max(y)]",
    )

    parser.add_argument("--y-num-ticks", type=float, default=10)

    parser.add_argument("--legend", type=str, nargs="+", default=None)

    parser.add_argument(
        "--multiply",
        nargs=2,
        type=str,
        metavar=("column", "multipl_factor"),
        action="append",
        default=[],
    )

    parser.add_argument(
        "--invert", nargs=1, type=int, metavar="column", action="append", default=[]
    )

    parser.add_argument("--title", type=str, default=None)

    parser.add_argument("--save", type=str, default=None)

    parser.add_argument("--dont-show", action="store_true", default=False)
    parser.add_argument("--show-legend", action="store_true", default=False)

    parser.add_argument(
        "--marker",
        type=str,
        default="",
        help="Default: None. Check https://matplotlib.org/stable/api/markers_api.html",
    )

    parser.add_argument(
        "--linestyle",
        type=str,
        default="-",
        help="Default: Solid line. Check https://matplotlib.org/stable/gallery/lines_bars_and_markers/linestyles.html",
    )

    parser.add_argument(
        "--skip-header", type=int, default=1, help="Default: 1. Skip the first line."
    )

    # Parses arguments from the user
    args = parser.parse_args()

    # Creates figure and plots data
    fig, ax = plt.subplots()

    # Create list of all minimas and maximas for each dataset
    x_min = []
    x_max = []

    y_min = []
    y_max = []

    if args.legend is not None:
        legends = args.legend.copy()
        legends.reverse()
    else:
        legends = None

    # Go through each dataset and retrieve the x and y information
    for fname in args.csv_filename:
        x, y = get_xy_data_from_file(
            fname,
            csv_delimiter=args.csv_delimiter,
            skip_header=args.skip_header,
            invert=args.invert,
            multiply=args.multiply,
            col_x=args.x,
            col_y=args.y,
        )

        x_min.append(np.min(x))
        x_max.append(np.max(x)) 

        y_min.append(np.min(y))
        y_max.append(np.max(y))

        if args.legend is not None:
            if len(args.legend) == len(args.csv_filename):
                legend = legends.pop()
            else:
                legend = args.legend
        else:
            legend = None

        plot_xy_data(
            fig,
            ax,
            x,
            y,
            legend=legend,
            linestyle=args.linestyle,
            marker=args.marker,
        )

    x_min = np.min(x_min) if args.x_lim is None else args.x_lim[0]
    x_max = np.max(x_max) if args.x_lim is None else args.x_lim[1]

    y_min = np.min(y_min) if args.y_lim is None else args.y_lim[0]
    y_max = np.max(y_max) if args.y_lim is None else args.y_lim[1]

    ax.set(
        xlim=(x_min, x_max),
        xticks=np.arange(x_min, x_max, (x_max - x_min) / args.x_num_ticks),
        ylim=(y_min, y_max),
        yticks=np.arange(y_min, y_max, (y_max - y_min) / args.y_num_ticks),
    )

    if args.show_legend:
        ax.legend()

    if args.x_label is not None:
        plt.xlabel(args.x_label)
    if args.y_label is not None:
        plt.ylabel(args.y_label)

    if args.title is not None:
        plt.title(args.title)

    if args.save is not None:
        fig.savefig(args.save)

    if not args.dont_show:
        plt.show()


def plot_xy_data(fig, ax, x, y, legend=None, linestyle="-", marker=""):
    if legend is not None:
        for yp in y.T:
            ax.plot(x, yp, label=legend, linestyle=linestyle, marker=marker)
    else:
        for yp in y.T:
            ax.plot(x, yp, linestyle=linestyle, marker=marker)


def get_xy_data_from_file(
    csv_filename: Path,
    csv_delimiter: str | None = None,
    skip_header: int = 1,
    invert: list[int] = [],
    multiply=[],
    col_x=1,
    col_y=None,
):
    """Reads the CSV file and extracts 2D plot information.

    :param csv_filename: Path to the CSV file
    :type csv_filename: str
    :param csv_delimiter: The delimiter separating the data values. Default: Any consecutive whitespaces act as delimeter
    :type csv_delimiter: str
    :param skip_header: The row number in the CSV file where the data starts.
    :type skip_header: int
    :param invert: Inverts specific column numbers, defaults to []
    :type invert: list, optional
    :param multiply: Multiply column number with a scalar, defaults to [] (no scalar multiplication)
    :type multiply: list, optional
    :param col_x: Specifies the column with the x-data, defaults to 1 (first column)
    :type col_x: int, optional
    :param col_y: Specifies the column with the y-data, defaults to None (i.e. all other columns are y-values)
    :type col_y: _type_, optional
    :return: returns the x and y data
    :rtype: _type_
    """
    data_mx = np.genfromtxt(
        csv_filename, delimiter=csv_delimiter, skip_header=skip_header
    )

    # Remove columns which only have NaN
    data_mx = data_mx[:, ~np.isnan(data_mx).any(axis=0)]

    # Inverts columns given by the user
    for col in invert:
        col = col[0]
        data_mx[:, col - 1] = 1 / data_mx[:, col - 1]

    for col, fac in multiply:
        data_mx[:, int(col) - 1] = float(fac) * data_mx[:, int(col) - 1]

    x = data_mx[:, col_x - 1]

    # Removes "x" column from data matrix
    data_mx_excl_x = np.delete(data_mx, col_x - 1, 1)

    if col_y is not None:
        y = data_mx_excl_x[:, np.array(col_y) - 1]
    else:
        y = data_mx_excl_x

    return x, y


if __name__ == "__main__":
    main()
