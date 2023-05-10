from pathlib import Path
from typing import Collection, Iterable, TypeVar

from PIL import Image

T = TypeVar('T')


def get_source_path() -> Path:
    """Require the path to the image from user."""
    request_phrase = 'Enter the path to the source image file: \n'

    while True:
        source_path = input(request_phrase)

        if not source_path:
            print('The path is empty!')
            continue

        source_path = Path(source_path)

        if not source_path.exists():
            print('The path does not exist!')
            continue

        return source_path


def get_initial_name() -> str:
    """Require the initial name associated with the image."""
    request_phrase = 'Enter the initial name of the image:\n'

    while True:
        name = input(request_phrase)

        if not name:
            print('The name is empty!')
            continue

        return name


def get_final_name() -> str:
    """Require the final name associated with the image."""
    request_phrase = 'Enter the final name of the image:\n'

    while True:
        name = input(request_phrase)

        if not name:
            print('The name is empty!')
            continue

        return name


def split_img_between_items(img: Image.Image, items: Collection[T]) \
        -> dict[T, Image.Image]:
    """Create a dict with parts of the image with appropriate values.

    Split the image between the first occurrences of each item.

    :param img: The image to be split.
    :param items: The items the image to be split between.

    :result: A dictionary with the items as a key and the parts of the
    split image as appropriate values to the items.

    .. note:: The presence of a key in the dictionary is
    determined by its hash."""
    letters_img_parts_map = {}
    width, height = img.size
    part = height // len(items)

    # Not the highest value but the previous highest point on the image
    upper = 0
    for l in items:
        lower = upper + part
        if l not in letters_img_parts_map:
            letters_img_parts_map[l] = img.crop((0, upper, width, lower))

        upper = lower

    return letters_img_parts_map


def compose_img_from_parts(parts: Iterable[Image.Image]) -> Image.Image:
    """Compose a new image from the different images.

    Generate a new image composed of the specified parts arranged vertically
    one after the other in the original order from top to bottom.

    :param parts: The parts of the new image from which it will be composed.

    :result: The image composed of the specified parts."""
    width = max(p.size[0] for p in parts)
    height = sum(p.size[1] for p in parts)
    # Create the bigger image to fit the rest
    img = Image.new('RGB', (width, height), 'white')

    upper = 0
    for p in parts:
        img.paste(p, (0, upper))
        upper += p.size[1]

    return img


def main():
    source_path = get_source_path()
    initial_name = get_initial_name()
    final_name = get_final_name()

    img = Image.open(source_path)

    letters_img_parts = split_img_between_items(img, initial_name)
    img_parts = [letters_img_parts[l] for l in final_name]
    img = compose_img_from_parts(img_parts)

    img.save(source_path.with_stem(final_name))


if __name__ == '__main__':
    main()
