from http import HTTPStatus

from fastapi.exceptions import HTTPException


class ObjectAlreadyExistsError(HTTPException):
    def __init__(self, instance):
        self.detail = f"Object {instance!r} already exists."
        self.status_code = HTTPStatus.BAD_REQUEST


class SkuNotFoundError(HTTPException):
    def __init__(self, sku: str):
        self.detail = f"SKU `{sku}` not found."
        self.status_code = HTTPStatus.NOT_FOUND


class CartonNotFoundError(HTTPException):
    def __init__(self, carton_type: str):
        self.detail = f"Carton `{carton_type}` not found."
        self.status_code = HTTPStatus.NOT_FOUND


#
#
#
# class RecordNotFoundError(HTTPException):
#     def __init__(self, record_id: UUID, user_id: UUID):
#         self.detail = (
#             f"Record with ID `{record_id}'"
#             f" created by the user ID `{user_id}`"
#             f" not found."
#         )
#         self.status_code = HTTPStatus.NOT_FOUND
#
#
# class Mp3ConversionError(HTTPException):
#     def __init__(self, error: bytes):
#         self.detail = (
#             f"Error during mp3 conversion: {error.strip().decode('ascii')}"
#         )
#         self.status_code = HTTPStatus.NOT_FOUND
