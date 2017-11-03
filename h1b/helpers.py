from math import log
import sys

from bokeh.embed import components
from bokeh.models import HoverTool, LogColorMapper, LogTicker, ColorBar
from bokeh.palettes import grey
from bokeh.plotting import figure, ColumnDataSource
from bokeh.resources import INLINE
from bokeh.sampledata.us_states import data as states
from bokeh.sampledata.unemployment import data as unemployment


# Preprocessed for speed, counts of how many H-1B applications each state has for 2002-2017
counts = {'CA': 3196865, 'NJ': 2453053, 'TX': 1922579, 'NY': 1552977, 'PA': 1201477, 'WA': 1071944, 'MA': 977908, 'IL': 915559, 'CT': 758070, 'NC': 739783, 'FL': 701662, 'VA': 592261, 'MI': 587154, 'MD': 411046, 'GA': 342109, 'MO': 291253, 'WI': 262572, 'OH': 260284, 'CO': 236999, 'MN': 224327, 'AZ': 222363, 'IN': 200266, 'DC': 144852, 'KY': 141163, 'NH': 130091, 'TN': 128088, 'DE': 125614, 'IA': 114983, 'UT': 114298, 'SC': 105416, 'NE': 95288, 'ND': 93922, 'KS': 88565, 'AR': 78960, 'LA': 77365, 'RI': 48027, 'OR': 47521, 'AL': 45253, 'OK': 44417, 'NV': 33392, 'WY': 30637, 'NM': 30536, 'ME': 29221, 'ID': 29025, 'VT': 27761, 'WV': 24392, 'MS': 22484, 'SD': 7347, 'MT': 4362}

count_max = counts['CA']
count_min = counts['MT']


def create_cases_by_state():

    if 'HI' in states.keys():
        del states['HI']
        del states['AK']

    excluded = ('AK', 'HI', 'PR', 'GU', 'VI', 'MP', 'AS')

    state_xs = [states[code]['lons'] for code in states]
    state_ys = [states[code]['lats'] for code in states]

    state_colors = []
    pal = grey(25)

    for st in states:
        if st not in excluded:
            st_bin = int((1 - (counts[st] - count_min)/count_max) * 25 - 1)
            state_colors.append(pal[st_bin])

    source = ColumnDataSource(data=dict(
        x=state_xs,
        y=state_ys,
        color=state_colors,
        name=[c for c in states if c not in excluded],
        cn=[counts[c] for c in states if c not in excluded]
    ))

    hover = HoverTool(tooltips=[
        ('State', '@name'),
        ('Number of H-1B Visas', '@cn{0,0}'),
        ("(Long, Lat)", "($x, $y)"),
    ])

    p = figure(toolbar_location='right', plot_width=800, plot_height=425, tools=[hover])

    p.patches('x', 'y', source=source, fill_color='color', line_color='black', line_width=1)

    p.xgrid.grid_line_color = None
    p.ygrid.grid_line_color = None
    p.axis.visible = False

    js = INLINE.render_js()
    css = INLINE.render_css()
    script, div = components(p)

    return (script, div, js, css)
