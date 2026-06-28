# Legacy wrapper — prefer calling ui.py directly from Python.
# python -c "import sys; sys.path.insert(0,'D:/ai-workstation/scripts'); from ui import click; click(500, 400)"
param([int]$X, [int]$Y)
python -c "import sys; sys.path.insert(0,'D:/ai-workstation/scripts'); from ui import click; click($X, $Y); print('clicked ($X, $Y)')"
