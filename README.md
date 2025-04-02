## 📚 API Quản lý Sách & Tác Giả với Tìm kiếm & Bộ nhớ Đệm  

### 🚀 **Công nghệ sử dụng**  
- **Backend**: Python (FastAPI)  
- **Cache**: Redis  
- **Tìm kiếm**: Elasticsearch  
- **Đóng gói**: Docker + Docker Compose  

Cấu trúc theo MVC

---

## 📌 **Các API chính**  

### Auth
#### Đăng nhập
- **POST** `/login`  
- **Dữ liệu**:  
  ```json
  { "username": "Username", "password": "password" }
  ```
- **Trả về**: Access token + Refresh token

#### 🔍 Refresh access token
- **GET** `/refresh`  
- **Trả về**: New access token

#### ✏️ Register
- **POST** `/register`  
- **Dữ liệu** Đăng ký user
  ```json
  { "username": "", "email": "", "fullname": "", "pasword": "" }
  ```
- **Trả về**: User mới

#### ❌ Get current user
- **GET** `/users/me`  
- **Trả về**: Username get from access token

#### ❌ Logout
- **POST** `/logout`  
- **Trả về**: Logout user bằng cách thêm user vào blacklist trong redis với format TOKEN_BLACK_LIST_username.

#### Middleware validate token
- **Trả về**: Decode token và check username có trong blacklist redis hay ko, có thì đã logout, ko thì pass. Set TTL = refresh token expire time

### 📖 Quản lý Sách  

#### ➕ Thêm sách  
- **POST** `/books`  
- **Dữ liệu**:  
  ```json
  { "title": "Tên sách", "author_id": "ID tác giả" }
  ```
- **Trả về**: Sách vừa thêm  

#### 🔍 Xem chi tiết sách  
- **GET** `/books/{book_id}`  
- **Trả về**: Thông tin sách  

#### ✏️ Cập nhật sách 
- **PUT** `/books/{book_id}`  
- **Dữ liệu** (có thể cập nhật một phần):  
  ```json
  { "title": "Tên mới", "author_id": "ID tác giả mới" }
  ```
- **Trả về**: Sách đã cập nhật  

#### ❌ Xóa sách
- **DELETE** `/books/{book_id}`  
- **Trả về**: Thông báo thành công  

#### 🔎 Tìm kiếm sách *(sử dụng Elasticsearch)*  
- **GET** `/books/search?q={query}`  
- **Trả về**: Danh sách sách liên quan  

---

### ✍️ Quản lý Tác Giả  

#### ➕ Thêm tác giả  
- **POST** `/authors`  
- **Dữ liệu**:  
  ```json
  { "name": "Tên tác giả", "bio": "Tiểu sử" }
  ```
- **Trả về**: Tác giả vừa thêm  

#### 🔍 Xem chi tiết tác giả  
- **GET** `/authors/{author_id}`  
- **Trả về**: Thông tin tác giả và danh sách sách của họ  

#### ✏️ Cập nhật tác giả  
- **PUT** `/authors/{author_id}`  
- **Dữ liệu**:  
  ```json
  { "name": "Tên mới", "bio": "Tiểu sử mới" }
  ```
- **Trả về**: Thông tin tác giả đã cập nhật  

#### ❌ Xóa tác giả  
- **DELETE** `/authors/{author_id}`  
- **Trả về**: Thông báo thành công  

---

## 🛠 **Cài đặt & Chạy ứng dụng**  

### 1️⃣ **Cài đặt Python & Thư viện**  
```bash
pip install -r requirements.txt
```

### 3️⃣ **Chạy API**  
```bash
uvicorn app.main:app --reload
```