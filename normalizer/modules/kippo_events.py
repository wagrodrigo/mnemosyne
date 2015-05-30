# Copyright (C) 2012 Johnny Vestergaard <jkv@unixcluster.dk>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

import json
from normalizer.modules.basenormalizer import BaseNormalizer


class KippoEvents(BaseNormalizer):
    channels = ('kippo.sessions',)

    def normalize(self, data, channel, submission_timestamp, ignore_rfc1918=True):
        o_data = data

        if ignore_rfc1918 and self.is_RFC1918_addr(o_data['peerIP']):
            return []

        session = {
            'timestamp': submission_timestamp,
            'source_ip': o_data['peerIP'],
            'source_port': o_data['peerPort'],
            'destination_port': o_data['hostPort'],
            'honeypot': 'kippo',
            'protocol': 'ssh',
            'session_ssh': {'version': o_data['version']}
        }

        if 'ttylog' in o_data and o_data['ttylog'] is not None:
            attachments = [
                {
                    'description': 'Kippo session log (ttylog).',
                    'data': o_data['ttylog']
                }, ]

            session['attachments'] = attachments

        if len(o_data['credentials']) > 0:
            auth_attempts = []
            for cred in o_data['credentials']:
                auth_attempts.append({'login': cred[0],
                                      'password': cred[1]})
            session['auth_attempts'] = auth_attempts

        relations = [{'session': session}, ]

        return relations
