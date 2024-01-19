# type: ignore
# Copyright (c) dlup contributors
from typing import Any, TypedDict

import h5py
import numpy as np
import PIL.Image
import tifffile

from dlup.backends.common import AbstractSlideBackend, numpy_to_pil
from dlup.types import PathLike
from dlup.utils.tifffile_utils import get_tile


def open_slide(filename: PathLike) -> "TifffileSlide":
    """
    Read slide with tifffile.

    Parameters
    ----------
    filename : PathLike
        Path to image.
    """
    return TifffileSlide(filename)


class H5PropertiesDict(TypedDict):
    pass


class TifffileSlide(AbstractSlideBackend):
    """
    Backend for tifffile.
    """

    def __init__(self, filename: PathLike) -> None:
        """
        Parameters
        ----------
        filename : PathLike
            Path to image.
        """
        super().__init__(filename)
        self._h5file = h5py.File(filename, "r")
        self._level_count = 1
        self.__parse_h5_metadata()

    def __parse_h5_metadata(self) -> None:
        self._downsamples.append(1.0)
        self._spacings.append((1.0, 1.0))
        self._shapes.append((0, 0))

    @property
    def properties(self) -> H5PropertiesDict:
        """Metadata about the image as given by the h5 file."""

        properties: H5PropertiesDict = {}

        return properties

    def set_cache(self, cache):
        """Cache for h5 file."""
        raise NotImplementedError

    def read_region(self, coordinates: tuple[int, int], level: int, size: tuple[int, int]) -> PIL.Image.Image:
        """
        Return the best level for displaying the given image level.

        Parameters
        ----------
        coordinates : tuple
            Coordinates of the region in level 0.
        level : int
            Level of the image pyramid.
        size : tuple
            Size of the region to be extracted.

        Returns
        -------
        PIL.Image
            The requested region.
        """
        if level > self._level_count - 1:
            raise RuntimeError(f"Level {level} not present.")

    @property
    def vendor(self) -> None:
        """Returns the scanner vendor. h5s are not vendored."""
        return None

    @property
    def magnification(self) -> int | None:
        """Returns the objective power at which the WSI was sampled."""
        return self._metadata.get("magnification", None)

    def close(self) -> None:
        """Close the underlying h5file"""
        self._h5file.close()
