import os
import pickle
import time


def checkpoint(temp_path):
    if os.path.isdir(temp_path):
        temp_path = os.path.join(temp_path, "temp.pkl")

    def _checkpoint(func):
        def wrapper(*args, **kwargs):
            if os.path.exists(temp_path):
                with open(temp_path, "rb") as f:
                    temp_data = pickle.load(f)
            else:
                temp_data = func(*args, **kwargs)
                with open(temp_path, "wb") as f:
                    pickle.dump(temp_data, f)
            return temp_data

        return wrapper

    return _checkpoint


def functimer(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__}:{end_time - start_time}s")
        return result

    return wrapper
