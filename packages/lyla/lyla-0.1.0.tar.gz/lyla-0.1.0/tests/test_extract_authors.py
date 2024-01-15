import pytest as pytest

from lyla.extract_authors import extract_author_names_from_latex_string


@pytest.mark.integration
def test_extract_author_names():
    latex_string = r"""
    \documentclass[twocolumn]{aastex631}
    
    \newcommand{\gsfcAffiliationString}{NASA Goddard Space Flight Center, Greenbelt, MD 20771, USA}
    \newcommand{\umdAffiliationString}{Department of Astronomy, University of Maryland, College Park, MD 20742, USA}
    \newcommand{\orauAffiliationString}{Oak Ridge Associated Universities, Oak Ridge, TN 37830, USA}
    \newcommand{\moaAffiliationString}{The MOA Collaboration}
    
    \begin{document}
    \title{MOA-2020-BLG-208: Cool Sub-Saturn Planet Within Predicted Desert}
    
    \author[0000-0001-8472-2219]{Greg Olmschenk}
    \affiliation{\gsfcAffiliationString}
    \affiliation{\orauAffiliationString}
    \affiliation{\moaAffiliationString}
    
    \author[0000-0001-8043-8413]{David P. Bennett}
    \affiliation{\gsfcAffiliationString}
    \affiliation{\umdAffiliationString}
    \affiliation{\moaAffiliationString}
    
    \author{Ian A.~Bond}
    \affiliation{Institute of Natural and Mathematical Sciences, Massey University, Auckland 0745, New Zealand}
    \affiliation{\moaAffiliationString}
    
    \author{P.~Zieli{\'n}ski}
    
    \end{document}    
    """
    author_names = extract_author_names_from_latex_string(latex_string)
    assert author_names == ['Greg Olmschenk', 'David P. Bennett', 'Ian A.~Bond', r"P.~Zieli{\'n}ski"]
