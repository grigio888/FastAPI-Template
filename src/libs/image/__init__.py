"""
Image - Index.
"""

from __future__ import annotations

import base64
import io
import sys
import uuid
from pathlib import Path

from fastapi import UploadFile
from PIL import Image
from starlette.datastructures import UploadFile as StarletteUploadFile

from src.libs.image.errors import ImageTooLargeError, InvalidImageError
from src.libs.log import get_context as _
from src.libs.log import get_logger

log = get_logger()


class ImageHandler:
    """
    Upload class to handle image uploads.
    """

    def __init__(
        self,
        file: UploadFile | StarletteUploadFile | bytes | str | io.BytesIO,
        path: Path | str,
    ) -> None:
        """
        # Initialize the class.

        ---

        The file to be handled can be it a UploadFile, a data URI (base64) or a bytes
        object.

        Args:
            file (UploadFile | StarletteUploadFile | bytes | str | io.BytesIO):
                The file to be handled.
            path (Path | str): The path to save the file.

        """

        log.info(f"{_()}: Initializing ImageHandler")

        self.path = self._parse_path(path)
        self.original_file = file

        self.file = self._return_image_object(file)

    # -- Misc -- #
    @staticmethod
    def _parse_path(path: Path | str) -> Path:
        """
        # Parse the path.

        This method will parse the path to a Path object.

        ---

        Args:
            path (Path | str): The path to be parsed.

        Returns:
            Path: The parsed path.

        ---

        Usage:
        ```python
        path = ImageHandler._parse_path("/path/to/directory")

        print(path)  # Path("/path/to/directory")

        """

        log.info(f"{_()}: Parsing path")

        if isinstance(path, str):
            log.debug(f"{_()}: Path is string")
            return Path(path)

        log.debug(f"{_()}: Path is Path object")
        return path

    # --------------- FILE HANDLING ----------------- #
    @staticmethod
    def _validate_format(
        file: UploadFile | StarletteUploadFile | bytes | str | io.BytesIO,
    ) -> None:
        """
        # Validate the file.

        This method will validate the file format to be handled.
        """

        log.info(f"{_()}: Validating image")

        if isinstance(file, str):
            log.debug(f"{_()}: Image is base64")

            if not file.startswith("data:image"):
                raise InvalidImageError

        elif isinstance(file, bytes):
            log.debug(f"{_()}: Image is bytes")

        elif isinstance(file, UploadFile | StarletteUploadFile):
            log.debug(f"{_()}: Image is UploadFile")

            if not file.content_type or not file.content_type.startswith("image/"):
                raise InvalidImageError

        elif isinstance(file, io.BytesIO):
            log.debug(f"{_()}: Image is BytesIO")

    @staticmethod
    def _get_binary_data(
        file: UploadFile | StarletteUploadFile | bytes | str | io.BytesIO,
    ) -> io.BytesIO:
        """
        # Get the binary data from the file.

        This method will convert the file to a bytes object.
        """

        log.info(f"{_()}: Getting binary data from file")
        log.debug(f"{_()}: File type: {type(file)}")

        if isinstance(file, bytes):
            log.debug(f"{_()}: Image is bytes")

            return io.BytesIO(file)

        if isinstance(file, str):
            log.debug(f"{_()}: Image is base64")

            image_data = base64.b64decode(file.split(";base64,")[1])

            return io.BytesIO(image_data)

        if isinstance(file, UploadFile | StarletteUploadFile):
            log.debug(f"{_()}: Image is UploadFile")

            return io.BytesIO(file.file.read())

        if isinstance(file, io.BytesIO):
            log.debug(f"{_()}: Image is BytesIO")
            file.seek(0)
            return file

        log.error(f"{_()}: Invalid file type")

        raise InvalidImageError

    @staticmethod
    def _validate_size(file: io.BytesIO) -> None:
        """
        # Validate the file.

        This method will validate the file size to be handled.
        The file must be a image and the size must be less than 10MB.
        """

        size = sys.getsizeof(file)

        log.info(f"{_()}: Validating image size")
        log.debug(f"{_()}: Image size: {(size / 1024):.2f} KB")

        mb_convert = 1024 * 1024

        if size > 10 * mb_convert:
            filesize = size / mb_convert
            raise ImageTooLargeError(size=int(filesize))

    def _return_image_object(
        self,
        file: UploadFile | StarletteUploadFile | bytes | str | io.BytesIO,
    ) -> Image:  # type: ignore[return]
        """
        # Return the image object.

        This method will be a pipeline that will:
        - Validate the file type.
        - Validate the file size.
        - Convert the file into a binary object.

        ---

        Args:
            file (UploadFile | StarletteUploadFile | bytes | str):
                The file to be handled.

        Returns:
            Image: The image object.

        """

        log.info(f"{_()}: Getting image object")

        self._validate_format(file)
        binary_file: io.BytesIO = self._get_binary_data(file)
        self._validate_size(binary_file)

        return Image.open(binary_file)  # type: ignore[return]

    # -------------- TOOLS ----------------- #
    def _create_unique_name(
        self,
        extension: str | None = None,
    ) -> str:
        """
        # Create a unique name for the file.

        This method will create a unique name for the file to be handled.
        The name will be a UUID4 string to avoid collisions.

        ---

        Args:
            extension (str | None): The file extension. If not passed, the method
            will retrieve the extension from the original file.

        Returns:
            str: The unique name for the file.

        """

        name = str(uuid.uuid4())

        log.debug(f"{_()}: Unique name: {name}")

        if extension:
            unique_name = f"{name}.{extension}"
            log.debug(f"{_()}: Returning: {unique_name}")

            return f"{name}.{extension}"

        extension = self._retrieve_file_extension(self.original_file)
        unique_name = f"{name}.{extension}"
        log.debug(f"{_()}: Returning: {unique_name}")

        return unique_name

    @staticmethod
    def _retrieve_file_extension(
        file: UploadFile | StarletteUploadFile | bytes | str | io.BytesIO,
    ) -> str:
        """
        Retrieve the file extension.

        This method will retrieve the file extension from the file.
        """

        log.info(f"{_()}: Retrieving file extension")

        if isinstance(file, bytes):
            log.debug(f"{_()}: Cannot retrieve file extension from bytes")
            return "webp"

        if isinstance(file, str):
            log.debug(f"{_()}: Retrieve file extension from base64")
            return file.split(";base64,")[0].split("/")[1]

        if isinstance(file, UploadFile | StarletteUploadFile):
            log.debug(f"{_()}: Retrieve file extension from UploadFile")
            return str(Path(file.filename).suffix).strip(".")

        if isinstance(file, io.BytesIO):
            log.debug(f"{_()}: Cannot retrieve file extension from BytesIO")
            return "webp"

        raise InvalidImageError

    # -------------- IMAGE MANIPULATION ----------------- #
    @staticmethod
    def _resize(
        image: Image,
        width: int | None = None,
        height: int | None = None,
    ) -> Image:
        """
        # Resize the image.

        This internal method will resize the image to the width and height passed.
        Both parameters are optional, but one of them must be passed in order to
        resize the image.

        - If only width is passed, the image will be resized proportionally.
        - If only height is passed, the image will be resized proportionally.
        - If both are, the image will be resized to the width and height passed.

        ---

        Args:
            image (Image): The image to be resized.
            width (int | None): The width to resize the image to.
            height (int | None): The height to resize the image to.

        Returns:
            Image: The resized image.

        """

        log.info(f"{_()}: Resizing image")

        assert width or height, "You must pass at least one parameter"

        if width and height:
            log.debug(f"{_()}: Resizing image to: {width}x{height}")
            return image.resize((width, height))

        log.debug(f"{_()}: Calculating aspect ratio")
        aspect_ratio = image.width / image.height
        log.debug(f"{_()}: Aspect ratio: {aspect_ratio}")

        if width:
            log.debug(f"{_()}: Resizing image to: {width}x{int(width / aspect_ratio)}")
            return image.resize((width, int(width / aspect_ratio)))

        log.debug(f"{_()}: Resizing image to: {int(height * aspect_ratio)}x{height}")
        return image.resize((int(height * aspect_ratio), height))

    def resize(
        self,
        width: int | None = None,
        height: int | None = None,
    ) -> None:
        """
        # Resize the image in self.file.

        This method is the same as the _resize method, but it operates on self.file.
        Useful when you're not dealing with multiple frames and just want to resize
        the image stored in self.file.

        ---

        Args:
            width (int | None): The width to resize the image to.
            height (int | None): The height to resize the image to.

        """

        log.info(f"{_()}: Resizing image in self.file")

        self.file = self._resize(
            self.file,
            width=width,
            height=height,
        )

    # # ---------------------- IO ------------------------- #
    async def preprocess(
        self,
        file: Image,
        size: dict = {},
    ) -> tuple[Image, list[Image]]:
        """
        # Process the file.

        This method will process the file to be saved to the path specified
        in the constructor.

        ---

        Args:
            file (Image): The image to be processed.
            size (dict): The size to resize the image to.
                Default is {} (no resize).

        Returns:
            str: The filename of the file saved.

        """

        log.info(f"{_()}: Processing image.")

        image = file
        log.debug(f"{_()}: Image object: {image}")
        log.debug(f"{_()}: Image size: {image.size}")
        log.debug(f"{_()}: Image format: {image.format}")

        frames = [image.copy()]
        try:
            while True:
                log.debug(f"{_()}: Dealing with frame {len(frames)}")

                image.seek(image.tell() + 1)
                frames.append(image.copy())

        except EOFError:
            log.error(f"{_()}: Reached end of frames.")  # noqa: TRY400

        if size:
            log.debug(f"{_()}: Resizing image to: {size}")

            for frame_index, frame in enumerate(frames):
                frames[frame_index] = self._resize(frame, **size)

            # Keep the base frame consistent with the resized frames to avoid WebP
            # errors caused by mismatched dimensions between the first frame and
            # the appended frames.
            image = frames[0]

        log.debug(f"{_()}: Image size after resize: {frames[0].size}")

        log.debug(f"{_()}: Rewind image dataframes, if any.")

        image.seek(0)

        return image, frames

    async def save(
        self,
        extension: str = "webp",
        size: dict = {},
        quality: int = 100,
        custom_name: str | None = None,
    ) -> str:
        """
        # Save the file.

        This method will save the file to the path specified in the constructor.

        The method consists in:
        - Create a unique name for the file
        - Defining a extension (default is webp for perfomance).
        - Resize the image if size is passed.
        - Save the image to the path specified in the constructor.

        Return the filename of the file saved.

        ---

        Args:
            extension (str): The file extension. Default is webp.
            size (dict): The size to resize the image to.
                Default is {} (no resize).
            quality (int): The quality of the image. Default is 100.
            custom_name (str | None): Custom name for the file.
                If not passed, a unique name will be created.

        Returns:
            str: The filename of the file saved.

        """

        log.info(f"{_()}: Saving image")

        if custom_name:
            filename = f"{custom_name}.{extension}"
            log.debug(f"{_()}: Custom name: {filename}")
        else:
            # Detect if the image has extension of .gif
            if self.file.format and self.file.format.lower() == "gif":
                extension = "gif"

            filename = self._create_unique_name(extension=extension)

        base_path = self.path
        path = base_path / filename
        log.debug(f"{_()}: Destination path: {path}")

        log.debug(f"{_()}: Verifying path: {path}")
        if not path.parent.exists():
            log.debug(f"{_()}: Path does not exist. Creating it.")
            path.parent.mkdir(parents=True, exist_ok=True)

        image, frames = await self.preprocess(file=self.file, size=size)

        try:
            image.save(
                path,
                save_all=True,
                append_images=frames,
                loop=0,
                optimize=True,
                quality=quality,
            )
        except Exception:
            log.exception(f"{_()}: Error while saving image.")
            raise

        return filename

    async def return_as_uploadfile(
        self,
        extension: str = "webp",
        size: dict = {},
        quality: int = 100,
        custom_name: str | None = None,
    ) -> UploadFile:
        """
        # Return the file as UploadFile.

        This method will return the file as UploadFile.

        The method consists in:
        - Create a unique name for the file
        - Defining a extension (default is webp for perfomance).
        - Resize the image if size is passed.
        - Return the image as UploadFile.

        ---

        Args:
            extension (str): The file extension. Default is webp.
            size (dict): The size to resize the image to.
                Default is {} (no resize).
            quality (int): The quality of the image. Default is 100.
            custom_name (str | None): Custom name for the file.
                If not passed, a unique name will be created.

        Returns:
            UploadFile: The file as UploadFile.

        """

        log.info(f"{_()}: Returning image as UploadFile")

        extension = (extension or "webp").lower()

        if custom_name:
            filename = f"{custom_name}.{extension}"
            log.debug(f"{_()}: Custom name: {filename}")
        else:
            filename = self._create_unique_name(extension=extension)

        _image, frames = await self.preprocess(file=self.file, size=size)

        primary_frame = frames[0]
        byte_array = io.BytesIO()

        save_kwargs = {
            "format": extension.upper(),
            "optimize": True,
        }
        if quality is not None and extension not in {"png"}:
            save_kwargs["quality"] = quality

        if len(frames) > 1:
            primary_frame.save(
                byte_array,
                save_all=True,
                append_images=frames[1:],
                loop=0,
                **save_kwargs,
            )
        else:
            primary_frame.save(byte_array, **save_kwargs)

        byte_array.seek(0)

        return UploadFile(
            filename=filename,
            file=byte_array,
        )

    @classmethod
    def delete_other_file(cls, file_path: str) -> None:
        """
        # Delete the file from the folder.

        Helper method to remove a file from a path.
        Commonly used to remove the previous file when uploading a new one.

        ---

        Args:
            file_path (str): The path of the file to be deleted.

        """

        log.info(f"{_()}: Finding file to delete.")

        file = Path(file_path)

        if file.exists():
            log.debug(f"{_()}: File found.")
            log.debug(f"{_()}: Deleting file: {file}")
            file.unlink()
        else:
            log.debug(f"{_()}: File not found.")
