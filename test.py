import datetime

now = datetime.datetime.now(datetime.timezone.utc).strftime(
    "%Y-%m-%d %H:%M:%S"
)

import time

print(now)
time.sleep(2)
print(now)
