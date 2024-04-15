import seaborn as sns
from faicons import icon_svg

from shiny import reactive
from shiny.express import input, render, ui
import palmerpenguins
import plotly.express as px
from shinywidgets import render_plotly
import shinyswatch

shinyswatch.theme.sketchy()

# saving the data locally
df = palmerpenguins.load_penguins()

ui.page_opts(title="Shellenberger Modlue 07 Penguins dashboard", fillable=True)


with ui.sidebar(title="Filter controls"):
    # Slider used to control 'mass' variable
    ui.input_slider("mass", "Mass", 2000, 6000, 6000)
    # checkboxes to control 'species' variable
    ui.input_checkbox_group(
        "species",
        "Species",
        ["Adelie", "Gentoo", "Chinstrap"],
        selected=["Adelie", "Gentoo", "Chinstrap"],
    )
    ui.hr()
    ui.h6("Links")
    ui.a(
        "GitHub Source",
        href="https://github.com/denisecase/cintel-07-tdash",
        target="_blank",
    )
    ui.a(
        "GitHub App",
        href="https://denisecase.github.io/cintel-07-tdash/",
        target="_blank",
    )
    ui.a(
        "GitHub Issues",
        href="https://github.com/denisecase/cintel-07-tdash/issues",
        target="_blank",
    )
    ui.a("PyShiny", href="https://shiny.posit.co/py/", target="_blank")
    ui.a(
        "Template: Basic Dashboard",
        href="https://shiny.posit.co/py/templates/dashboard/",
        target="_blank",
    )
    ui.a(
        "See also",
        href="https://github.com/denisecase/pyshiny-penguins-dashboard-express",
        target="_blank",
    )


with ui.layout_column_wrap(fill=False):
    # Shows a colored box for numerical statistics.
    with ui.value_box(showcase=icon_svg("earlybirds")):
        "Number of penguins"
        # Uses the filtered data based on the variables
        @render.text
        def count():
            return filtered_df().shape[0]

    with ui.value_box(showcase=icon_svg("ruler-horizontal")):
        "Average bill length"

        @render.text
        def bill_length():
            return f"{filtered_df()['bill_length_mm'].mean():.1f} mm" # Rounds to 1 decimal place ':.1f'

    with ui.value_box(showcase=icon_svg("ruler-vertical")):
        "Average bill depth"

        @render.text
        def bill_depth():
            return f"{filtered_df()['bill_depth_mm'].mean():.1f} mm" # Rounds to 1 decimal place ':.1f'


with ui.layout_columns():
    with ui.card(full_screen=True):
        ui.card_header("Bill length and depth")

        @render_plotly
        def length_depth():
            return px.scatter(
                filtered_df(),
                x="bill_length_mm",
                y="bill_depth_mm",
                color="species",
            )

    with ui.card(full_screen=True):
        ui.card_header("Penguin data")
        # Shows a Data Grid of the filtered data.
        @render.data_frame
        def summary_statistics():
            cols = [
                "species",
                "island",
                "bill_length_mm",
                "bill_depth_mm",
                "body_mass_g",
            ]
            return render.DataGrid(filtered_df()[cols], filters=True)


#ui.include_css(app_dir / "styles.css")

# filtering the data by species and body mass from the variables in the ui.sidebar
@reactive.calc
def filtered_df():
    filt_df = df[df["species"].isin(input.species())]
    filt_df = filt_df.loc[filt_df["body_mass_g"] < input.mass()]
    return filt_df
