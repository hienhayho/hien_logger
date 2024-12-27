## Colorful logger for application

#### 1. Installation

You can easily install it from pypi:

```bash
pip install hien_logger
```

#### 2. Usage
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