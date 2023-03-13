from pydantic import BaseModel

class request_body(BaseModel):
    # Hosoda, Hayao, Shinkai, Paprika
    style: str
    file_path: str
