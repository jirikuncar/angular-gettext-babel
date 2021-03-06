# Copyright 2015, Rackspace, US, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.


default_keys = []


import unittest

from babel._compat import StringIO

from angular_gettext_babel.extract import extract_angular

default_keys = []


class ExtractAngularTestCase(unittest.TestCase):

    def test_extract_no_tags(self):
        buf = StringIO('<html></html>')

        messages = list(extract_angular(buf, default_keys, [], {}))
        self.assertEqual([], messages)

    def test_simple_string(self):
        buf = StringIO(
            """<html><translate>hello world!</translate>'
            <div translate>hello world!</div></html>"""
        )

        messages = list(extract_angular(buf, default_keys, [], {}))
        self.assertEqual(
            [
                (1, u'gettext', 'hello world!', []),
                (2, u'gettext', 'hello world!', [])
            ],
            messages)

    def test_attr_value(self):
        """We should not translate tags that have translate as the value of an
        attribute.
        """
        buf = StringIO('<html><div id="translate">hello world!</div></html>')

        messages = list(extract_angular(buf, [], [], {}))
        self.assertEqual([], messages)

    def test_attr_value_plus_directive(self):
        """Unless they also have a translate directive.
        """
        buf = StringIO(
            '<html><div id="translate" translate>hello world!</div></html>')

        messages = list(extract_angular(buf, [], [], {}))
        self.assertEqual([(1, 'gettext', 'hello world!', [])], messages)

    def test_translate_tag(self):
        buf = StringIO('<html><translate>hello world!</translate></html>')

        messages = list(extract_angular(buf, [], [], {}))
        self.assertEqual([(1, 'gettext', 'hello world!', [])], messages)

    def test_plural_form(self):
        buf = StringIO(
            (
                '<html><translate translate-plural="hello {$count$} worlds!">'
                'hello one world!</translate></html>'
            ))

        messages = list(extract_angular(buf, [], [], {}))
        self.assertEqual(
            [
                (1, 'ngettext',
                 ('hello one world!',
                  'hello {$count$} worlds!'
                  ),
                 [])
            ], messages)

    def test_translate_tag_comments(self):
        buf = StringIO(
            '<html><translate translate-comment='
            '"What a beautiful world">hello world!</translate></html>')

        messages = list(extract_angular(buf, [], [], {}))
        self.assertEqual(
            [
                (1, 'gettext', 'hello world!', ['What a beautiful world'])
            ],
            messages)

    def test_comments(self):
        buf = StringIO(
            '<html><div translate translate-comment='
            '"What a beautiful world">hello world!</div></html>')

        messages = list(extract_angular(buf, [], [], {}))
        self.assertEqual(
            [
                (1, 'gettext', 'hello world!', ['What a beautiful world'])
            ],
            messages)

    def test_multiple_comments(self):
        buf = StringIO(
            '<html><translate '
            'translate-comment="What a beautiful world"'
            'translate-comment="Another comment"'
            '>hello world!</translate></html>')

        messages = list(extract_angular(buf, [], [], {}))
        self.assertEqual(
            [
                (1, 'gettext', 'hello world!',
                 [
                     'What a beautiful world',
                     'Another comment'
                 ])
            ],
            messages)

    def test_nested_tags(self):
        buf = StringIO(
            '<html><translate '
            '>hello <b>Beautiful</b> world!</translate></html>')

        messages = list(extract_angular(buf, [], [], {}))
        self.assertEqual(
            [
                (1, 'gettext', 'hello <b>Beautiful</b> world!',
                 [ ])
            ],
            messages)
