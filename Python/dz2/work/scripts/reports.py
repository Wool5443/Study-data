"""Specialized report functions for the shelter database."""

import os
from pathlib import Path

# TODO: убрать
os.environ.setdefault("MPLCONFIGDIR", "/tmp/matplotlib")
import matplotlib.pyplot as plt
import pandas as pd


def _to_datetime(series: pd.Series) -> pd.Series:
    """Convert a pandas series to datetime values."""
    return pd.to_datetime(series, errors="coerce")


def denormalize_animals(tables: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """
    Join animal reference tables into a denormalized table.

    Parameters
    ----------
    tables : dict[str, pandas.DataFrame]
        Database tables loaded from pickle files.

    Returns
    -------
    pandas.DataFrame
        Animal table with species, breed and status names.
    """
    animals = tables["animals"].copy()
    species = tables["species_breed"].copy()
    statuses = tables["animal_statuses"].copy()

    result = animals.merge(species, on="species_breed_id", how="left")
    result = result.merge(statuses, on="status_id", how="left")
    result["birth_date"] = _to_datetime(result["birth_date"])
    result["admission_date"] = _to_datetime(result["admission_date"])
    return result


def denormalize_volunteer_tasks(
    tables: dict[str, pd.DataFrame],
) -> pd.DataFrame:
    """
    Join volunteer task tables into one report relation.

    Parameters
    ----------
    tables : dict[str, pandas.DataFrame]
        Database tables loaded from pickle files.

    Returns
    -------
    pandas.DataFrame
        Task table with animal and volunteer names.
    """
    tasks = tables["animal_volunteer_tasks"].copy()
    animals = tables["animals"][["animal_id", "name"]].copy()
    volunteers = tables["volunteers"].copy()
    volunteers["volunteer_name"] = (
        volunteers["last_name"].astype(str) + " " + volunteers["first_name"].astype(str)
    )
    result = tasks.merge(animals, on="animal_id", how="left")
    result = result.merge(
        volunteers[["volunteer_id", "volunteer_name", "phone", "is_active"]],
        on="volunteer_id",
        how="left",
    )
    result["task_date"] = _to_datetime(result["task_date"])
    return result


def add_animal_age_days_in_shelter(animals: pd.DataFrame) -> pd.DataFrame:
    """
    Add quantitative attributes used in reports.

    Parameters
    ----------
    animals : pandas.DataFrame
        Denormalized animal table.
    report_date : str | None, optional
        Date for age and shelter stay calculations.
        If None, the current date is used.

    Returns
    -------
    pandas.DataFrame
        Table with age and shelter stay columns.
    """
    result = animals.copy()
    date = pd.Timestamp.today().normalize()
    result["age_years"] = ((date - result["birth_date"]).dt.days / 365.25).round(1)
    result["days_in_shelter"] = (date - result["admission_date"]).dt.days
    return result


def report_animals_attention_list(tables: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """
    Create a text report with animals that require administrator attention.

    Parameters
    ----------
    tables : dict[str, pandas.DataFrame]
        Database tables loaded from pickle files.

    Returns
    -------
    pandas.DataFrame
        Report with animals that need medical or administrative attention.
    """
    animals = add_animal_age_days_in_shelter(denormalize_animals(tables))
    active_status_ids = [1, 2, 4, 5]
    attention_status_ids = [2, 4]
    row_index = animals["status_id"].isin(active_status_ids) & (
        animals["status_id"].isin(attention_status_ids)
        | (animals["vaccinated"] == 0)
        | (animals["sterilized"] == 0)
    )
    columns = [
        "inventory_number",
        "name",
        "species_name",
        "breed_name",
        "sex",
        "age_years",
        "status_name",
        "vaccinated",
        "sterilized",
        "days_in_shelter",
        "notes",
    ]
    return animals.loc[row_index, columns].reset_index(drop=True)


def report_volunteer_workload_summary(tables: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """
    Create an aggregated workload report for volunteers.

    Parameters
    ----------
    tables : dict[str, pandas.DataFrame]
        Database tables loaded from pickle files.

    Returns
    -------
    pandas.DataFrame
        Report with task count and duration statistics by volunteer.
    """
    tasks = denormalize_volunteer_tasks(tables)
    report = (
        tasks.groupby(["volunteer_id", "volunteer_name", "phone", "is_active"])
        .agg(
            task_count=("task_id", "count"),
            total_minutes=("duration_minutes", "sum"),
            average_minutes=("duration_minutes", "mean"),
        )
        .reset_index()
    )
    report["average_minutes"] = report["average_minutes"].round(1)
    return report[
        [
            "volunteer_name",
            "phone",
            "is_active",
            "task_count",
            "total_minutes",
            "average_minutes",
        ]
    ]


def statistics_report(tables: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """
    Create a statistical text report.

    Parameters
    ----------
    tables : dict[str, pandas.DataFrame]
        Database tables loaded from pickle files.

    Returns
    -------
    pandas.DataFrame
        Statistical report for qualitative and quantitative attributes.
    """
    animals = add_animal_age_days_in_shelter(denormalize_animals(tables))
    tasks = denormalize_volunteer_tasks(tables)
    rows = []
    for column in ["species_name", "status_name", "sex", "vaccinated", "sterilized"]:
        counts = animals[column].value_counts(dropna=False)
        percent = (counts / len(animals) * 100).round(2)
        for level, frequency, percent_value in zip(
            counts.index.astype(str),
            counts.values,
            percent.values,
        ):
            rows.append(
                {
                    "attribute": column,
                    "level": level,
                    "frequency": frequency,
                    "percent": percent_value,
                    "min": "",
                    "max": "",
                    "mean": "",
                    "std": "",
                }
            )

    quantitative = {
        "age_years": animals["age_years"],
        "days_in_shelter": animals["days_in_shelter"],
        "duration_minutes": tasks["duration_minutes"],
    }
    for column, series in quantitative.items():
        rows.append(
            {
                "attribute": column,
                "level": "",
                "frequency": len(series),
                "percent": 100.0,
                "min": series.min(),
                "max": series.max(),
                "mean": round(series.mean(), 2),
                "std": round(series.std(), 2),
            }
        )
    return pd.DataFrame(rows)


def pivot_species_status(
    tables: dict[str, pd.DataFrame],
    aggfunc: str = "count",
) -> pd.DataFrame:
    """
    Create a pivot table of animal statuses by species.

    Parameters
    ----------
    tables : dict[str, pandas.DataFrame]
        Database tables loaded from pickle files.
    aggfunc : str, optional
        Aggregation function name for pandas.pivot_table.

    Returns
    -------
    pandas.DataFrame
        Pivot table.
    """
    animals = denormalize_animals(tables)
    pivot = pd.pivot_table(
        animals,
        values="animal_id",
        index="species_name",
        columns="status_name",
        aggfunc=aggfunc,
        fill_value=0,
    )
    return pivot.reset_index()


def plot_species_status_bar(
    tables: dict[str, pd.DataFrame],
    graphics_dir: str | Path,
) -> Path:
    """
    Build a clustered bar chart by species and status.

    Parameters
    ----------
    tables : dict[str, pandas.DataFrame]
        Database tables loaded from pickle files.
    graphics_dir : str | Path
        Directory for graphic reports.

    Returns
    -------
    pathlib.Path
        Path to the created image.
    """
    graphics_path = Path(graphics_dir)
    graphics_path.mkdir(parents=True, exist_ok=True)
    animals = denormalize_animals(tables)
    counts = pd.crosstab(animals["species_name"], animals["status_name"])

    plt.figure(figsize=(8, 5))
    x_positions = range(len(counts.index))
    width = 0.8 / max(len(counts.columns), 1)
    for index, status in enumerate(counts.columns):
        shifted = [x + index * width for x in x_positions]
        plt.bar(shifted, counts[status], width=width, label=status)
    centers = [x + width * (len(counts.columns) - 1) / 2 for x in x_positions]
    plt.xticks(centers, counts.index)
    plt.title("Animal statuses by species")
    plt.xlabel("Species")
    plt.ylabel("Number of animals")
    plt.legend(title="Status")
    plt.tight_layout()
    path = graphics_path / "species_status_bar.png"
    plt.savefig(path, dpi=150)
    plt.close()
    return path


def plot_age_stay_scatter(
    tables: dict[str, pd.DataFrame],
    graphics_dir: str | Path,
) -> Path:
    """
    Build a categorized scatter plot by age and shelter stay.

    Parameters
    ----------
    tables : dict[str, pandas.DataFrame]
        Database tables loaded from pickle files.
    graphics_dir : str | Path
        Directory for graphic reports.

    Returns
    -------
    pathlib.Path
        Path to the created image.
    """
    graphics_path = Path(graphics_dir)
    graphics_path.mkdir(parents=True, exist_ok=True)
    animals = add_animal_age_days_in_shelter(denormalize_animals(tables))

    plt.figure(figsize=(8, 5))
    for species, group in animals.groupby("species_name"):
        plt.scatter(
            group["age_years"],
            group["days_in_shelter"],
            label=species,
            s=80,
        )
    plt.title("Age and shelter stay by species")
    plt.xlabel("Age, years")
    plt.ylabel("Days in shelter")
    plt.legend(title="Species")
    plt.tight_layout()
    path = graphics_path / "age_stay_scatter.png"
    plt.savefig(path, dpi=150)
    plt.close()
    return path


def plot_volunteer_task_type_bar(
    tables: dict[str, pd.DataFrame],
    graphics_dir: str | Path,
) -> Path:
    """
    Build a bar chart with total volunteer task duration by task type.

    Parameters
    ----------
    tables : dict[str, pandas.DataFrame]
        Database tables loaded from pickle files.
    graphics_dir : str | Path
        Directory for graphic reports.

    Returns
    -------
    pathlib.Path
        Path to the created image.
    """
    graphics_path = Path(graphics_dir)
    graphics_path.mkdir(parents=True, exist_ok=True)
    tasks = tables["animal_volunteer_tasks"].copy()
    totals = (
        tasks.groupby("task_type")["duration_minutes"]
        .sum()
        .sort_values(ascending=False)
    )

    plt.figure(figsize=(8, 5))
    plt.bar(totals.index, totals.values)
    plt.title("Volunteer workload by task type")
    plt.xlabel("Task type")
    plt.ylabel("Total minutes")
    plt.xticks(rotation=25, ha="right")
    plt.tight_layout()
    path = graphics_path / "volunteer_task_type_bar.png"
    plt.savefig(path, dpi=150)
    plt.close()
    return path


def plot_medical_diagnosis_bar(
    tables: dict[str, pd.DataFrame],
    graphics_dir: str | Path,
) -> Path:
    """
    Build a bar chart with medical record counts by diagnosis.

    Parameters
    ----------
    tables : dict[str, pandas.DataFrame]
        Database tables loaded from pickle files.
    graphics_dir : str | Path
        Directory for graphic reports.

    Returns
    -------
    pathlib.Path
        Path to the created image.
    """
    graphics_path = Path(graphics_dir)
    graphics_path.mkdir(parents=True, exist_ok=True)
    records = tables["medical_records"].copy()
    counts = records["diagnosis"].value_counts()

    plt.figure(figsize=(8, 5))
    plt.bar(counts.index, counts.values)
    plt.title("Medical records by diagnosis")
    plt.xlabel("Diagnosis")
    plt.ylabel("Number of records")
    plt.xticks(rotation=25, ha="right")
    plt.tight_layout()
    path = graphics_path / "medical_diagnosis_bar.png"
    plt.savefig(path, dpi=150)
    plt.close()
    return path
