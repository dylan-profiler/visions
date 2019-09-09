from io import BytesIO
import base64
import matplotlib.pyplot as plt
import seaborn as sn

from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()


def _plot_histogram(series):
    plot = sn.distplot(series)
    plot.figure.subplots_adjust(left=0.15, right=0.95, top=0.9, bottom=0.1, wspace=0, hspace=0)
    return plot


def save_plot_to_str(plot):
    imgdata = BytesIO()
    plot.figure.savefig(imgdata, format='png')
    imgdata.seek(0)
    encoded = base64.b64encode(imgdata.getvalue())
    result_string = f"data:image/png;base64, {encoded.decode('utf-8')}"
    plt.close(plot.figure)
    return result_string


def histogram(series):
    plot = _plot_histogram(series)
    return save_plot_to_str(plot)
