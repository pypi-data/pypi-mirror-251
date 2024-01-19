from typing import Literal
import pandas as pd
from .misc import remove_bin_chars
from .casting import can_be_int


def parse_df(df: pd.DataFrame) -> pd.DataFrame:
    """Automatically try to parse dataframe columns into the right format."""

    for col in df.columns:
        try:
            df[col] = df[col].astype(pd.BooleanDtype())
            continue
        except:
            pass
        try:
            df[col] = df[col].astype(pd.Int64Dtype())
            continue
        except:
            pass
        try:
            df[col] = df[col].astype(pd.Float64Dtype())
            continue
        except:
            pass
        try:
            df[col] = df[col].astype(pd.StringDtype())
            continue
        except:
            pass

    return df


def write_df(df: pd.DataFrame, path: str) -> None:
    """Save a DataFrame to CSV format."""
    df.to_csv(path, index=False, sep=";", quoting=2)


def read_df(path: str, skip_info=True, sep=";", quoting=2):
    """Read a DataFrame from CSV format."""
    df = pd.read_csv(path, sep=sep, quoting=quoting, low_memory=False)
    df.columns = [int(colname) if can_be_int(colname) else colname for colname in df.columns]

    df = parse_df(df)
    if not skip_info:
        df.head()
    return df


def to_turtle(
    df: pd.DataFrame,
    subject_col: str = "subject",
    subject_type: Literal["value", "uri"] = "uri",
    subject_prefix: str = "",
    predicate_col: str = "predicate",
    predicate_prefix: str = "",
    object_col: str = "object",
    object_type: Literal["value", "uri"] = "uri",
    object_prefix: str = "",
    path: str = "",
) -> str:
    """Transform a dataframe into a turtle string."""

    output = ""
    for _, row in df.iterrows():
        # If we have a nan value
        if pd.isna(row[subject_col]) or pd.isna(row[predicate_col]) or pd.isna(row[object_col]):
            continue

        # Subject
        subject = ""
        if subject_type == "value":
            subject = '"' + str(row[subject_col]) + '"'
        elif subject_type == "uri":
            subject = "<" + str(subject_prefix) + str(row[subject_col]) + ">"

        # Predicate
        predicate = "<" + str(predicate_prefix) + str(row[predicate_col]) + ">"

        # Object
        object = ""
        if object_type == "value":
            object = '"' + str(row[object_col]) + '"'
        elif object_type == "uri":
            object = "<" + str(object_prefix) + str(row[object_col]) + ">"

        output += subject + " " + predicate + " " + object + " .\n"

    if path != "":
        f = open(path, "w")
        f.write(output)
        f.close()

    return output


def remove_binary_chars(df: pd.DataFrame | pd.Series) -> None:
    """Remove binary characters in each column. Inplace."""

    for col in df.columns:
        if df[col].dtype == "object":
            df[col] = [remove_bin_chars(str(content)) for content in df[col]]
