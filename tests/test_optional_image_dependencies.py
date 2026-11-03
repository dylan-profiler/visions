import subprocess
import sys

from PIL import Image

from visions.utils.images.image_utils import extract_exif, hash_image, open_image

# None in sys.modules makes `import x` raise ModuleNotFoundError, which is what a
# plain `pip install visions` looks like without the type_image_path extra.
HIDE_IMAGE_EXTRA = (
    "import sys; sys.modules['PIL'] = None; sys.modules['imagehash'] = None; "
)


def run_without_image_extra(code: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, "-c", HIDE_IMAGE_EXTRA + code],
        capture_output=True,
        text=True,
    )


def test_import_visions_without_image_extra():
    result = run_without_image_extra("import visions")
    assert result.returncode == 0, result.stderr


def test_image_helpers_name_the_missing_module_when_called():
    code = (
        "from visions.utils.images.image_utils import open_image; "
        "open_image('missing.png')"
    )
    result = run_without_image_extra(code)
    assert result.returncode != 0
    assert "PIL" in result.stderr


def test_image_helpers_work_with_image_extra(tmp_path):
    path = tmp_path / "image.png"
    Image.new("RGB", (8, 8)).save(path)

    image = open_image(path)

    assert image.size == (8, 8)
    assert isinstance(hash_image(image), str)
    assert extract_exif(image) == {}
