# Legacy wrapper — prefer calling ui.py directly from Python.
# python -c "import sys; sys.path.insert(0,'C:/Users/1/scripts'); from ui import screenshot; print(screenshot())"
param([string]$OutputPath = "")
$cmd = if ($OutputPath) { "screenshot('$OutputPath')" } else { "screenshot()" }
python -c "import sys; sys.path.insert(0,'C:/Users/1/scripts'); from ui import screenshot; print($cmd)"
