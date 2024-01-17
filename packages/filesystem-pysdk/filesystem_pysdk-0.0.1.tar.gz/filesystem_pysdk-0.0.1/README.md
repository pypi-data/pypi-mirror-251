# filesystem-pysdk

<!-- TOC -->

* [filesystem-pysdk](#filesystem-pysdk)
    * [I. Brief](#i-brief)

<!-- TOC -->

python filesystem sdk: [filesystem project](https://github.com/i-curve/filesystem)

## I. Brief

a python client for [filesystem](https://github.com/i-curve/filesystem).

support user, bucket, file manager.

## II. Quick tutorial

### 1. create a client

```python
import filesystem_pysdk

client, err = filesystem_pysdk.new_client("user", "auth", "api_host", "web_host")
```

### 2. user manager

- create a user

```python
import filesystem_pysdk

client.add_user(filesystem_pysdk.User("user1"))
```

- delete a user

```python
client.delete_user("user1")
```

### 3. bucket manager

- create a new bucket

```python
import filesystem_pysdk

client.add_bucket(filesystem_pysdk.Bucket(name="bucket1"))
```

- delete a bucket

```python
client.delete_user(name="bucket1")
```

### 4. file manager

- upload file

```python
import filesystem_pysdk

with open("client.py", "rb") as f:
    client.upload_file(filesystem_pysdk.File("bucket1", "test/client.py", 0),
                       f)
```

- download file

```python
import filesystem_pysdk

res = client.download_file(filesystem_pysdk.File("bucket1", "test/client.py"))
with open("client_download.py", "wb") as f:
    f.write(res)
```

- file move

```python
import filesystem_pysdk

client.move_file(filesystem_pysdk.File("bucket1", "test/a.py"),
                 filesystem_pysdk.File("bucket1", "test/b.py"))
```

- file copy

```python
import filesystem_pysdk

client.move_file(filesystem_pysdk.File("bucket1", "test/a.py"),
                 filesystem_pysdk.File("bucket1", "test/b.py"))
```