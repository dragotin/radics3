# Copyright © 2022 Klaas Freitag <kraft@freisturz.de>
#
# This library is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Radicale.  If not, see <http://www.gnu.org/licenses/>.

from radicale.auth import BaseAuth
from radicale.log import logger

import grpc

import cs3.storage.provider.v1beta1.resources_pb2 as cs3spr
import cs3.storage.provider.v1beta1.provider_api_pb2 as cs3sp
import cs3.gateway.v1beta1.gateway_api_pb2_grpc as cs3gw_grpc

import cs3.gateway.v1beta1.gateway_api_pb2 as cs3gw
import cs3.rpc.v1beta1.code_pb2 as cs3code
import cs3.types.v1beta1.types_pb2 as types


PLUGIN_CONFIG_SCHEMA = {"auth": {
    "revagateway": {"value": "", "type":str}}}

ctx = {}

class Auth(BaseAuth):
    def __init__(self, configuration):
        super().__init__(configuration.copy(PLUGIN_CONFIG_SCHEMA))
        revagateway = configuration.get('auth', 'revagateway')
        # prepare the gRPC connection
        ch = grpc.insecure_channel(revagateway)
        ctx['cs3gw'] = cs3gw_grpc.GatewayAPIStub(ch)

    def login(self, userid, userpwd):
        '''Use basic authentication against Reva for testing purposes'''
        logger.info('--- CS3 API Basic Auth Authentication ----')
        authReq = cs3gw.AuthenticateRequest(type='basic', client_id=userid, client_secret=userpwd)
        authRes = ctx['cs3gw'].Authenticate(authReq)
        logger.debug('msg="Authenticated user" res="%s"' % authRes)
        if authRes.status.code != cs3code.CODE_OK:
            raise IOError('Failed to authenticate as user ' + userid + ': ' + authRes.status.message)
        
        ctx['cs3token'] = authRes.token # Store the token in the contex for that user
        return authRes.user.username
        
