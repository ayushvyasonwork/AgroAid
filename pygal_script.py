import pygal
from pygal.style import Style

# Create a custom style with transparent background
custom_style = Style(
    background='transparent',
    plot_background='transparent',
    foreground='white'
)


def generate_semicircle_gauge_chart(value):
    # Create a SolidGauge chart
    gauge_chart = pygal.SolidGauge(
        half_pie=True,  # Display half pie (semi-circle)
        inner_radius=0.70,  # Adjust inner radius to create space for labels
        show_legend=False,  # Hide legend
        show_minor_ticks=False,  # Hide minor ticks
        human_readable=True,  # Enable human-readable values on labels
        range=(0, 100),  # Set range from 0 to 100
        major_label_font_size=50,  # Adjust major label font size
        style=custom_style,  # Use custom style
        height=400,
        padding=20,
    )
    # Add the humidity value to the chart
    gauge_chart.add('Humidity', [{'value': value, 'max_value': 100}])
    # Customize the value text
    gauge_chart.value_formatter = lambda x: '{:.1f}'.format(x)
    gauge_chart.value_font_size = 30  # Adjust value font size
    return gauge_chart.render(is_unicode=True)
