import argparse
from void import storage
from core import resolution


def cmd_add(args):
    props = {}
    tags = set()

    if args.value:
        props["value"] = args.value

    if args.props:
        for p in args.props:
            if "=" in p:
                k, v = p.split("=", 1)
                props[k] = v

    if args.tag:
        tags.update(args.tag.split(","))

    item = storage.create_item(props, tags)

    suggestions = resolution.analyze_item(item)
    if suggestions and not args.skip:
        print("Suggestions:")
        for idx, s in enumerate(suggestions, 1):
            print(f"{idx}. {s.description}")
        answer = input("Apply all? [y/N]: ").lower()
        if answer in ("y", "yes"):
            item = resolution.resolve(item, suggestions)

    storage.update_item(item.uuid, item.properties, item.tags)

    print(f"Item created: {item.uuid}")


def cmd_list(args):
    filters = {}
    if args.tag:
        filters["tags"] = args.tag.split(",")
    for item in storage.list_items(filters):
        print(
            f"{item.uuid} | {item.properties.get('value', '')} | tags: {','.join(item.tags)}"
        )


def main():
    parser = argparse.ArgumentParser(prog="mm")
    sub = parser.add_subparsers(dest="cmd")

    add_parser = sub.add_parser("add")
    add_parser.add_argument("value", nargs="?")
    add_parser.add_argument("--tag", "-t")
    add_parser.add_argument("--skip", action="store_true")
    add_parser.add_argument("props", nargs="*")
    add_parser.set_defaults(func=cmd_add)

    list_parser = sub.add_parser("list")
    list_parser.add_argument("--tag", "-t")
    list_parser.set_defaults(func=cmd_list)

    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
