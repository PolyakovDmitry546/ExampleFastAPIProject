from fastapi.security import OAuth2PasswordBearer

from settings import TOKEN_URL

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=TOKEN_URL)
