# Legacy wrapper — prefer calling ui.py directly from Python.
# python -c "import sys; sys.path.insert(0,'D:/ai-workstation/scripts'); from ui import click, paste_text; click(X,Y); paste_text('...')"
param([int]$ClickX, [int]$ClickY, [string]$Message)
python -c "
import sys; sys.path.insert(0,'D:/ai-workstation/scripts')
from ui import click, paste_text
click($ClickX, $ClickY)
paste_text('''$($Message.Replace("'","\'"))''')
print('done')
"
