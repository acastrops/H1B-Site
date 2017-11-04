from bokeh.embed import components
from bokeh.models import HoverTool, ColorBar, LinearColorMapper, BasicTicker
from bokeh.palettes import grey
from bokeh.plotting import figure, ColumnDataSource
from bokeh.resources import INLINE
from bokeh.sampledata.us_states import data as states
from bokeh.sampledata.unemployment import data as unemployment


# Preprocessed for speed, counts of how many H-1B applications each state has for 2002-2017
counts = {'CA': 3196865, 'NJ': 2453053, 'TX': 1922579, 'NY': 1552977, 'PA': 1201477, 'WA': 1071944, 'MA': 977908, 'IL': 915559, 'CT': 758070, 'NC': 739783, 'FL': 701662, 'VA': 592261, 'MI': 587154, 'MD': 411046, 'GA': 342109, 'MO': 291253, 'WI': 262572, 'OH': 260284, 'CO': 236999, 'MN': 224327, 'AZ': 222363, 'IN': 200266, 'DC': 144852, 'KY': 141163, 'NH': 130091, 'TN': 128088, 'DE': 125614, 'IA': 114983, 'UT': 114298, 'SC': 105416, 'NE': 95288, 'ND': 93922, 'KS': 88565, 'AR': 78960, 'LA': 77365, 'RI': 48027, 'OR': 47521, 'AL': 45253, 'OK': 44417, 'NV': 33392, 'WY': 30637, 'NM': 30536, 'ME': 29221, 'ID': 29025, 'VT': 27761, 'WV': 24392, 'MS': 22484, 'SD': 7347, 'MT': 4362}

count_max = counts['CA']
count_min = counts['MT']


# Preprocessed for speed, average H1B wage by state
avg_wages = {'PA': 81708.683808370870087, 'FM':  86997.802601794341, 'FL': 61423.884635333133, 'AZ': 68482.958816720327, 'LA': 135194.409353287377, 'MT': 57838.117615384615, 'PW': 66835.973877415057, 'AS': 55354.352218225420, 'GU': 72310.771521087270, 'NM': 67835.47651402369125, 'AK': 89534.925326321852, 'NC': 144925.546312036118, 'OR': 64451.476498469816, 'VT': 64376.687720754140, 'MS': 61758.814080978448, 'AR': 114299.067085244043, 'IL': 67181.015764884806, 'MO': 66442.588092489267, 'HI': 54715.200157316429, 'IN': 63696.431524319236, 'WY': 79329.069912262941, 'UT': 66925.111327745232, 'MI': 61498.273944995008, 'MP': 45285.639152981850, 'KS': 71027.822046907798, 'MD': 83936.754455080014, 'VI': 59039.797830534158, 'GA': 64244.433579801667045, 'MN': 69187.818506480722, 'DC': 71952.039821353809705, 'WI': 73370.993966988293, 'OH': 65070.896592780734, 'NE': 66455.144470735765, 'CT': 68905.762018881211, 'NV': 67682.178370632625, 'PR': 67381.454681626928, 'OK': 55640.272419008940, 'AL': 60478.663987440206, 'CA': 73739.043658373963091, 'CO': 67727.652849195915, 'WV': 75282.234543932276, 'DE': 71856.089998225722, 'ND': 95243.028586940212, 'WA': 88630.986802966711, 'KY': 64899.161438357796, 'ME': 69183.700568858972, 'RI': 40351.779469923213, 'VA': 61449.995813143130, 'TN': 63541.283296886847, 'SD': 81847.136237962100, 'NH': 82396.721050396559, 'IA': 65577.868224274924, 'SC': 63755.552200149165, 'MH': 53406.208479532164, 'NY': 88038.447972141742394, 'MA': 81947.616065191248727, 'NJ': 65899.417162808630555, 'TX': 68110.347310616114, 'ID': 79471.455976315487}


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
