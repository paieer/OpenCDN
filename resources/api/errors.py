from resources.config import config


class BasicError(Exception):
    id = 0
    name = "basic_error"
    description = "The basic OpenCDN Error."
    http_return = 500

    def to_json(self):
        return {"id": self.id, "name": self.name, "description": self.description}


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


class FileToBig(BasicError):
    id = 6
    name = "file_to_big"
    description = f"The file is to big: {config.MAX_FILE_BYTES} bytes is maximum."
    http_return = 403


class AccessDenied(BasicError):
    id = 7
    name = "access_denied"
    description = "The access to the requested content was blocked, because you don't have access to the resource."
    http_return = 403
