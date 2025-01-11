from pathlib import Path

import aipc
from aipc import LLaVA


def main():
    aipc.init(verbose=True)
    images_folder = Path("C:/Users/mikiv/Pictures/People")  # Replace with your folder path
    captioner = LLaVA()
    captioner.process_images(images_folder)

if __name__ == "__main__":
    main()