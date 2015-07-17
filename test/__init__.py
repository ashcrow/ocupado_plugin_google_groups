# Copyright (C) 2015 SEE AUTHORS FILE
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
Tests for the LDAP plugin.
"""

import unittest

import mock

from apiclient.http import HttpMock, HttpMockSequence
from ocupado_plugin_google_groups import GoogleGroups


class TestOcupadoPluginGoogleGroups(unittest.TestCase):
    """
    Tests the GoogleGroups plugin.
    """

    #: Full path to the authorize method to patch
    auth_patch_str = (
        'oauth2client.client.SignedJwtAssertionCredentials.authorize')

    def test_plugin_google_groups_init(self):
        g = GoogleGroups(
            oauth2_file_location='test/test.json',
            group='test')

        self.assertEquals(g._group, 'test')
        self.assertEquals(g._oauth2_file_location, 'test/test.json')

    def test_plugin_google_groups_authenticate(self):
        with mock.patch(self.auth_patch_str) as _ca:
            # Replace the http_instance with our mock
            _http_mock = HttpMock(
                'test/directory-discovery.json', {'status': '200'})
            _ca.return_value = _http_mock

            g = GoogleGroups(
                oauth2_file_location='test/test.json',
                group='test')

            self.assertEquals(g.authenticate(), None)
            self.assertIsNotNone(g._con)

    def test_plugin_google_groups_logout(self):
        g = GoogleGroups(
            oauth2_file_location='test/test.json',
            group='test')

        # There is no auth state.
        self.assertEquals(g.logout(), None)

    def test_plugin_google_groups_exists(self):
        with mock.patch(self.auth_patch_str) as _ca:
            # Replace the http_instance with our mock
            _http_mock = HttpMockSequence([
                ({'status': '200'}, open(
                    'test/directory-discovery.json', 'r').read()),
                ({'status': '200'}, open(
                    'test/member-exists.json', 'r').read()),
            ])
            _ca.return_value = _http_mock

            g = GoogleGroups(
                oauth2_file_location='test/test.json',
                group='test')
            g.authenticate()

            exists, info = g.exists('human')
            self.assertTrue(exists)
            self.assertTrue(info['exists'])
            self.assertEquals(info['details']['username'], 'human')

    def test_plugin_google_groups_exists_with_no_results(self):
        with mock.patch(self.auth_patch_str) as _ca:
            # Replace the http_instance with our mock
            _http_mock = HttpMockSequence([
                ({'status': '200'}, open(
                    'test/directory-discovery.json', 'r').read()),
                ({'status': '404'}, '{}'),
            ])
            _ca.return_value = _http_mock

            g = GoogleGroups(
                oauth2_file_location='test/test.json',
                group='test')
            g.authenticate()

            exists, info = g.exists('doesnotexist')
            self.assertFalse(exists)
            self.assertFalse(info['exists'])
            self.assertEquals(info['details']['username'], 'doesnotexist')

    def test_plugin_google_groups_get_all_usernames(self):
        with mock.patch(self.auth_patch_str) as _ca:
            # Replace the http_instance with our mock
            _http_mock = HttpMockSequence([
                ({'status': '200'}, open(
                    'test/directory-discovery.json', 'r').read()),
                ({'status': '200'}, open(
                    'test/member-list.json', 'r').read()),
            ])
            _ca.return_value = _http_mock

            g = GoogleGroups(
                oauth2_file_location='test/test.json',
                group='test')
            g.authenticate()

            users = g.get_all_usernames()
            self.assertIn('human', users)
            self.assertIn('robot', users)
