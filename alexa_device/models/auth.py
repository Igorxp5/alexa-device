import datetime

from pydantic import BaseModel, Field


class CodePairRequest(BaseModel):
    user_code: str
    device_code: str
    interval: int
    verification_uri: str
    expires_in: int

    created_time: datetime.datetime = Field(default_factory=datetime.datetime.now)

    def is_expired(self):
        return (datetime.datetime.now() - self.created_time).total_seconds() > self.expires_in


class AccessGrant(BaseModel):
    refresh_token: str
    access_token: str = ''
    token_type: str = 'bearer'
    expires_in: int = 0

    created_time: datetime.datetime = Field(default_factory=datetime.datetime.now)

    def is_expired(self):
        return (datetime.datetime.now() - self.created_time).total_seconds() > self.expires_in
