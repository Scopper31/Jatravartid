from utilities.string_utilities import *
from utilities.system_utilities import *

sss = """- Remember to test the updated code thoroughly to ensure it functions as expected. 

Devops_req_terminal_response:
```python
#FILE_REQ_START
pygame
#FILE_REQ_END
```

```bash
#TERMINAL_START
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
#TERMINAL_END
``` 

create_file:"""
requirements = extract_blocks(sss, "#FILE_REQ_START", "#FILE_REQ_END")
print(requirements)
