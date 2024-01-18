import pathlib as pl
import pandas as pd
from dataclasses import dataclass

import ehr.utilities as eu

__all__ = [
    "MIMICMetadata",
]


@dataclass()
class MIMICMetadata:

    # Overview
    dataset_dir = pl.Path.home() / "ds/datasets/physionet.org/files/mimiciv/2.2"
    table_paths = eu.fs.list_nested_files(dataset_dir, fn_includes=[".csv.gz"])
    table_map = {eu.fs.filename(tp).split(".csv.gz")[0]: tp for tp in table_paths}

    patients_path = dataset_dir / "hosp/patients.csv.gz"
