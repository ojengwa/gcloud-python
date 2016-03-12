# Copyright 2016 Google Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Define Logging API Metrics."""


class Metric(object):
    """Metrics represent named filters for log entries.

    See:
    https://cloud.google.com/logging/docs/api/ref_v2beta1/rest/v2beta1/projects.metrics

    :type name: string
    :param name: the name of the metric

    :type filter_: string
    :param filter_: the advanced logs filter expression defining the entries
                   tracked by the metric.

    :type client: :class:`gcloud.logging.client.Client`
    :param client: A client which holds credentials and project configuration
                   for the metric (which requires a project).

    :type description: string
    :param description: an optional description of the metric
    """
    def __init__(self, name, filter_, client, description=''):
        self.name = name
        self._client = client
        self.filter_ = filter_
        self.description = description

    @property
    def client(self):
        """Clent bound to the logger."""
        return self._client

    @property
    def project(self):
        """Project bound to the logger."""
        return self._client.project

    @property
    def full_name(self):
        """Fully-qualified name used in metric APIs"""
        return 'projects/%s/metrics/%s' % (self.project, self.name)

    @property
    def path(self):
        """URL path for the metric's APIs"""
        return '/%s' % (self.full_name,)

    def _require_client(self, client):
        """Check client or verify over-ride.

        :type client: :class:`gcloud.logging.client.Client` or ``NoneType``
        :param client: the client to use.  If not passed, falls back to the
                       ``client`` stored on the current metric.

        :rtype: :class:`gcloud.logging.client.Client`
        :returns: The client passed in or the currently bound client.
        """
        if client is None:
            client = self._client
        return client

    def create(self, client=None):
        """API call:  create the metric via a PUT request

        See:
        https://cloud.google.com/logging/docs/api/ref_v2beta1/rest/v2beta1/projects.metrics/create

        :type client: :class:`gcloud.logging.client.Client` or ``NoneType``
        :param client: the client to use.  If not passed, falls back to the
                       ``client`` stored on the current metric.
        """
        client = self._require_client(client)
        data = {
            'name': self.name,
            'filter': self.filter_,
        }
        if self.description:
            data['description'] = self.description
        client.connection.api_request(method='PUT', path=self.path, data=data)