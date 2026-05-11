"""Specialized report functions for the shelter database."""

import os
from pathlib import Path

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
        volunteers[["volunteer_id", "volunteer_name", "phone"]],
        on="volunteer_id",
        how="left",
    )
    result["task_date"] = _to_datetime(result["task_date"])
    return result


def add_animal_metrics(
    animals: pd.DataFrame,
    report_date: str = "2026-05-11",
) -> pd.DataFrame:
    """
    Add quantitative attributes used in reports.

    Parameters
    ----------
    animals : pandas.DataFrame
        Denormalized animal table.
    report_date : str, optional
        Date for age and shelter stay calculations.

    Returns
    -------
    pandas.DataFrame
        Table with age and shelter stay columns.
    """
    result = animals.copy()
    date = pd.Timestamp(report_date)
    result["age_years"] = ((date - result["birth_date"]).dt.days / 365.25).round(1)
    result["days_in_shelter"] = (date - result["admission_date"]).dt.days
    return result


def report_animals_by_status_species(
    tables: dict[str, pd.DataFrame],
    status_name: str,
    species_name: str,
) -> pd.DataFrame:
    """
    Create a text report by animal status and species.

    Parameters
    ----------
    tables : dict[str, pandas.DataFrame]
        Database tables loaded from pickle files.
    status_name : str
        Required animal status.
    species_name : str
        Required animal species.

    Returns
    -------
    pandas.DataFrame
        Filtered animal report.
    """
    animals = add_animal_metrics(denormalize_animals(tables))
    row_index = (animals["status_name"] == status_name) * (
        animals["species_name"] == species_name
    )
    columns = [
        "inventory_number",
        "name",
        "species_name",
        "breed_name",
        "sex",
        "age_years",
        "status_name",
    ]
    return animals.loc[row_index, columns].reset_index(drop=True)


def report_animals_by_age_range(
    tables: dict[str, pd.DataFrame],
    min_age: float,
    max_age: float,
    status_names: list[str] | None = None,
) -> pd.DataFrame:
    """
    Create a text report for animals in the specified age range.

    Parameters
    ----------
    tables : dict[str, pandas.DataFrame]
        Database tables loaded from pickle files.
    min_age : float
        Minimum age in years.
    max_age : float
        Maximum age in years.
    status_names : list[str] | None, optional
        Allowed statuses. If the value is None, all statuses are used.

    Returns
    -------
    pandas.DataFrame
        Animal report with a quantitative selection criterion.
    """
    animals = add_animal_metrics(denormalize_animals(tables))
    row_index = (animals["age_years"] >= min_age) * (animals["age_years"] <= max_age)
    if status_names is not None:
        row_index = row_index * animals["status_name"].isin(status_names)
    columns = [
        "name",
        "species_name",
        "breed_name",
        "age_years",
        "days_in_shelter",
        "status_name",
    ]
    return animals.loc[row_index, columns].reset_index(drop=True)


def report_volunteer_workload(
    tables: dict[str, pd.DataFrame],
    min_duration: int,
) -> pd.DataFrame:
    """
    Create a text report for volunteer tasks.

    Parameters
    ----------
    tables : dict[str, pandas.DataFrame]
        Database tables loaded from pickle files.
    min_duration : int
        Minimum task duration in minutes.

    Returns
    -------
    pandas.DataFrame
        Volunteer workload report.
    """
    tasks = denormalize_volunteer_tasks(tables)
    row_index = tasks["duration_minutes"] >= min_duration
    columns = [
        "task_date",
        "volunteer_name",
        "phone",
        "name",
        "task_type",
        "duration_minutes",
        "comment",
    ]
    return tasks.loc[row_index, columns].reset_index(drop=True)


def report_medical_records(
    tables: dict[str, pd.DataFrame],
    diagnosis_part: str,
) -> pd.DataFrame:
    """
    Create a text report for medical records.

    Parameters
    ----------
    tables : dict[str, pandas.DataFrame]
        Database tables loaded from pickle files.
    diagnosis_part : str
        Text fragment to search for in the diagnosis.

    Returns
    -------
    pandas.DataFrame
        Medical report with animal attributes.
    """
    records = tables["medical_records"].copy()
    animals = denormalize_animals(tables)
    result = records.merge(
        animals[["animal_id", "name", "species_name", "status_name"]],
        on="animal_id",
        how="left",
    )
    row_index = result["diagnosis"].str.contains(
        diagnosis_part,
        case=False,
        na=False,
    )
    columns = [
        "record_date",
        "name",
        "species_name",
        "status_name",
        "diagnosis",
        "treatment",
        "vet_name",
        "comment",
    ]
    return result.loc[row_index, columns].reset_index(drop=True)


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
    animals = add_animal_metrics(denormalize_animals(tables))
    rows = []
    for column in ["species_name", "status_name", "sex"]:
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
                    "variance": "",
                    "std": "",
                }
            )

    for column in ["age_years", "days_in_shelter"]:
        series = animals[column]
        rows.append(
            {
                "attribute": column,
                "level": "",
                "frequency": len(series),
                "percent": 100.0,
                "min": series.min(),
                "max": series.max(),
                "mean": round(series.mean(), 2),
                "variance": round(series.var(), 2),
                "std": round(series.std(), 2),
            }
        )
    return pd.DataFrame(rows)


def pivot_status_by_species(
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


def plot_clustered_bar(
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
    path = graphics_path / "clustered_bar_species_status.png"
    plt.savefig(path, dpi=150)
    plt.close()
    return path


def plot_hist_age_by_status(
    tables: dict[str, pd.DataFrame],
    graphics_dir: str | Path,
) -> Path:
    """
    Build a categorized histogram of age by status.

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
    animals = add_animal_metrics(denormalize_animals(tables))

    plt.figure(figsize=(8, 5))
    for status, group in animals.groupby("status_name"):
        plt.hist(group["age_years"], alpha=0.65, label=status)
    plt.title("Animal age by status")
    plt.xlabel("Age, years")
    plt.ylabel("Number of animals")
    plt.legend(title="Status")
    plt.tight_layout()
    path = graphics_path / "hist_age_by_status.png"
    plt.savefig(path, dpi=150)
    plt.close()
    return path


def plot_box_age_by_status(
    tables: dict[str, pd.DataFrame],
    graphics_dir: str | Path,
) -> Path:
    """
    Build a categorized box-and-whisker plot by age.

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
    animals = add_animal_metrics(denormalize_animals(tables))
    groups = [
        group["age_years"].dropna() for _, group in animals.groupby("status_name")
    ]
    labels = [status for status, _ in animals.groupby("status_name")]

    plt.figure(figsize=(8, 5))
    plt.boxplot(groups, labels=labels)
    plt.title("Animal age by status")
    plt.xlabel("Status")
    plt.ylabel("Age, years")
    plt.tight_layout()
    path = graphics_path / "box_age_by_status.png"
    plt.savefig(path, dpi=150)
    plt.close()
    return path


def plot_scatter_age_stay_by_species(
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
    animals = add_animal_metrics(denormalize_animals(tables))

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
    path = graphics_path / "scatter_age_stay_by_species.png"
    plt.savefig(path, dpi=150)
    plt.close()
    return path
