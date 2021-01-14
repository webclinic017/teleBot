import time
from datetime import datetime
a = datetime.fromtimestamp(1206723939).strftime("%A, %B %d, %Y %I:%M:%S")
print(str(time.time())[:10])
print(a)
print(time.time())
print(str(datetime.date(datetime.now())).replace('-',''))