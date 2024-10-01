import numpy as np
import sys
import pdal

import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import matplotlib.mlab as mlab

from io import BytesIO


def make_plot(array, filename):


    global expression
    global threshold

    figure_position = 1
    row = 1

    fig = plt.figure(figure_position, figsize=(6, 8.5), dpi=300)
    ax = fig.add_subplot(1, 1, row)
    n, bins, patches = ax.hist( array, 30,
                                density=0,
                                facecolor='grey',
                                alpha=0.75,
                                align='mid',
                                histtype='stepfilled',
                                linewidth=None)



    ax.set_ylabel('Count', size=10)
    ax.set_title(expression, size=10)
    ax.set_xlabel(f'Z - {threshold}', size=10)
    ax.get_xaxis().set_visible(True)
#       ax.set_yticklabels('')
#    ax.set_yticks((),)
    ax.set_xlim(min(min(array), threshold -1), max(max(array), threshold + 1))
    ax.set_ylim(min(n), max(n))
    plt.axvline(x = threshold, linewidth=4, color = 'b', label = f'{threshold}', linestyle="--")

    output = BytesIO()
    plt.savefig(output,format="PNG")

    with open(filename, 'wb') as o:
        o.write(output.getvalue())





data = sys.argv[1]

classification = sys.argv[2]
threshold = 948.305
expression = f"Classification == {classification}"
data = pdal.Reader(filename=data) | pdal.Filter.expression(expression=expression)

data.execute()

make_plot(data.arrays[0]['Z'], f"Classification-{classification}.png")

