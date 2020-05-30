"""
open_cdn.server
~~~~~~~~~~~~

This module implements the error management.
:copyright: (c) 2020 by AdriBloober.
:license: GNU General Public License v3.0
"""

from resources.config import config


class BasicError(Exception):
    id = 0
    name = "basic_error"
    description = "The basic OpenCDN Error."
    http_return = 500

    def to_json(self):
        return {
            "status": "error",
            "id": self.id,
            "name": self.name,
            "description": self.description,
        }


class NoFileInRequest(BasicError):
    id = 1
    name = "no_file_in_request"
    description = "In the upload request is not file named 'file'."
    http_return = 400


class InvalidFileSuffix(BasicError):
    id = 2
    name = "invalid_file_suffix"
    description = "The file suffix is blacklisted, not whitelisted or does not exists."
    http_return = 403


class InvalidFileName(BasicError):
    id = 3
    name = "invalid_file_name"
    description = "The filename is invalid."
    http_return = 403


class BadRequest(BasicError):
    id = 4
    name = "bad_request"
    description = "The request is invalid constructed."
    http_return = 400


class FileDoesNotExists(BasicError):
    id = 5
    name = "file_does_not_exists"
    description = "The requested file does not exists."
    http_return = 404


class FileTooBig(BasicError):
    id = 6
    name = "file_too_big"
    description = f"The file is too big: {config.MAX_FILE_BYTES} bytes is maximum."
    http_return = 403


class AccessDenied(BasicError):
    id = 7
    name = "access_denied"
    description = "The access to the requested content was blocked, because you don't have access to the resource."
    http_return = 403


class ActionNeedsAuthenticationToken(BasicError):
    id = 8
    name = "action_needs_authentication_token"
    description = "To run this action, you should set 'authentication_token' to you'r authentication token."
    http_return = 400


class AuthenticationKeyNotFound(BasicError):
    id = 9
    name = "authentication_key_not_found"
    description = "The key with the key identifier was not found."
    http_return = 404


class InvalidAuthenticationToken(BasicError):
    id = 10
    name = "invalid_authentication_token"
    description = "The authentication token is invalid."
    http_return = 403


class InternalServerError(BasicError):
    id = 11
    name = "internal_server_error"
    description = "An unknown error occurred while answering the request."
    http_return = 500
