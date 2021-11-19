#-----------------------------------------------------------------------------
# Copyright (c) 2012 - 2021, Anaconda, Inc., and Bokeh Contributors.
# All rights reserved.
#
# The full license is in the file LICENSE.txt, distributed with this software.
#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
# Boilerplate
#-----------------------------------------------------------------------------
from __future__ import annotations # isort:skip

import pytest ; pytest

#-----------------------------------------------------------------------------
# Imports
#-----------------------------------------------------------------------------

# Standard library imports
import hashlib
import re
from os.path import abspath, join, split
from typing import List

# Bokeh imports
from bokeh.embed import file_html
from bokeh.plotting import figure
from bokeh.resources import JSResources

# Module under test
import bokeh.core.templates as bct # isort:skip

#-----------------------------------------------------------------------------
# Setup
#-----------------------------------------------------------------------------

TOP_PATH = abspath(join(split(bct.__file__)[0]))

#-----------------------------------------------------------------------------
# General API
#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
# Private API
#-----------------------------------------------------------------------------

def _crlf_cr_2_lf_bin(s):
    return re.sub(b"\r\n|\r|\n", b"\n", s)

#-----------------------------------------------------------------------------
# Dev API
#-----------------------------------------------------------------------------

def compute_sha256(data):
    sha256 = hashlib.sha256()
    sha256.update(data)
    return sha256.hexdigest()

def get_html_lines() -> List[str]:
    p = figure()
    p.scatter(x=[], y=[])
    html = file_html(p, JSResources(mode="absolute"))
    return html.split('\n')

pinned_template_sha256 = "5d26be35712286918e36cc469c9354076b3d555eb39799aa63d04473c0566c29"

def test_autoload_template_has_changed() -> None:
    """This is not really a test but a reminder that if you change the
    autoload_nb_js.js template then you should make sure that insertion of
    plots into notebooks is working as expected. In particular, this test was
    created as part of https://github.com/bokeh/bokeh/issues/7125.
    """
    with open(join(TOP_PATH, "_templates/autoload_nb_js.js"), mode="rb") as f:
        current_template_sha256 = compute_sha256(_crlf_cr_2_lf_bin(f.read()))
        assert pinned_template_sha256 == current_template_sha256, """\
            It seems that the template autoload_nb_js.js has changed.
            If this is voluntary and that proper testing of plots insertion
            in notebooks has been completed successfully, update this test
            with the new file SHA256 signature."""

def test_no_white_space_in_top_of_html() -> None:
    lines = get_html_lines()
    any_character = re.compile(r"\S")
    assert(any_character.search(lines[0]) is not None)

def test_no_scripts_start_on_same_line() -> None:
    lines = get_html_lines()
    script_start = re.compile("<script")
    for line in lines:
        start_match = script_start.findall(line)
        if start_match:
            assert len(start_match) == 1
        
def test_no_scripts_start_on_same_line_another_ends() -> None:
    lines = get_html_lines()
    script_start = re.compile("<script")
    script_end = re.compile("</script>")
    for line in lines:
        start_match = script_start.search(line)
        end_match = script_end.search(line)
        if  start_match and end_match:
            assert start_match.start() < end_match.start()
#-----------------------------------------------------------------------------
# Private API
#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
# Code
#-----------------------------------------------------------------------------
