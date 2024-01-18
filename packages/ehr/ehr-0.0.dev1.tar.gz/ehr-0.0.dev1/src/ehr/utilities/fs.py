import os
import pathlib as pl


__all__ = [
    "list_nested_files",
]


def filename(path: str):
    return pl.Path(path).name


def list_files(path, full_path=True):
    filenames = [fn for fn in os.listdir(path) if os.path.isfile(os.path.join(path, fn))]

    return [os.path.join(path, fn) for fn in filenames] if full_path else filenames


def list_nested_files(top, fn_includes: list[str] = None, fn_excludes: list[str] = None, full_path=True, **kwargs):
    file_paths = []
    for top, dirnames, files in os.walk(top, **kwargs):
        for fn in files:
            # when it doesn't meet any filter condition, skip to next
            if fn_includes:
                if not any(kw in fn for kw in fn_includes):
                    continue
            if fn_excludes:
                if any(kw in fn for kw in fn_excludes):
                    continue

            # when it passes all filters
            file_paths.append(os.path.join(top, fn))

    return file_paths if full_path else [filename(fp) for fp in file_paths]


if __name__ == "__main__":
    test_path = "/Users/san/ds/datasets/physionet.org/files/mimiciv/2.2"
    print(list_files(test_path))
    print(list_nested_files(test_path))
