import uuid

class IDGen:
    id: int = 0

    @classmethod
    def new_id(cls) -> int:
        cls.id += 1
        return cls.id

    @staticmethod
    def new_uuid() -> str:
        return str(uuid.uuid4())

    @classmethod
    def reset(cls):
        cls.id = 0