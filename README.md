## 📚 API Quản lý Sách & Tác Giả với Tìm kiếm & Bộ nhớ Đệm  

### 🚀 **Công nghệ sử dụng**  
- **Backend**: Python (FastAPI)  
- **Cache**: Redis  
- **Tìm kiếm**: Elasticsearch  
- **Đóng gói**: Docker + Docker Compose  

---

## 📌 **Các API chính**  

### 📖 Quản lý Sách  

#### ➕ Thêm sách  
- **POST** `/books`  
- **Dữ liệu**:  
  ```json
  { "title": "Tên sách", "author_id": "ID tác giả" }
  ```
- **Trả về**: Sách vừa thêm  

#### 🔍 Xem chi tiết sách *(có cache Redis)*  
- **GET** `/books/{book_id}`  
- **Trả về**: Thông tin sách  

#### ✏️ Cập nhật sách *(xóa cache Redis)*  
- **PUT** `/books/{book_id}`  
- **Dữ liệu** (có thể cập nhật một phần):  
  ```json
  { "title": "Tên mới", "author_id": "ID tác giả mới" }
  ```
- **Trả về**: Sách đã cập nhật  

#### ❌ Xóa sách *(xóa cache Redis)*  
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
pip install fastapi uvicorn redis elasticsearch
```

### 2️⃣ **Chạy Redis & Elasticsearch (Docker)**  
```bash
docker-compose up -d
```

### 3️⃣ **Chạy API**  
```bash
uvicorn app:app --reload
```

---

## 🎯 **Mục tiêu học tập**  
✅ Xây dựng API với **FastAPI**  
✅ Tích hợp **Redis** để cache dữ liệu  
✅ Dùng **Elasticsearch** cho tìm kiếm  
✅ **Docker hóa** ứng dụng  
