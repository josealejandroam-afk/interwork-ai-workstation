# Legacy wrapper — prefer calling ui.py directly from Python.
# python -c "import sys; sys.path.insert(0,'D:/ai-workstation/scripts'); from ui import screenshot; print(screenshot())"
param([string]$OutputPath = "")
$cmd = if ($OutputPath) { "screenshot('$OutputPath')" } else { "screenshot()" }
python -c "import sys; sys.path.insert(0,'D:/ai-workstation/scripts'); from ui import screenshot; print($cmd)"
