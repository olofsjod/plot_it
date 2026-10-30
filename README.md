# plot_it

A CLI tool that transforms data into plots.

## Install 

```
$ git clone https://github.com/olofsjod/plot_it.git
$ cd plot_it
$ pip install .
```

## Usage

```
$ plot_it --help
usage: plot_it [-h] [--csv-delimiter CSV_DELIMITER] [--x X] [--x-label X_LABEL]
               [--x-lim X_LIM X_LIM] [--x-num-ticks X_NUM_TICKS] [--y Y [Y ...]]
               [--y-label Y_LABEL] [--y-lim Y_LIM Y_LIM] [--y-num-ticks Y_NUM_TICKS]
               [--legend LEGEND [LEGEND ...]] [--multiply column multipl_factor]
               [--invert column] [--title TITLE] [--save SAVE] [--dont-show] [--show-legend]
               [--marker MARKER] [--linestyle LINESTYLE] [--skip-header SKIP_HEADER]
               csv_filename [csv_filename ...]

Program to quickly plot from csv files.

positional arguments:
  csv_filename          The csv files which we want to plot

options:
  -h, --help            show this help message and exit
  --csv-delimiter CSV_DELIMITER
                        The CSV delimiter. Default: Any consecutive whitespaces act as
                        delimeter
  --x X                 The column number which we want to have on the x-axis. Default: 1
  --x-label X_LABEL     The label on the x-axis. Default: None
  --x-lim X_LIM X_LIM   Minimum and maximum limits. Default: [min(x), max(x)]
  --x-num-ticks X_NUM_TICKS
  --y Y [Y ...]         The column number which we want to have on the y-axis. Default:
                        Everything but column x.
  --y-label Y_LABEL     The label on the x-axis. Default: None
  --y-lim Y_LIM Y_LIM   Minimum and maximum limits. Default: [min(y), max(y)]
  --y-num-ticks Y_NUM_TICKS
  --legend LEGEND [LEGEND ...]
  --multiply column multipl_factor
  --invert column
  --title TITLE
  --save SAVE
  --dont-show
  --show-legend
  --marker MARKER       Default: None. Check
                        https://matplotlib.org/stable/api/markers_api.html
  --linestyle LINESTYLE
                        Default: Solid line. Check https://matplotlib.org/stable/gallery/lin
                        es_bars_and_markers/linestyles.html
  --skip-header SKIP_HEADER
                        Default: 1. Skip the first line.

```

