# plot_it.py v0.1.1
# written by Olof Sjödin <olsj@kth.se> 2024-05-06

import argparse
import matplotlib.pyplot as plt
import numpy as np

def main():
    parser = argparse.ArgumentParser(description="Program to quickly plot from csv files.")
    parser.add_argument(
        "csv_filename", type=str, help="The csv file which we want to plot"
    )

    parser.add_argument(
        "--csv-delimiter", type=str, help="The CSV delimiter. Default: ','", default=","
    )

    parser.add_argument(
        "--x", type=int, help="The column number which we want to have on the x-axis. Default: 1", default=1
    )

    parser.add_argument(
        "--x-label", type=str, help="The label on the x-axis. Default: None"
    )

    parser.add_argument(
        "--x-lim", type=float, nargs=2, help="Minimum and maximum limits. Default: [min(x), max(x)]"
    )

    parser.add_argument(
        "--x-num-ticks", type=float, default=10
    )

    parser.add_argument(
        "--y", type=int, nargs="+", help="The column number which we want to have on the y-axis. Default: Everything but column x.",
    )

    parser.add_argument(
        "--y-label", type=str, help="The label on the x-axis. Default: None"
    )

    parser.add_argument(
        "--y-lim", type=float, nargs=2, help="Minimum and maximum limits. Default: [min(y), max(y)]"
    )

    parser.add_argument(
        "--y-num-ticks", type=float, default=10
    )

    parser.add_argument(
        "--legend", type=str, nargs="+", default=None
    )

    parser.add_argument(
    	"--multiply", nargs=2, type=str, metavar=('column', 'multipl_factor'), action='append', default=[]
    )

    parser.add_argument(
    	"--invert", nargs=1, type=int, metavar='column', action='append', default=[]
    )

    parser.add_argument(
        "--title", type=str, default=None
    )

    parser.add_argument(
        "--save", type=str, default=None
    )

    parser.add_argument(
        "--dont-show", action="store_true", default=False
    )

    args = parser.parse_args()
    data_mx = np.genfromtxt(args.csv_filename, delimiter=args.csv_delimiter)

    for col in args.invert:
        col=col[0]
        data_mx[:, col-1] = 1/data_mx[:, col-1]

    for col, fac in args.multiply:
        data_mx[:, int(col)-1] = float(fac) * data_mx[:, int(col)-1]

    x = data_mx[:, args.x-1]
    data_mx_excl_x = np.delete(data_mx, args.x-1, 1)
    if args.y is not None:
        y = data_mx_excl_x[:, np.array(args.y)-1]
    else:
        y = data_mx_excl_x

    fig, ax = plt.subplots()
    if args.legend is not None:
        for (yp, legend) in y.T, args.legend:
            ax.plot(x, yp, label=legend)
    else:
        for yp in y.T:
            ax.plot(x, yp)

    x_min = np.min(x) if args.x_lim is None else args.x_lim[0]
    x_max = np.max(x) if args.x_lim is None else args.x_lim[1]

    y_min = np.min(y) if args.y_lim is None else args.y_lim[0]
    y_max = np.max(y) if args.y_lim is None else args.y_lim[1]

    ax.set(
        xlim=(x_min, x_max), xticks=np.arange(x_min, x_max, (x_max-x_min)/args.x_num_ticks),
        ylim=(y_min, y_max), yticks=np.arange(y_min, y_max, (y_max-y_min)/args.y_num_ticks)
    )

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


if __name__ == "__main__":
    main()
