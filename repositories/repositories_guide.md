# Repository Layer Documentation

This document provides concrete examples of how to interact with the database.

The repositories `LordRepository`, `KnightRepository`, `CommonFolkRepository` are providing interface for CRUD operations.

## 1. Initialization and Session Management
Before using any repository, you must obtain a database session from `database_access.py`. 
**Note:** Close the session after your operations are complete to release the database connection.

```python
from database_access import get_session
from repositories import LordRepository, KnightRepository, CommonFolkRepository

# 1. Open a new session for the current request/operation
session = get_session()

# 2. Initialize repositories
lord_repo = LordRepository(session)
knight_repo = KnightRepository(session)
folk_repo = CommonFolkRepository(session)

# ... perform database operations ...

# 3. Always close the session in a `finally` block or context manager
session.close()
```

## 2. Creating Records (Create)
The `create_*` methods instantiate the models, add them to the session, and commit the transaction automatically.

```python
# Create a Lord
ned_stark = lord_repo.create_lord(name="Eddard Stark", photo_url="https://example.com/ned.jpg")

# Create a Knight
arthur = knight_repo.create_knight(
    name="Arthur Pendragon", 
    strength=95, 
    speed=85, 
    protection=90, 
    home="Camelot"
)

# Create a CommonFolk
smith = folk_repo.create_commonfolk(name="Will the Smith")
```

## 3. Reading Records (Read)
You can fetch records by their primary key (ID), retrieve all records, or use pagination. 

```python
# Get by ID
target_knight = knight_repo.get_knight_by_id(arthur.id)
print(target_knight.name)

# Get All (Lords and Knights only)
all_lords = lord_repo.get_all_lords()
for lord in all_lords:
    print(lord.name)

# Pagination (Page 1, 10 items per page)
page_1 = knight_repo.get_knights_paginated(page=1, page_size=10)
```

## 4. Updating Records (Update)
The `update_*` methods accept keyword arguments (`**kwargs`). You only need to pass the fields you want to change.

```python
# 1. Partial Update: Change only speed and strength
knight_repo.update_knight(arthur.id, speed=100, strength=99)

# 2. Set to NULL: Remove the home location
knight_repo.update_knight(arthur.id, home=None)

# 3. Update Lord
lord_repo.update_lord(ned_stark.id, photo_url="https://example.com/new_ned.jpg")
```

## 5. Deleting Records (Delete)
Returns `True` if the record was successfully found and deleted, or `False` if the record did not exist.

```python
is_deleted = folk_repo.delete_commonfolk(smith.id)
if is_deleted:
    print("CommonFolk removed successfully.")
```