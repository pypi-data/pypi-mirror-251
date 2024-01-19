# Hack4u Academy Courses Library

Python library to consult academy courses

## Courses Available

- Introducción a Linux [15 hours]
- Personalización de Linux [3 hours]
- Introducción al Hacking [53 hours]

## Installation

Install the package using pip3:
```python3
pip3 install hack4u
```

## Basic Use

### List all courses

```python
from hack4u import list_courses

for course in list_courses():
  print(course)
```

### Get course by name

```python
from hack4u import get_course_by_name

course = get_course_by_name("Introducción a Linux")
print(course)
```
### Calculate total duration of courses

```python
from hack4u.utils import total_duration

print(f"Duración total: {total_duration()} hours")
```
