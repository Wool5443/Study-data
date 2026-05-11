"""Main script for homework 02 report generation."""

from configparser import ConfigParser
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]

import matplotlib
import pandas as pd

matplotlib.use("Agg")

LIBRARY_DIR = BASE_DIR / "library"
SCRIPTS_DIR = BASE_DIR / "scripts"

from library.io_tools import (  # noqa: E402
    load_pickle_tables,
    save_pickle_tables,
    save_table_report,
)
from scripts.reports import (  # noqa: E402
    pivot_status_by_species,
    plot_box_age_by_status,
    plot_clustered_bar,
    plot_hist_age_by_status,
    plot_scatter_age_stay_by_species,
    report_animals_by_age_range,
    report_animals_by_status_species,
    report_medical_records,
    report_volunteer_workload,
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
    status_in_shelter = tables["animal_statuses"].loc[
        tables["animal_statuses"]["status_id"] == 1,
        "status_name",
    ].iat[0]
    status_under_treatment = tables["animal_statuses"].loc[
        tables["animal_statuses"]["status_id"] == 2,
        "status_name",
    ].iat[0]
    species_cat = tables["species_breed"].loc[
        tables["species_breed"]["species_breed_id"] == 3,
        "species_name",
    ].iat[0]
    diagnosis_dermatitis = tables["medical_records"].loc[
        tables["medical_records"]["record_id"] == 1,
        "diagnosis",
    ].iat[0]

    reports = {
        "animals_status_species": report_animals_by_status_species(
            tables,
            status_name=status_in_shelter,
            species_name=species_cat,
        ),
        "animals_age_range": report_animals_by_age_range(
            tables,
            min_age=2,
            max_age=5,
            status_names=[status_in_shelter, status_under_treatment],
        ),
        "volunteer_workload": report_volunteer_workload(
            tables,
            min_duration=30,
        ),
        "medical_records": report_medical_records(
            tables,
            diagnosis_part=diagnosis_dermatitis,
        ),
        "statistics": statistics_report(tables),
        "pivot_status_by_species": pivot_status_by_species(tables),
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
    return [
        plot_clustered_bar(tables, graphics_dir),
        plot_hist_age_by_status(tables, graphics_dir),
        plot_box_age_by_status(tables, graphics_dir),
        plot_scatter_age_stay_by_species(tables, graphics_dir),
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
