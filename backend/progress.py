import threading

_progress_state = {
    "is_running": False,
    "percent": 0,
    "message": "",
    "time_remaining": 0
}
_lock = threading.Lock()

def update_progress(is_running: bool = None, percent: int = None, message: str = None, time_remaining: int = None):
    with _lock:
        if is_running is not None:
            _progress_state["is_running"] = is_running
        if percent is not None:
            _progress_state["percent"] = percent
        if message is not None:
            _progress_state["message"] = message
        if time_remaining is not None:
            _progress_state["time_remaining"] = time_remaining

def get_progress():
    with _lock:
        return _progress_state.copy()
