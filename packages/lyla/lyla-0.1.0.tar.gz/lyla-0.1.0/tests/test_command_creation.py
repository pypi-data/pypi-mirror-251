import textwrap

from lyla.latex_file_modifier import upsert_command_value_in_lines


def test_upsert_command_value_in_lines_adds_line():
    initial_file_contents = textwrap.dedent("""\
    \\newcommand{\\exampleLightCurveTicId}{149989733}
    \\newcommand{\\exampleLightCurveSector}{10}
    """)
    expected_file_contents = textwrap.dedent("""\
    \\newcommand{\\exampleLightCurveTicId}{149989733}
    \\newcommand{\\exampleLightCurveSector}{10}
    \\newcommand{\\exampleLightCurvePeriodInHours}{1.326}
    """)
    initial_file_lines = initial_file_contents.splitlines(keepends=True)
    file_lines = upsert_command_value_in_lines(initial_file_lines, 'exampleLightCurvePeriodInHours', 1.326)
    file_contents = ''.join(file_lines)
    assert file_contents == expected_file_contents


def test_upsert_command_value_in_lines_replaces_existing_line():
    initial_file_contents = textwrap.dedent("""\
    \\newcommand{\\exampleLightCurveTicId}{149989733}
    \\newcommand{\\exampleLightCurveSector}{10}
    """)
    expected_file_contents = textwrap.dedent("""\
    \\newcommand{\\exampleLightCurveTicId}{149989733}
    \\newcommand{\\exampleLightCurveSector}{11}
    """)
    initial_file_lines = initial_file_contents.splitlines(keepends=True)
    file_lines = upsert_command_value_in_lines(initial_file_lines, 'exampleLightCurveSector', 11)
    file_contents = ''.join(file_lines)
    assert file_contents == expected_file_contents
