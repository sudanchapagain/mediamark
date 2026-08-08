from void.storage import Item


class Suggestion:
    def __init__(self, description: str, key: str, value, optional=True):
        self.description = description
        self.key = key
        self.value = value
        self.optional = optional


def analyze_item(item: Item) -> list[Suggestion]:
    suggestions = []

    url = item.properties.get("url") or item.properties.get("value")
    if url and "youtube.com" in url:
        if "youtube_video" not in item.tags:
            suggestions.append(
                Suggestion("Tag as youtube_video", "tags", "youtube_video")
            )

    return suggestions


def resolve(item: Item, suggestions: list[Suggestion], accept_all: bool = True) -> Item:
    for s in suggestions:
        if accept_all or s.optional:
            if s.key == "tags":
                item.tags.add(s.value)
            else:
                item.properties[s.key] = s.value
    return item
