# Legacy wrapper — prefer calling ui.py directly from Python.
# python -c "import sys; sys.path.insert(0,'C:/Users/1/scripts'); from ui import bring_window_to_front; bring_window_to_front('Teams')"
python -c "import sys; sys.path.insert(0,'C:/Users/1/scripts'); from ui import bring_window_to_front; r=bring_window_to_front('Teams'); print('ok' if r else 'not found')"
