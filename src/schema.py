from fastapi import HTTPException


class Response:
    def __init__(self, message: str, status_code: int, data=None):
        self.message = message
        self.status_code = status_code
        self.data = data

    def success_response(self):
        response = {"message": self.message, "data": self.data}
        return response, self.status_code

    def error_response(self):
        raise HTTPException(status_code=self.status_code, detail=self.message)