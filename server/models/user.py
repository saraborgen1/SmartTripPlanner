from pydantic import BaseModel

# מייצג משתמש שנכנס או נרשם למערכת עם שם משתמש וסיסמה
class User(BaseModel):
    username: str
    password: str
