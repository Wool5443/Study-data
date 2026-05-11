"""Main script for homework 02 report generation."""

from configparser import ConfigParser
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]

import pandas as pd

LIBRARY_DIR = BASE_DIR / "library"
SCRIPTS_DIR = BASE_DIR / "scripts"

from library.io_tools import (  # noqa: E402
    load_pickle_tables,
    save_pickle_tables,
    save_table_report,
)
from scripts.reports import (  # noqa: E402
    pivot_species_status,
    plot_age_stay_scatter,
    plot_medical_diagnosis_bar,
    plot_species_status_bar,
    plot_volunteer_task_type_bar,
    report_animals_attention_list,
    report_volunteer_workload_summary,
    statistics_report,
)


def read_config(config_path: str | Path) -> ConfigParser:
    """
    Read application settings from an INI file.

    Parameters
    ----------
    config_path : str | Path
        Path to the settings file.

    Returns
    -------
    configparser.ConfigParser
        Loaded configuration object.
    """
    config = ConfigParser()
    config.read(config_path, encoding="utf-8")
    return config


def prepare_database(config: ConfigParser) -> dict:
    """
    Load database pickle files or create them from Excel.

    Parameters
    ----------
    config : configparser.ConfigParser
        Application settings.

    Returns
    -------
    dict
        Database tables loaded from pickle files.
    """
    data_dir = BASE_DIR / config["paths"]["data_dir"]
    pickle_files = list(data_dir.glob("*.pick"))
    if pickle_files:
        return load_pickle_tables(data_dir)

    excel_path = data_dir / config["paths"]["excel_file"]
    tables = pd.read_excel(excel_path, sheet_name=None)
    save_pickle_tables(tables, data_dir)
    return load_pickle_tables(data_dir)


def build_text_reports(config: ConfigParser, tables: dict) -> list[Path]:
    """
    Build all text reports and save them to files.

    Parameters
    ----------
    config : configparser.ConfigParser
        Application settings.
    tables : dict
        Database tables loaded from pickle files.

    Returns
    -------
    list[pathlib.Path]
        Paths to created text reports.
    """
    output_dir = BASE_DIR / config["paths"]["output_dir"]
    output_dir.mkdir(parents=True, exist_ok=True)

    for path in output_dir.glob("*.xlsx"):
        path.unlink()

    reports = {
        "animals_attention_list": report_animals_attention_list(tables),
        "volunteer_workload_summary": report_volunteer_workload_summary(tables),
        "shelter_statistics": statistics_report(tables),
        "pivot_species_status": pivot_species_status(tables),
    }
    return [
        save_table_report(report, output_dir, name) for name, report in reports.items()
    ]


def build_graphic_reports(config: ConfigParser, tables: dict) -> list[Path]:
    """
    Build all graphic reports and save them to files.

    Parameters
    ----------
    config : configparser.ConfigParser
        Application settings.
    tables : dict
        Database tables loaded from pickle files.

    Returns
    -------
    list[pathlib.Path]
        Paths to created graphic files.
    """
    graphics_dir = BASE_DIR / config["paths"]["graphics_dir"]
    graphics_dir.mkdir(parents=True, exist_ok=True)
    for path in graphics_dir.glob("*.png"):
        path.unlink()

    return [
        plot_species_status_bar(tables, graphics_dir),
        plot_age_stay_scatter(tables, graphics_dir),
        plot_volunteer_task_type_bar(tables, graphics_dir),
        plot_medical_diagnosis_bar(tables, graphics_dir),
    ]


def main() -> None:
    """
    Run database preparation and report generation.

    Returns
    -------
    None
        The function prints paths to created files.
    """
    config = read_config(SCRIPTS_DIR / "config.ini")
    tables = prepare_database(config)
    text_paths = build_text_reports(config, tables)
    graphic_paths = build_graphic_reports(config, tables)

    print("Text reports:")
    for path in text_paths:
        print(path)
    print("Graphic reports:")
    for path in graphic_paths:
        print(path)


if __name__ == "__main__":
    main()
