"""Tests for wholewheattoast.com scripts."""

from nose.tools import assert_equal

from .sketchbook_tools import (
    assemble_spreads,
    sort_image_list,
    sb_url_safe_name,
    sb_display_name,
    sb_image_dir,
)

test_list = ['front cover', '001 002', '003 004', '141 142', 'back cover']
test_list_with_back_cover_first = ['back cover', '001 002']
test_list_with_ifc_001_last = ['197 198', 'ifc 001']
test_list_with_front_cover_last = ['001 002', 'front cover']


def test_sb_image_dir():
    assert_equal(
        sb_image_dir("bob"),
        "../image/sketchbooks/bob"
    )


def test_sb_display_name():
    assert_equal(
        sb_display_name("a-good-test"),
        "A Good Test"
    )


def test_sb_url_safe_name():
    assert_equal(
        sb_url_safe_name("A Good Test"),
        "a-good-test"
    )


def test_sort_image_list_back_cover_is_not_first():
    """"If back cover is first `sort_image_list()` should move it to end."""
    assert_equal(
        sort_image_list(test_list_with_back_cover_first),
        ['001 002', 'back cover']
    )


def test_sort_image_list_ifc_001_is_not_last():
    assert_equal(
        sort_image_list(test_list_with_ifc_001_last),
        ['ifc 001', '197 198']
    )


def test_sort_image_list_front_cover_is_first():
    assert_equal(
        sort_image_list(test_list_with_front_cover_last),
        ['front cover', '001 002']
    )


def test_assemple_spreads():
    assert_equal(
        assemble_spreads("test", test_list),
        [
            {
                'next': '001-002',
                'prev': 'back-cover',
                'sb_display_name': 'Test',
                'sb_url_safe_name': 'test',
                'spread': 'front-cover'
            },
            {
                'next': '003-004',
                'prev': 'front-cover',
                'sb_display_name': 'Test',
                'sb_url_safe_name': 'test',
                'spread': '001-002'
            },
            {
                'next': '141-142',
                'prev': '001-002',
                'sb_display_name': 'Test',
                'sb_url_safe_name': 'test',
                'spread': '003-004'
            },
            {
                'next': 'back-cover',
                'prev': '003-004',
                'sb_display_name': 'Test',
                'sb_url_safe_name': 'test',
                'spread': '141-142'
            },
            {
                'next': 'front-cover',
                'prev': '141-142',
                'sb_display_name': 'Test',
                'sb_url_safe_name': 'test',
                'spread': 'back-cover'
            }
        ]
    )
