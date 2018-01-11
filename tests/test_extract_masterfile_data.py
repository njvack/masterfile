#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Part of the masterfile package: https://github.com/njvack/masterfile
# Copyright (c) 2018 Board of Regents of the University of Wisconsin System
# Written by Nate Vack <njvack@wisc.edu> at the Center for Healthy Minds
# at the University of Wisconsin-Madison.
# Released under MIT licence; see LICENSE at the package root.

import pytest
import pandas as pd
from os import path

from .test_masterfile import EXAMPLE_PATH, GOOD_PATH
from masterfile.scripts import extract_masterfile_data
from masterfile.masterfile import Masterfile

INPUT_FILE = path.join(EXAMPLE_PATH, 'foo_input.csv')



class TestExtractMasterfileData(object):

    @pytest.fixture
    def df(self):
        return pd.read_csv(INPUT_FILE, dtype=str)

    @pytest.fixture
    def mf(self):
        return Masterfile.load_path(GOOD_PATH)

    def test_raises_on_empty_params(self):
        with pytest.raises(SystemExit):
            extract_masterfile_data.main([])

    def test_skip_rows_excludes_blanks(self, df):
        df2 = extract_masterfile_data._filter_rows(df, 'id_number', 0)
        assert len(df2) == (len(df) - 1)

    def test_skip_rows_skips(self, df):
        df2 = extract_masterfile_data._filter_rows(df, 'id_number', 1)
        assert len(df2) == (len(df) - 2)

    def test_sets_index_column(self, df, mf):
        df2 = extract_masterfile_data.format_dataframe_for_masterfile(
            df, mf, 'id_number', 1)
        assert df2.index.name == mf.index_column

    def test_filters_rows(self, df, mf):
        df2 = extract_masterfile_data.format_dataframe_for_masterfile(
            df, mf, 'id_number', 1)
        assert len(df2) == (len(df) - 2)

    def test_filters_columns(self, df, mf):
        df2 = extract_masterfile_data.format_dataframe_for_masterfile(
            df, mf, 'id_number', 1)
        assert len(df2.columns) == (len(df.columns) - 3)

    def test_roundtrip_file(self, tmpdir):
        outfile = str(tmpdir.join('output.csv'))
        extract_masterfile_data.main([
            '--index_column=id_number',
            '--skip=1',
            GOOD_PATH,
            INPUT_FILE,
            outfile])
        out = open(outfile).read()
        lines = out.split('\r\n')
        assert len(lines) == 11
        assert lines[-1] == ''
        columns = lines[0].split(',')
        assert columns[0] == 'ppt_id'

    def test_roundtrip_stdout(self, capsys):
        extract_masterfile_data.main([
            '--index_column=id_number',
            '--skip=1',
            GOOD_PATH,
            INPUT_FILE,
            '-'])
        out, _err = capsys.readouterr()
        lines = out.split('\r\n')
        assert len(lines) == 11
        assert lines[-1] == ''
        columns = lines[0].split(',')
        assert columns[0] == 'ppt_id'
