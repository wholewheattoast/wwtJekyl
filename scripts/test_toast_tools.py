"""Tests for toast_tools scripts."""

from nose.tools import assert_equal


from toast_tools import (
    sort_nicely,
)

unsorted_list = ['b', '1', 'c', 'a', '0']


def test_sort_nicely():
    assert_equal(
        sort_nicely(unsorted_list),
        ['0', '1', 'a', 'b', 'c']
    )
