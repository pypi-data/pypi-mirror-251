# auro_utils

Auro Utils is a utility toolkit, providing enhanced logging, performance profiling, etc.

## Install

### Install from pip

```bash
pip install auro_utils
```

### Install from source

```bash
git clone https://github.com/Auromix/auro_utils
cd auro_utils
pip install -e .
```

## Test

```bash
cd auro_utils
python3 -m pytest -v .
```

## Usage

Following are some simplified examples of utilities offered by this package.

You can also find detailed examples in the `examples` folder.

```bash
cd auro_utils/examples
```

## Loggers

### logger

Logger is a class that can be used to log messages to the console and to a file. It is a wrapper around loguru.

```python
from auro_utils.loggers.logger import Logger
my_logger = Logger()
my_logger.log_info("This is a info log test.")
```

![logger_cmd](/assets/images/loggers/logger_cmd.png)

### classic logger

Classic logger is a class that can be used to log messages to the console and to a file. It is a wrapper around the standard python logging module.

```python
from auro_utils.loggers.logger_classic import Logger
my_logger = Logger()
my_logger.log_info("This is a info log test.")
```

## Profilers

### profiler

Decorator for profiling and analyzing performance of functions. It is a wrapper around yappi.

```python
from auro_utils.profilers.profiler import auro_profiler
@auro_profiler
def your_function_code():
    import time
    time.sleep(2)
```

![profiler_cmd](/assets/images/profilers/profiler_cmd.png)

![profiler_web](/assets/images/profilers/profile_results.png)

## Troubleshooting

### ModuleNotFoundError

Make sure you have installed the package correctly. See [Install](#install) section.

### Want to uninstall

```bash
pip uninstall auro_utils
```

## Contribute

Please refer to [CONTRIBUTING.md](CONTRIBUTING.md) for more information.
