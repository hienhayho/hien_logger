from pathlib import Path
from hien_logger import get_formatted_logger, get_date_format


def test_logger():
    logger = get_formatted_logger("hien_logger")
    logger.info("Hello, World!")
    assert True


def test_function():
    logger = get_formatted_logger("hien_logger")
    logger.info("Hello, World!")
    logger.debug("Hello, World!")
    logger.warning("Hello, World!")
    logger.error("Hello, World!")
    logger.critical("Hello, World!")
    assert True


def test_logger_file():
    logger = get_formatted_logger("hien_logger", file_path="test.log")
    logger.info("Hello, World!")
    assert Path("test.log").exists()

    with open("test.log", "r") as f:
        assert "Hello, World!" in f.read()

    Path("test.log").unlink()


def test_logger_with_folder():
    logger = get_formatted_logger("hien_logger", file_path="logs/test.log")
    logger.info("Hello, World!")
    assert Path("logs/test.log").exists()

    with open("logs/test.log", "r") as f:
        assert "Hello, World!" in f.read()

    Path("logs/test.log").unlink()


def test_global_log_file():
    logger = get_formatted_logger("hien_logger", global_file_log=True)

    logger.info("Hello, World!")
    assert Path("logs/global.log").exists()

    with open("logs/global.log", "r") as f:
        assert "Hello, World!" in f.read()

    Path("logs/global.log").unlink()


def test_include_date():
    now = get_date_format()
    logger = get_formatted_logger(
        "hien_logger", file_path="test.txt", include_date=True
    )
    logger.info("Hello, World!")
    assert Path(f"test_{now}.txt").exists()

    with open(f"test_{now}.txt", "r") as f:
        assert "Hello, World!" in f.read()

    Path(f"test_{now}.txt").unlink()
