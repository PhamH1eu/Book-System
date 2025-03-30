# from fastapi import FastAPI, Request, Response, status
# from fastapi.security import OAuth2PasswordBearer
# import jwt
# from jwt.exceptions import InvalidTokenError

# SECRET_KEY = "your_secret_key"
# ALGORITHM = "HS256"

# app = FastAPI()

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# EXCLUDED_PATHS = ["/token", "/register"]


# @app.middleware("http")
# async def check_oauth_token(request: Request, call_next):
#     # Bỏ qua kiểm tra token cho các route trong EXCLUDED_PATHS
#     if request.url.path in EXCLUDED_PATHS:
#         return await call_next(request)

#     # Lấy token từ header Authorization
#     auth_header = request.headers.get("Authorization")
#     if not auth_header or not auth_header.startswith("Bearer "):
#         return Response(
#             content="Missing or invalid token", status_code=status.HTTP_401_UNAUTHORIZED
#         )

#     token = auth_header.split("Bearer ")[1]  # Lấy phần token sau "Bearer "

#     # Kiểm tra token có hợp lệ không
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         request.state.user = payload  # Gán user vào request.state để sử dụng sau này
#     except InvalidTokenError:
#         return Response(
#             content="Invalid token", status_code=status.HTTP_401_UNAUTHORIZED
#         )

#     return await call_next(request)
