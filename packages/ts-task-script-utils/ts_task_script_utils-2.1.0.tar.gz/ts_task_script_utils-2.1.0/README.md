# ts-task-script-utils <!-- omit in toc -->

## Version <!-- omit in toc -->

v2.1.0

## Table of Contents <!-- omit in toc -->

- [Summary](#summary)
- [Installation](#installation)
- [Usage](#usage)
  - [Parsing Numbers](#parsing-numbers)
  - [Parsing Datetimes](#parsing-datetimes)
    - [`DatetimeParser` Usage](#datetimeparser-usage)
  - [Generating Random UUIDs for Task Scripts](#generating-random-uuids-for-task-scripts)
  - [Using Python's `logging` module in Task Scripts](#using-pythons-logging-module-in-task-scripts)
  - [WellPosition](#wellposition)
- [Changelog](#changelog)
  - [v2.1.0](#v210)
  - [v2.0.1](#v201)
  - [v2.0.0](#v200)
  - [v1.9.0](#v190)
  - [v1.8.1](#v181)
  - [v1.8.0](#v180)
  - [v1.7.0](#v170)
  - [v1.6.0](#v160)
  - [v1.5.0](#v150)
  - [v1.4.0](#v140)
  - [v1.3.1](#v131)
  - [v1.3.0](#v130)
  - [v1.2.0](#v120)
  - [v1.1.1](#v111)
  - [v1.1.0](#v110)

## Summary

Utility functions for Tetra Task Scripts

## Installation

`pip install ts-task-script-utils`

## Usage

### Parsing Numbers

```python
from task_script_utils.parse import to_int

string_value = '1.0'
int_value = to_int(string_value)

# `int_value` now has the parsed value of the string
assert isinstance(int_value, int)
assert int_value == 1

# it returns `None` if the value is unparseable
string_value = 'not an int'
int_value = to_int(string_value)

assert int_value is None
```

### Parsing Datetimes

> [!WARNING]
> **DEPRECATION** Do not use the old datetime parsing functions:
>
> - `convert_datetime_to_ts_format` from `task_script_utils.convert_datetime_to_ts_format`
> - `parse` from `task_script_utils.datetime_parser`

Use the `DatetimeParser` from `task_script_utils.datetime_parser` to parse datetimes.

`DatetimeParser` takes a list of formats used for parsing datetimes.
`DatetimeParser` does not infer the structure of a datetime string, formats must be provided.

#### `DatetimeParser` Usage

Using `DatetimeParser` with a list of formats

```python
from task_script_utils.datetime_parser import DatetimeParser

datetime_parser = DatetimeParser(formats=["YYYY-MM-DD[T]hh:mm A Z"])

ts_formatted_datetime: str | None = datetime_parser.to_tsformat("2004-12-23T12:30 AM +05:30")
```

Using `DatetimeParser` with a timezone mapping and a list of formats

```python
from task_script_utils.datetime_parser import DatetimeParser

formats = ["YYYY-MM-DD[T]hh:mm A zz"]
tz_dict = {"EST": "-05:00"}
datetime_parser = DatetimeParser(formats=formats, tz_dict=tz_dict)

ts_formatted_datetime: str | None = datetime_parser.to_tsformat("2004-12-23T12:30 AM EST")
```

If you need the `TSDatetime` object, you can use `DatetimeParser.parse() -> TSDatetime`.
`TSDatetime` gives access to  `TSDatetime.datetime` which can be used as a regular python datetime object.

You can read more about the datetime parser [here](task_script_utils/datetime_parser/README.md).

### Generating Random UUIDs for Task Scripts

To generate standard and random UUIDs, Python's `uuid` module can be used (`uuid1` for standard and `uuid4` for random).
However, to get UUIDs that are reproducible for a given task script and input file, a custom UUID generator is provided:
`task_script_utils.random.TaskScriptUUIDGenerator`.

```python
from pathlib import Path
from task_script_utils.random import TaskScriptUUIDGenerator

input_file = Path(...)
file_content = input_file.read_bytes()
rand = TaskScriptUUIDGenerator("common/my-task-script:v1.0.0", file_content)

# Get 3 random bytes:
random_bytes = rand.randbytes(3)

# Get a random UUID:
uuid = rand.uuid()
```

It's also possible to use a class method and provide the task script identifiers separately:

```python
from pathlib import Path
from task_script_utils.random import TaskScriptUUIDGenerator

input_file = Path(...)
file_content = input_file.read_bytes()
rand = TaskScriptUUIDGenerator.from_task_script_identifier_parts("common", "my-task-script", "v1.0.0", file_content)
```

The class uses a pattern similar to the singleton pattern that allows to create an instance once and then "get the last created" instance later without passing the instance around.
This is achieved with the `get_last_created` method:

```python
from pathlib import Path
from task_script_utils.random import TaskScriptUUIDGenerator

input_file = Path(...)
file_content = input_file.read_bytes()
rand1 = TaskScriptUUIDGenerator("common/my-task-script:v1.0.0", file_content)

rand2 = TaskScriptUUIDGenerator.get_last_created()

assert rand1 is rand2
```

If no instance has been created before, `NoPreviouslyCreatedInstanceError` will be raised.

Note that the arguments used to create a `TaskScriptUUIDGenerator` makes up the seed for the RNG and two instances made with the same seed will go through the same sequence of UUIDs.
That is usually unintentional in the context of a Task Script where the UUIDs should be unique.

```python
from pathlib import Path
from task_script_utils.random import TaskScriptUUIDGenerator

input_file = Path(...)
file_content = input_file.read_bytes()

rand1 = TaskScriptUUIDGenerator("common/my-task-script:v1.0.0", file_content)
rand2 = TaskScriptUUIDGenerator("common/my-task-script:v1.0.0", file_content)

assert rand1.uuid() == rand2.uuid()
assert rand1.uuid() == rand2.uuid()
```

### Using Python's `logging` module in Task Scripts

Task Scripts can write workflow logs which are visible to users on TDP, but only if the logs are written via the logger provided by the `context` object. The `context` logger is documented here: [context.get_logger](https://developers.tetrascience.com/docs/context-api#contextget_logger).

This utility is a wrapper for the `context` logger which allows Task Scripts to use Python's `logging` module for creating TDP workflow logs, instead of directly using the `context` logger object. This means the `context` logger object doesn't need to be passed around to each function which needs to do logging, and Task Script code can benefit from other features of the Python `logging` module such as [integration with `pytest`](https://docs.pytest.org/en/7.1.x/how-to/logging.html).

To log warning messages on the platform from a task script do the following:

- Setup the log handler in `main.py`:

```python
from task_script_utils.workflow_logging import (
    setup_ts_log_handler,
)
```

- Then within the function called by the protocol:

```python
setup_ts_log_handler(context.get_logger(), "main")
```

- In a module where you wish to log a warning:

```python
import logging
logger = logging.getLogger("main." + __name__)
```

- Log a warning message with:

```python
logger.warning("This is a warning message")
```

### WellPosition

For plate readers, you can parse the well label using `task_script_utils.plate_reader.WellPosition`.

`WellPosition` encapsulates row and column indexes for a well on a plate.

You can use `WellPosition.from_well_label` to parse the `well_label: str` and get the `WellPosition` object.

For example:

```python
from plate_reader import WellPosition
WellPosition.from_well_label("P45") # returns WellPosition(row=16, column=45)
```

A `well_label` must satisfy following conditions:

  1. It must start with a letter
  2. It can contain at max two letters
      - When it contains two letters, they must both be uppercase
  3. Letter(s) must be followed by at least one and at max two digits

If the label cannot be parsed, `InvalidWellLabelError` is raised.

eg, `A45, a45, A01, A1, z1, z01, AC23` are valid well labels

Following are the example of invalid well labels:

- `A245`: `well_label` with more than 2 digits is not supported
- `A` or `a` or `aa`: `well_label`  doesn't contain any digit. Hence it is not supported.
- `aB02, Ab02, ab02`: Both letters must be uppercase.

Parsing for `well_label` containing a single letter is case sensitive ie. well labels A02 and a02 represent different wells on the plate

Parsing for `well_label` containing two letters is limited to uppercase only ie. AB01 is supported but ab01, Ab01 and aB01 are not supported

The following are the only supported sequence of rows for a plate:

  1. A -> Z and then a -> z
  2. A -> Z and then AA -> AZ

For `well_label` with single letter, even though well labels starting with `w`, `x`, `y`, and `z` are supported by the parser, in real life this is not possible as the largest plate contains `3456 wells` which is `48x72`, so the last well label is going to be `v72`.

Similarly, for `well_label` with two letters, in real life the largest possible `well_label` would be `AV72` for a plate with 3456 wells. However, `well_label` beyond `AV72` are also supported by parser.

## Changelog

### v2.1.0

- Deprecate datetime parsing function `parse()`, replaced by object `DatetimeParser`
- Add `DatetimeParser`
- Update to pendulum 3.0.0 and adapt to breaking changes

### v2.0.1

- Restrict pendulum to `<3.0.0`

### v2.0.0

- Python minimum requirement is now 3.9
- Removed parquet support
- Made dependencies less restrictive

### v1.9.0

- Add `task_script_utils.plate_reader.WellPosition.to_label` for converting a `WellPosition` to a well label
- Add `task_script_utils.plate_reader.create_well_to_pk_map` for creating a map of `WellPosition` to primary keys from a list of samples

### v1.8.1

- Update to python dependency to >=3.7.2,<4

### v1.8.0

- Add `task_script_utils.plate_reader.WellPosition` for parsing well labels
- Update `task_script_utils.random.Singleton` used by `TaskScriptUUIDGenerator` and rename to `task_script_utils.random.CacheLast`
  - `CacheLast` no longer provides singleton behavior, but it still provides the method `get_last_created`
  - Instantiating `TaskScriptUUIDGenerator` always seeds the random generator. A second instance will repeat the same sequence of UUIDs as the first instance (if instantiated with the same arguments).
  - Rename `NoPreviouslyCreatedSingletonError` to `NoPreviouslyCreatedInstanceError`
  - Add type information to `get_last_created`

### v1.7.0

- Add `task_script_utils.workflow_logging` for logging warning messages in task scripts

### v1.6.0

- Add `task_script_utils.datacubes.parquet` for creating Parquet file representations of datacubes

### v1.5.0

- Add `TaskScriptUUIDGenerator` class for generating random UUIDs and random bytes.

### v1.4.0

- Add `extract-to-decorate` functions

### v1.3.1

- Update datetime parser usage in README.md

### v1.3.0

- Added string parsing functions

### v1.2.0

- Add boolean config parameter `require_unambiguous_formats` to `DatetimeConfig`
- Add logic to `parser._parse_with_formats` to be used when `DatetimeConfig.require_unambiguous_formats` is set to `True`
  - `AmbiguousDatetimeFormatsError` is raised if mutually ambiguous formats are detected and differing datetimes are parsed
- Add parameter typing throughout repository
- Refactor `datetime_parser` package
- Add base class `DateTimeInfo`
- Segregate parsing logic into `ShortDateTimeInfo` and `LongDateTimeInfo`

### v1.1.1

- Remove `convert_to_ts_iso8601()` method

### v1.1.0

- Add `datetime_parser` package
