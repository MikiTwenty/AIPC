from pathlib import Path

import aipc
from pprint import pprint
from aipc import VisionModel


def main():
    aipc.init(verbose=True)
    images_folder = Path("C:/Users/mikiv/Pictures/People")
    model = VisionModel()
    model.process_images(images_folder)
    pprint(model.qdrant_db.search(input("Search image: ")))


if __name__ == "__main__":
    main()