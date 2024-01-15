import re
from typing import Optional


class PytexPlaceholder:
    # noinspection SpellCheckingInspection
    context = {
        'textwidth': '469.0pt',
        'linewidth': '229.5pt',
        'columnwidth': '229.5pt',
    }


class PythontexLiaison:
    pytex: Optional[PytexPlaceholder] = None

    @classmethod
    def with_pytex_placeholder(cls):
        pythontex_liaison_ = cls()
        pythontex_liaison_.pytex = PytexPlaceholder()
        return pythontex_liaison_

    @staticmethod
    def latex_points_to_inches(latex_points: float) -> float:
        """
        Converts LaTeX points to inches. Note, a LaTeX point is a slightly different size than the now standard "point".

        :param latex_points: The number of LaTeX points.
        :return: The number of inches.
        """
        return latex_points / 72.27

    @staticmethod
    def inches_to_standard_points(inches: float) -> float:
        """
        Converts inches to standard points. Note, a LaTeX point is a slightly different size than the now standard "point".

        :param inches: The number of inches.
        :return: The number of standard points.
        """
        return inches * 72

    def latex_points_to_standard_points(self, latex_points: float) -> float:
        """
        Converts latex points to standard points. Note, a LaTeX point is a slightly different size than the now standard "point".

        :param latex_points: The number of latex points.
        :return: The number of standard points.
        """
        return self.inches_to_standard_points(self.latex_points_to_inches(latex_points))

    def latex_points_string_to_inches(self, latex_points_string: str) -> float:
        """
        Converts LaTeX points string to inches. Note, a LaTeX point is a slightly different size than the now standard
        "point".

        :param latex_points_string: The string listing the number of LaTeX points.
        :return: The number of inches.
        """
        assert latex_points_string.strip().endswith('pt')
        latex_points = float(latex_points_string.replace('pt', ''))
        return self.latex_points_to_inches(latex_points)

    def latex_dimension_string_to_inches(self, latex_dimension_string: str) -> float:
        """
        Converts a LaTeX dimension string to inches.

        :param latex_dimension_string: The latex dimension string (e.g., `0.8\textwidth`).
        :return: The size in inches.
        """
        latex_points_string, scalar = self.get_latex_points_string_from_latex_dimension_string(latex_dimension_string)
        return scalar * self.latex_points_string_to_inches(latex_points_string)

    def latex_dimension_string_to_standard_points(self, latex_dimension_string: str) -> float:
        """
        Converts a LaTeX dimension string to standard points.

        :param latex_dimension_string: The latex dimension string (e.g., `0.8\textwidth`).
        :return: The size in standard points (different from LaTeX points)
        """
        latex_points_string, scalar = self.get_latex_points_string_from_latex_dimension_string(latex_dimension_string)
        return scalar * self.inches_to_standard_points(self.latex_points_string_to_inches(latex_points_string))

    def get_latex_points_string_from_latex_dimension_string(self, latex_dimension_string):
        integer_or_float_pattern = r'\d+(?:\.\d+)?'
        match = re.match(fr'({integer_or_float_pattern})?\\(textwidth|linewidth|columnwidth)', latex_dimension_string)
        if match.group(1) is None:
            scalar = 1.0
        else:
            scalar = float(match.group(1))
        latex_dimension_name = match.group(2)
        latex_points_string = self.pytex.context[latex_dimension_name]
        return latex_points_string, scalar


pythontex_liaison = PythontexLiaison()
