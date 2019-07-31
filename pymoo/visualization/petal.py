import numpy as np

from pymoo.docs import parse_doc_string
from pymoo.model.plot import Plot
from pymoo.operators.default_operators import set_if_none
from pymoo.visualization.util import get_circle_points, plot_axes_lines, \
    plot_axis_labels, plot_circle, plot_polygon, parse_bounds, normalize, equal_axis, no_ticks


class PetalDiagram(Plot):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if "bounds" not in kwargs:
            raise Exception("Boundaries must be provided for Petal Width. Otherwise, no trade-offs can be calculated.")

        set_if_none(self.axis_style, "color", "black")
        set_if_none(self.axis_style, "linewidth", 2)
        set_if_none(self.axis_style, "alpha", 0.5)

    def _plot(self, ax, F):

        # equal axis length and no ticks
        equal_axis(ax)
        no_ticks(ax)

        V = get_circle_points(len(F))

        # sections to plot
        sections = np.linspace(0, 2 * np.pi, self.n_dim + 1)

        t = [(sections[i] + sections[i + 1]) / 2 for i in range(len(sections) - 1)]
        endpoints = np.column_stack([np.cos(t), np.sin(t)])
        plot_axis_labels(ax, endpoints, self.get_labels())

        center = np.zeros(2)

        for i in range(len(sections) - 1):
            t = np.linspace(sections[i], sections[i + 1], 100)
            v = np.column_stack([np.cos(t), np.sin(t)])

            P = np.row_stack([center, F[i] * v])
            plot_polygon(ax, P, color=self.colors[i])

        # draw the outer circle
        plot_circle(ax, **self.axis_style)
        plot_axes_lines(ax, V, **self.axis_style)

    def _do(self):

        n_rows = len(self.to_plot)
        n_cols = max([len(e[0]) for e in self.to_plot])
        self.init_figure(n_rows=n_rows, n_cols=n_cols, force_axes_as_matrix=True)

        # normalize the input
        bounds = parse_bounds(self.bounds, self.n_dim)
        to_plot_norm = normalize(self.to_plot, bounds, reverse=self.reverse)

        for k, (F, kwargs) in enumerate(to_plot_norm):
            for j, _F in enumerate(F):
                self._plot(self.ax[k, j], _F)


# =========================================================================================================
# Interface
# =========================================================================================================


def petal(bounds=None,
          **kwargs):
    """

    Petal Width Plot


    Parameters
    ----------------

    bounds : The boundaries for each objectives. Necessary to be provided for this plot!

    axis_style : {axis_style}

    reverse : bool
        Default false. Otherwise, larger area means smaller value.

    Other Parameters
    ----------------

    figsize : {figsize}
    title : {title}
    legend : {legend}
    tight_layout : {tight_layout}
    cmap : {cmap}



    Returns
    -------
    PetalDiagram : :class:`~pymoo.model.analytics.visualization.petal.PetalDiagram`

    """

    return PetalDiagram(bounds=bounds, **kwargs)


parse_doc_string(petal)