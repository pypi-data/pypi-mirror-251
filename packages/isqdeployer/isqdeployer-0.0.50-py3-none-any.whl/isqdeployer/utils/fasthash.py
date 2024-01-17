import hashlib



def fasthash(string):
    return hashlib.md5(string.encode("utf-8")).hexdigest()

