import re
import shutil
import subprocess
from pathlib import Path

from lyla.latex_file_modifier import prepend_file_with_auto_generated_warning_message


def combine_and_flatten(output_directory: Path):
    output_directory.mkdir(exist_ok=True)
    main_output_path = output_directory.joinpath('main.tex')
    subprocess.run(['latexpand', 'main.tex', '-o', str(main_output_path)])
    with main_output_path.open() as main_output_file:
        main_output_content = main_output_file.read()
    for graphics_match in re.finditer(r'{([\w/]+(\.tikz|\.png|\.jpg|\.jpeg))}', main_output_content):
        graphics_path = Path(graphics_match.group(1))
        shutil.copy(graphics_path, output_directory.joinpath(graphics_path.name))
    main_output_content = re.sub(r'{([\w/]+/(\w+(\.tikz|\.png|\.jpg|\.jpeg)))}', r'{\g<2>}', main_output_content)
    with main_output_path.open('w') as main_output_file:
        main_output_file.write(main_output_content)
    bibliography_path = Path('bibliography.bib')
    shutil.copy(bibliography_path, output_directory.joinpath(bibliography_path.name))
    bbl_path = Path('main.bbl')
    shutil.copy(bbl_path, output_directory.joinpath(bbl_path.name))
    prepend_file_with_auto_generated_warning_message(main_output_path)


if __name__ == '__main__':
    combine_and_flatten(Path('/Users/golmschenk/Desktop/out'))
