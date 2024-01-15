import io
import tempfile
from pathlib import Path
from typing import Union

from PIL import Image
from bokeh.core.enums import Place
from bokeh.core.property.wrappers import PropertyValueList
from bokeh.io import export_svg
from bokeh.io.export import wait_until_render_complete, _maximize_viewport, get_layout_html
from bokeh.models import LayoutDOM, Axis, ColorBar
from bokeh.plotting import figure as Figure
from cairosvg import svg2png
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from lyla.pythontex_liaison import pythontex_liaison


def export_png_via_svg(figure: Figure, output_path: Path) -> None:
    temporary_directory = Path(tempfile.gettempdir())
    resolution_scale_factor = 5
    figure.output_backend = 'svg'
    temporary_svg_path = temporary_directory.joinpath('temporary.svg')
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    web_driver = webdriver.Chrome(options=chrome_options)
    export_svg(figure, filename=temporary_svg_path, webdriver=web_driver)
    svg2png(url=str(temporary_svg_path), write_to=str(output_path), scale=resolution_scale_factor)


def export_png(figure: LayoutDOM, output_path: Path, scale_factor: int = 3) -> None:
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--hide-scrollbars")
    options.add_argument(f"--force-device-scale-factor={scale_factor}")
    options.add_argument("--force-color-profile=srgb")

    driver = webdriver.Chrome(options=options)

    with tempfile.NamedTemporaryFile(suffix='.html', mode='w', encoding="utf-8") as f:
        html = get_layout_html(figure)
        f.write(html)

        driver.maximize_window()
        driver.get(f"file://{f.name}")
        wait_until_render_complete(driver, 5)
        [width, height, dpr] = _maximize_viewport(driver)
        png = driver.get_screenshot_as_png()

        Image.MAX_IMAGE_PIXELS = None
        image = Image.open(io.BytesIO(png)).convert("RGBA").crop((0, 0, width * dpr, height * dpr))
        image.save(output_path)


def create_latex_figure_from_bokeh_figure(bokeh_figure: Figure, latex_figure_path: Union[Path, str], latex_width: str,
                                          latex_height: str) -> None:
    width__standard_points = pythontex_liaison.latex_dimension_string_to_standard_points(latex_width)
    height__standard_points = pythontex_liaison.latex_dimension_string_to_standard_points(latex_height)
    size_scale_factor = 1.5  # Bokeh figures have a 16px font by default and everything is based on that.
    # This is a simple way to scale the figure without needing to scale each Bokeh model.
    bokeh_figure.width = int(width__standard_points * size_scale_factor)
    bokeh_figure.height = int(height__standard_points * size_scale_factor)
    bokeh_figure.toolbar.logo = None
    bokeh_figure.toolbar_location = None
    set_label_font_to_math_font_recursively(bokeh_figure)
    export_png(figure=bokeh_figure, output_path=latex_figure_path)


def create_latex_figure_from_bokeh_layout(bokeh_layout: LayoutDOM, latex_figure_path: Union[Path, str],
                                          latex_width: str,
                                          latex_height: str) -> None:
    width__standard_points = pythontex_liaison.latex_dimension_string_to_standard_points(latex_width)
    height__standard_points = pythontex_liaison.latex_dimension_string_to_standard_points(latex_height)
    # Bokeh figures have a 16px font by default and everything is based on that.
    # This is a simple way to scale the figure without needing to scale each Bokeh model.
    size_scale_factor = 1.5
    bokeh_layout.width = int(width__standard_points * size_scale_factor)
    bokeh_layout.height = int(height__standard_points * size_scale_factor)
    remove_toolbar_recursively(bokeh_layout)
    set_label_font_to_math_font_recursively(bokeh_layout)
    set_size_stretch_on_children(bokeh_layout)
    export_png(figure=bokeh_layout, output_path=latex_figure_path)


def remove_toolbar_recursively(bokeh_layout: LayoutDOM):
    if isinstance(bokeh_layout, Figure):
        bokeh_layout.toolbar.logo = None
        bokeh_layout.toolbar_location = None
    if hasattr(bokeh_layout, 'children'):
        for child in bokeh_layout.children:
            remove_toolbar_recursively(child)


def set_label_font_to_math_font_recursively(bokeh_layout: LayoutDOM):
    if isinstance(bokeh_layout, Figure):
        for position in [bokeh_layout.above, bokeh_layout.left, bokeh_layout.right, bokeh_layout.below]:
            for property_value in position:
                if isinstance(property_value, Axis):
                    property_value.axis_label = rf'$$$${property_value.axis_label}$$$$'
                if isinstance(property_value, ColorBar):
                    property_value.title = rf'$$$${property_value.title}$$$$'
    if hasattr(bokeh_layout, 'children'):
        for child in bokeh_layout.children:
            set_label_font_to_math_font_recursively(child)


def set_size_stretch_on_children(bokeh_layout: LayoutDOM, sizing_mode: str = 'stretch_both'):
    if hasattr(bokeh_layout, 'children'):
        for child in bokeh_layout.children:
            child.sizing_mode = sizing_mode
            set_size_stretch_on_children(child)
