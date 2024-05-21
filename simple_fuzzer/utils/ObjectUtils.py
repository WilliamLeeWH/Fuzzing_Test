import hashlib
import pickle


def dump_object(path: str, data):
    with open(path, 'wb') as f:
        pickle.dump(data, f)


def load_object(path: str):
    with open(path, 'rb') as f:
        return pickle.load(f)


def get_md5_of_object(obj):
    serialized_obj = pickle.dumps(obj)
    md5_hash = hashlib.md5()
    md5_hash.update(serialized_obj)
    return md5_hash.hexdigest()
