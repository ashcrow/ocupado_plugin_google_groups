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
Google Groups plugin for the ocupado tool.
"""

import json

import httplib2

from ocupado.plugin import Plugin

import googleapiclient.errors

from apiclient import discovery
from oauth2client import client, tools


__version__ = '0.0.1'


class GoogleGroups:
    """
    GoogleGroups plugin for ocupado.
    """

    def __init__(self, oauth2_file_location, group):
        """
        Creates an instance of the Google Groups plugin.

        :oauth2_file_location: Disk location of the google provided auth file
        :group: Groups to look at
        """
        self._oauth2_file_location = oauth2_file_location
        self._group = group
        self._http_instance = httplib2.Http()
        self._con = None

    def authenticate(self, **kwargs):
        """
        Defines how to authenticate via Google Groups.

        :kwargs: Keyword arguments to use with authenticatation.
        """
        with open(self._oauth2_file_location) as f:
            conf_data = json.load(f)

        creds = client.SignedJwtAssertionCredentials(
            conf_data['client_email'],
            conf_data['private_key'],
            'https://www.googleapis.com/auth/admin.directory.user')

        http = creds.authorize(self._http_instance)
        self._con = discovery.build('admin', 'directory_v1', http=http)

    def logout(self):
        """
        Defines how to logout via a Plugin.
        """
        pass

    def exists(self, userid):
        """
        Checks for the existance of a user in Google Groups.

        :userid: The userid to check.
        """
        try:
            result = self._con.members().get(
                groupKey=self._group, memberKey=userid).execute()

            if not result:
                raise httplib2.HttpError(resp={'status': '404'})
            return True, {"exists": True, "details": {"username": userid}}
        except googleapiclient.errors.HttpError, he:
            return False, {'exists': False, 'details': {'username': userid}}

    def get_all_usernames(self):
        """
        Returns **all** user names.
        """
        result = []
        results = self._con.members().list(
            groupKey=self._group, maxResults=200).execute()
        for member in results['members']:
            result.append(member['email'].split('@')[0])
        return result
