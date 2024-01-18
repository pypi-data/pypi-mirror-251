# trainlog

Nice colorful logging module, which also includes an extra level TRAIN for model train etc.

```py
from trainerlog import get_logger

logger = get_logger(name="ebun", level="DEBUG")

logger.train("Training step complete")
logger.debug("this is just a debug message")
logger.info("This is supposed to be more important")
logger.warning("Somethings maybe not right")
logger.error("Something went wrong")
logger.critical("Something went very wrong")
```

![](https://gitlab.com/ninpnin/trainlog/-/raw/main/example.png)