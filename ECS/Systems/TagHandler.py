class TagHandler():
    _tags = []

    @staticmethod
    def add_tag(_, tag):
        if tag in TagHandler._tags:
            raise ValueError(f"Tag '{tag}' already exists")
        TagHandler._tags.append(tag)

    @staticmethod
    def remove_tag(tag):
        TagHandler._tags.remove(tag)