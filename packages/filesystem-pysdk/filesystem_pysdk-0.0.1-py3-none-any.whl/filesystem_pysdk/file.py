class File(object):
    def __init__(self, bucket: str, key: str, duration: int = 0):
        self.bucket = bucket
        self.key = key
        self.duration = duration
        pass

    def __str__(self) -> str:
        return f"File:{{bucket {self.bucket}, Key: {self.key}, Duration: {self.duration}}}"

    def to_dict(self) -> dict:
        return {"bucket": self.bucket, "key": self.key, "duration": self.duration}
