import json
import uuid
from pathlib import Path
from typing import Any, Dict, Iterable

DATA_FILE = Path("mm.json")


class Item:
    def __init__(self, uuid_: str, properties: Dict[str, Any], tags: set[str]):
        self.uuid = uuid_
        self.properties = properties
        self.tags = set(tags)

    def to_dict(self):
        return {
            "uuid": self.uuid,
            "properties": self.properties,
            "tags": list(self.tags),
        }

    @staticmethod
    def from_dict(d):
        return Item(d["uuid"], d["properties"], set(d.get("tags", [])))


def _load_data() -> dict:
    if not DATA_FILE.exists():
        return {}

    with DATA_FILE.open("r", encoding="utf-8") as f:
        return json.load(f)


def _save_data(data: dict):
    with DATA_FILE.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def create_item(properties: dict, tags: set[str]) -> Item:
    data = _load_data()
    uuid_ = str(uuid.uuid4())

    item = Item(uuid_, properties, tags)
    data[uuid_] = item.to_dict()
    _save_data(data)

    return item


def get_item(uuid_: str) -> Item | None:
    data = _load_data()

    if uuid_ not in data:
        return None

    return Item.from_dict(data[uuid_])


def update_item(
    uuid_: str, properties: dict | None = None, tags: set[str] | None = None
) -> Item | None:
    data = _load_data()

    if uuid_ not in data:
        return None

    item = Item.from_dict(data[uuid_])

    if properties:
        item.properties.update(properties)

    if tags:
        item.tags.update(tags)

    data[uuid_] = item.to_dict()
    _save_data(data)

    return item


def delete_item(uuid_: str) -> bool:
    data = _load_data()

    if uuid_ not in data:
        return False

    del data[uuid_]
    _save_data(data)
    return True


def list_items(filters: dict = None) -> Iterable[Item]:
    data = _load_data()

    for item_dict in data.values():
        item = Item.from_dict(item_dict)

        if filters:
            match = True

            for k, v in filters.items():
                if k == "tags":
                    if not set(v).issubset(item.tags):
                        match = False
                        break
                else:
                    if item.properties.get(k) != v:
                        match = False
                        break
            if not match:
                continue
        yield item
