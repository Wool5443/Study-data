"""Universal input and output functions for the shelter project."""

from pathlib import Path

import pandas as pd


def load_excel_tables(file_path: str | Path) -> dict[str, pd.DataFrame]:
    """
    Load all MS Excel workbook sheets as database reference tables.

    Parameters
    ----------
    file_path : str | Path
        Path to an MS Excel workbook.

    Returns
    -------
    dict[str, pandas.DataFrame]
        Dictionary where keys are sheet names and values are
        pandas.DataFrame tables.
    """
    tables = pd.read_excel(file_path, sheet_name=None)
    return {name: frame.dropna(how="all") for name, frame in tables.items()}


def save_pickle_tables(
    tables: dict[str, pd.DataFrame],
    data_dir: str | Path,
) -> list[Path]:
    """
    Save database reference tables in pickle format.

    Parameters
    ----------
    tables : dict[str, pandas.DataFrame]
        Database tables.
    data_dir : str | Path
        Directory for pickle files.

    Returns
    -------
    list[pathlib.Path]
        Paths to created pickle files.
    """
    data_path = Path(data_dir)
    data_path.mkdir(parents=True, exist_ok=True)
    saved_paths = []
    for name, frame in tables.items():
        path = data_path / f"{name}.pick"
        frame.to_pickle(path)
        saved_paths.append(path)
    return saved_paths


def load_pickle_tables(data_dir: str | Path) -> dict[str, pd.DataFrame]:
    """
    Load all database tables from pickle files in a directory.

    Parameters
    ----------
    data_dir : str | Path
        Directory with ``.pick`` files.

    Returns
    -------
    dict[str, pandas.DataFrame]
        Dictionary where keys are file names without extensions and values are
        pandas.DataFrame tables.
    """
    data_path = Path(data_dir)
    tables = {}
    for path in sorted(data_path.glob("*.pick")):
        tables[path.stem] = pd.read_pickle(path)
    return tables


def save_table_report(
    report: pd.DataFrame,
    output_dir: str | Path,
    file_name: str,
) -> Path:
    """
    Save a text report to an MS Excel file.

    Parameters
    ----------
    report : pandas.DataFrame
        Report table.
    output_dir : str | Path
        Directory for text reports.
    file_name : str
        Output file name without extension.

    Returns
    -------
    pathlib.Path
        Path to the created report file.
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    report_path = output_path / f"{file_name}.xlsx"
    report.to_excel(report_path, index=False)
    return report_path
