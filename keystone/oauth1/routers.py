# Copyright 2013 OpenStack Foundation
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import functools

from keystone.common import json_home
from keystone.common import wsgi
from keystone.oauth1 import controllers


build_resource_relation = functools.partial(
    json_home.build_v3_extension_resource_relation,
    extension_name='OS-OAUTH1', extension_version='1.0')

build_parameter_relation = functools.partial(
    json_home.build_v3_extension_parameter_relation,
    extension_name='OS-OAUTH1', extension_version='1.0')

ACCESS_TOKEN_ID_PARAMETER_RELATION = build_parameter_relation(
    parameter_name='access_token_id')


class Routers(wsgi.RoutersBase):
    """API Endpoints for the OAuth1 extension.

    The goal of this extension is to allow third-party service providers
    to acquire tokens with a limited subset of a user's roles for acting
    on behalf of that user. This is done using an oauth-similar flow and
    api.

    The API looks like::

      # User access token crud
      GET /users/{user_id}/OS-OAUTH1/access_tokens
      GET /users/{user_id}/OS-OAUTH1/access_tokens/{access_token_id}
      GET /users/{user_id}/OS-OAUTH1/access_tokens/{access_token_id}/roles
      GET /users/{user_id}/OS-OAUTH1/access_tokens
          /{access_token_id}/roles/{role_id}
      DELETE /users/{user_id}/OS-OAUTH1/access_tokens/{access_token_id}

    """

    _path_prefixes = ('users',)

    def append_v3_routers(self, mapper, routers):
        access_token_controller = controllers.AccessTokenCrudV3()
        access_token_roles_controller = controllers.AccessTokenRolesV3()

        # user access token crud
        self._add_resource(
            mapper, access_token_controller,
            path='/users/{user_id}/OS-OAUTH1/access_tokens',
            get_head_action='list_access_tokens',
            rel=build_resource_relation(resource_name='user_access_tokens'),
            path_vars={
                'user_id': json_home.Parameters.USER_ID,
            })
        self._add_resource(
            mapper, access_token_controller,
            path='/users/{user_id}/OS-OAUTH1/access_tokens/{access_token_id}',
            get_head_action='get_access_token',
            delete_action='delete_access_token',
            rel=build_resource_relation(resource_name='user_access_token'),
            path_vars={
                'access_token_id': ACCESS_TOKEN_ID_PARAMETER_RELATION,
                'user_id': json_home.Parameters.USER_ID,
            })
        self._add_resource(
            mapper, access_token_roles_controller,
            path='/users/{user_id}/OS-OAUTH1/access_tokens/{access_token_id}/'
            'roles',
            get_head_action='list_access_token_roles',
            rel=build_resource_relation(
                resource_name='user_access_token_roles'),
            path_vars={
                'access_token_id': ACCESS_TOKEN_ID_PARAMETER_RELATION,
                'user_id': json_home.Parameters.USER_ID,
            })
        self._add_resource(
            mapper, access_token_roles_controller,
            path='/users/{user_id}/OS-OAUTH1/access_tokens/{access_token_id}/'
            'roles/{role_id}',
            get_head_action='get_access_token_role',
            rel=build_resource_relation(
                resource_name='user_access_token_role'),
            path_vars={
                'access_token_id': ACCESS_TOKEN_ID_PARAMETER_RELATION,
                'role_id': json_home.Parameters.ROLE_ID,
                'user_id': json_home.Parameters.USER_ID,
            })
