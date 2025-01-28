# A-Parser Async Python Library

## Overview

The **A-Parser Async Python Library** is a powerful, modern, and feature-rich solution for interacting with the A-Parser API using Python. Designed for developers who require robust and efficient API integration, this library leverages Python's asynchronous capabilities and the Pydantic library for schema validation, ensuring performance, reliability, and ease of use.

---

## Key Features

### 🌟 **Asynchronous API**
The library is fully asynchronous, built on Python's `asyncio` and `httpx` to maximize performance and responsiveness. It allows for non-blocking API requests, enabling efficient parallel task management.

### 📜 **Pydantic-Based Validation**
Every request and response is validated using Pydantic models. This ensures data integrity, provides clear error messages, and reduces the risk of bugs caused by malformed data.

### 💡 **Simplified API Integration**
With thoughtfully designed methods, the library simplifies interaction with the A-Parser API, including task management, proxy checker control, and result retrieval.

### 🔧 **Comprehensive Functionality**
The library supports a wide range of features offered by the A-Parser API:
- Add tasks to the queue
- Retrieve task states and results
- Manage and delete tasks
- Control proxy checker states
- Handle task results with ease

---

## Installation

```bash
pip install aparser-async
```

---

## Usage

### Import the Library

```python
from aparser_async import AParser, schemas, AParserError
```

### Initialize the Client

```python
aparser = AParser(address="http://127.0.0.1", password="your_password", port=9091)
```

### Examples

#### 1. **Ping the API**
```python
import asyncio

async def check_api():
    response = await aparser.ping()
    print(f"Ping response: {response}")

asyncio.run(check_api())
```

#### 2. **Add a Task**
```python
task_data = schemas.Data(
    preset="example_preset",
    parsers=[["parser1"], ["parser2"]],
    queries="example_query"
)

async def create_task():
    task_id = await aparser.add_task(task_data)
    print(f"Task created with ID: {task_id}")

asyncio.run(create_task())
```

#### 3. **Get Task Status**
```python
async def get_status(task_id):
    status = await aparser.get_task_state(task_id)
    print(f"Task {task_id} Status: {status.status}")

asyncio.run(get_status(task_id=12345))
```

#### 4. **Wait for Task Completion**
```python
async def wait_for_task(task_id):
    try:
        await aparser.wait_for_task(task_id, delay=2, timeout=60)
        print(f"Task {task_id} completed successfully!")
    except AParserError as e:
        print(f"Task {task_id} failed: {e}")

asyncio.run(wait_for_task(task_id=12345))
```

---

## Benefits

### 🚀 Performance
Asynchronous programming allows you to handle multiple tasks efficiently, saving time and system resources.

### ✅ Reliability
The library ensures every interaction with the A-Parser API is validated, reducing the chance of runtime errors.

### 🛠️ Developer-Friendly
With clear documentation, intuitive APIs, and detailed logging, this library is designed for seamless integration into your Python projects.

---

## Requirements

- Python 3.8+
- A running instance of **A-Parser**
- `httpx` for HTTP requests
- `pydantic` for schema validation

---

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes. Ensure your code adheres to PEP 8 and includes tests for new functionality.

---

## License

This library is licensed under the MIT License. See the `LICENSE` file for more details.

---

## Acknowledgements

Special thanks to the developers of:
- [A-Parser](https://a-parser.com/)
- [httpx](https://www.python-httpx.org/)
- [Pydantic](https://docs.pydantic.dev/)

---

With **A-Parser Async**, managing your API tasks has never been easier or more efficient. 🎉