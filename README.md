# Colorful logger for application

## I. Installation

- You can easily install it from pypi:

```bash
pip install hien_logger
```

- Or you can also install it from source:

```bash
git clone https://github.com/hienhayho/hien_logger.git

cd hien_logger/

pip install -v .
```

**Optional**:

- You can set datetime to your timezone:

```python
from hien_logger import setup_timezone

setup_timezone("Asia/Ho_Chi_Minh")
```

- To make sure `hien_logger` was sucessfully installed, run this:

```bash
pip install pytest

pytest
```

## II. Usage

- You can use it as a console logger:

```python
from hien_logger import get_formatted_logger

logger = get_formatted_logger(name="hien_logger")

logger.info("Hello World")
```

- Or you can log it to a file:

```python
from hien_logger import get_formatted_logger

logger = get_formatted_logger(
    name="hien_logger",
    file_path="test.log"
)

logger.info("Hello World")
```

## III. LICENSE

`hien_logger` is under [MIT LICENSE.](./LICENSE)
