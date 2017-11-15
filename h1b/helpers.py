from bokeh.embed import components
from bokeh.models import HoverTool, ColorBar, LinearColorMapper, BasicTicker, Whisker, Range1d
from bokeh.models.formatters import NumeralTickFormatter
from bokeh.palettes import grey
from bokeh.plotting import figure, ColumnDataSource
from bokeh.resources import INLINE
from bokeh.sampledata.us_states import data as states

import numpy as np


# Preprocessed for speed, counts of how many H-1B applications each state has for 2002-2017
counts = {'CA': 3196865, 'NJ': 2453053, 'TX': 1922579, 'NY': 1552977, 'PA': 1201477, 'WA': 1071944, 'MA': 977908, 'IL': 915559, 'CT': 758070, 'NC': 739783, 'FL': 701662, 'VA': 592261, 'MI': 587154, 'MD': 411046, 'GA': 342109, 'MO': 291253, 'WI': 262572, 'OH': 260284, 'CO': 236999, 'MN': 224327, 'AZ': 222363, 'IN': 200266, 'DC': 144852, 'KY': 141163, 'NH': 130091, 'TN': 128088, 'DE': 125614, 'IA': 114983, 'UT': 114298, 'SC': 105416, 'NE': 95288, 'ND': 93922, 'KS': 88565, 'AR': 78960, 'LA': 77365, 'RI': 48027, 'OR': 47521, 'AL': 45253, 'OK': 44417, 'NV': 33392, 'WY': 30637, 'NM': 30536, 'ME': 29221, 'ID': 29025, 'VT': 27761, 'WV': 24392, 'MS': 22484, 'SD': 7347, 'MT': 4362}

count_max = counts['CA']
count_min = counts['MT']


# Preprocessed for speed, average H1B wage by state
avg_wages = {'FL': 59012.195429082, 'LA': 61117.3840982712, 'NM': 66545.7226448705, 'AK': 71449.4536703507, 'NC': 69984.9725894029, 'OR':  64595.766340105, 'VT': 63344.1328374939, 'MS': 61579.2163992118, 'AR': 83511.4570248415, 'IL':  65785.826252886, 'MO':  65826.667903666, 'IN':  63164.014970976, 'HI': 49790.3671336978, 'WY': 78631.5126496377, 'UT': 66425.2243542236, 'MI': 59079.9300108962, 'KS': 58349.9236134477, 'MD': 62033.6372695623, 'VI': 58792.8153992264, 'GA': 59075.5745867341, 'MN': 67971.9182409774, 'WI': 72892.2031108204, 'OH': 64147.7150167882, 'NE': 65581.4832396565, 'CT':  67599.799867161, 'NV': 63029.7528865365, 'OK': 55552.3466952578, 'AL': 59385.3426806741, 'CA':  72282.769358967, 'CO': 66827.3042488573, 'DE': 71813.7577147214, 'WV': 74677.8452534929, 'ND': 95224.4742161797, 'WA': 88322.1490585162, 'KY': 62631.2844277101, 'ME':  66666.780939149, 'RI': 40889.1688800198, 'VA': 58697.6783649352, 'TN': 62487.6464023609, 'SD': 79479.6676713801, 'NH': 62648.1190282254, 'IA': 64466.9335182881, 'SC': 61490.8015849381, 'NY': 74387.4186614052, 'MA': 71030.5076120827, 'NJ': 63766.5437575984, 'TX': 66947.5372873389, 'ID': 79240.5704975066, 'PA': 73640.6717774801, 'AZ': 67374.7785378836, 'MT': 57867.0902611916, 'DC': 66456.3437723182}


# Mean/std wage by year
yr = [2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017]
mean_wage = np.array([60054.815, 60620.562, 60373.805, 63028.128, 67129.455, 69198.940, 70607.377, 75342.197, 77179.807, 74936.084, 77114.969, 77118.744, 77075.323, 87134.622, 90761.583, 86888.704]) 
popstd_wage = np.array([34828.398, 31674.031, 30103.747, 30793.935, 31712.285, 32638.026, 32138.689, 35761.377, 33759.594, 29544.810, 30023.148, 28552.224, 26575.596, 35689.036, 36380.335, 36934.929])
upper = mean_wage + popstd_wage 
lower = (mean_wage - popstd_wage)[::-1]

wage_by_year = ColumnDataSource({'year': yr, 'mean_wg': mean_wage})


def prepare_source(data):
    data_min = min(data.values())
    data_max = max(data.values())

    if 'HI' in states.keys():
        del states['HI']
        del states['AK']

    excluded = ('AK', 'HI', 'PR', 'GU', 'VI', 'MP', 'AS')

    state_xs = [states[code]['lons'] for code in states]
    state_ys = [states[code]['lats'] for code in states]

    state_colors = []
    pal = grey(25)
    cmap = LinearColorMapper(palette=pal[::-1], low=data_min, high=data_max)

    for st in states:
        if st not in excluded:
            st_bin = int((1 - (data[st] - data_min)/data_max) * 25 - 1)
            state_colors.append(pal[st_bin])

    source = ColumnDataSource(data=dict(
        x=state_xs,
        y=state_ys,
        color=state_colors,
        name=[c for c in states if c not in excluded],
        data=[data[c] for c in states if c not in excluded]
    ))

    return (source, cmap)


def create_plot(source, cmap, tools, plot_width=700, plot_height=375):
    p = figure(toolbar_location='left', plot_width=plot_width, plot_height=plot_height, tools=tools)

    p.patches('x', 'y', source=source, fill_color='color', line_color='black', line_width=1)

    p.xgrid.grid_line_color = None
    p.ygrid.grid_line_color = None
    p.axis.visible = False
    p.toolbar.logo = None
    p.toolbar_location = None

    color_bar = ColorBar(color_mapper=cmap, ticker=BasicTicker(), label_standoff=12, border_line_color=None, location=(0, 0))

    p.add_layout(color_bar, 'left')

    js = INLINE.render_js()
    css = INLINE.render_css()
    script, div = components(p)

    return (script, div, js, css)


def create_wages_by_state():
    source, cmap = prepare_source(avg_wages)

    hover = HoverTool(tooltips=[
        ('State', '@name'),
        ('Average Wage', '@data{$0,0.00}'),
        ("(Long, Lat)", "($x, $y)"),
    ])

    return create_plot(source, cmap, [hover])


def create_cases_by_state():
    source, cmap = prepare_source(counts)
    
    hover = HoverTool(tooltips=[
        ('State', '@name'),
        ('Number of H-1B Visas', '@data{0,0}'),
        ("(Long, Lat)", "($x, $y)"),
    ])

    return create_plot(source, cmap, [hover])


def create_wages_by_year():
    p = figure(toolbar_location='left', plot_width=700, plot_height=375)

    band_x = np.append(yr, yr[::-1])
    band_y = np.append(upper, lower)
    p.patch(band_x, band_y, fill_color='black', line_color='#999999', fill_alpha=0.1)
    p.line('year', 'mean_wg', source=wage_by_year, line_width=2, line_color='black')

    p.yaxis[0].formatter = NumeralTickFormatter(format='$0,0.00')
    p.x_range = Range1d(2002, 2017)
    p.y_range = Range1d(0, 130000)
    p.toolbar.logo = None
    p.toolbar_location = None

    js = INLINE.render_js()
    css = INLINE.render_css()
    script, div = components(p)

    return (script, div, js, css)


