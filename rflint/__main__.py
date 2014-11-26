import sys
from rflint import RfLint

app = RfLint()
app.run(sys.argv[1:])
