# Legacy wrapper — prefer calling ui.py directly from Python.
# python -c "import sys; sys.path.insert(0,'D:/ai-workstation/scripts'); from ui import bring_window_to_front; bring_window_to_front('Teams')"
python -c "import sys; sys.path.insert(0,'D:/ai-workstation/scripts'); from ui import bring_window_to_front; r=bring_window_to_front('Teams'); print('ok' if r else 'not found')"
