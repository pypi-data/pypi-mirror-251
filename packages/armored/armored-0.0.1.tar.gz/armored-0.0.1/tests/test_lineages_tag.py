import datetime
import unittest
from unittest import mock

import armored.lineages as lineages


class TestTag(unittest.TestCase):
    @mock.patch("armored.lineages.date", wraps=datetime.date)
    @mock.patch("armored.lineages.datetime", wraps=datetime.datetime)
    def test_tag_init(self, mock_datetime, mock_date):
        mock_date.return_value = datetime.date(2023, 1, 1)
        mock_datetime.now.return_value = datetime.datetime(2023, 1, 1, 0, 0, 0)
        t = lineages.Tag()
        self.assertDictEqual(
            t.model_dump(by_alias=False),
            {
                "author": "undefined",
                "desc": None,
                "labels": [],
                "ts": datetime.datetime(2023, 1, 1, 0, 0, 0),
                "vs": datetime.date(2023, 1, 1),
            },
        )
