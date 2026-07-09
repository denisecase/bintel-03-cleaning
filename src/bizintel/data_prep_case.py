"""data_prep_case.py - example.

An example of cleaning and preparing raw smart sales data.
Cleaning and preparation is a critical step in any BI workflow.
It is different for every project and every dataset.

This example is designed to be copied and modified.
On new datasets, you will need to change the cleaning and preparation logic.
This example is only an illustration.

Cleaning can be 80-90% of the work in a BI project.
It is often the most time-consuming step and
to do it well requires domain knowledge, attention to detail,
tenacity, and resourcefulness.

It is often the most important step because
if the data is not clean, the analysis will be wrong and
the business decisions will be wrong.

Common cleaning and preparation tasks include:
- Remove duplicate rows.
- Remove rows with missing or invalid values.
- Normalize inconsistent values (e.g., "East", "east", " EAST ").
- Convert data types (e.g., text to numeric, text to datetime).

Author: Denise Case
Date: 2026-06

Process:
    - Load raw CSV data files.
    - Clean and prepare each dataset.
    - Verify data quality after cleaning.
    - Save prepared data to data/prepared/.

Data Source:
- data/raw/customers_data.csv
- data/raw/products_data.csv
- data/raw/sales_data.csv

Output:
- data/prepared/customers_data_prepared.csv
- data/prepared/products_data_prepared.csv
- data/prepared/sales_data_prepared.csv

Terminal command to run this file from the root project folder:

uv run python -m bizintel.data_prep_case

OBS:
  Don't edit this file - it should remain a working example.
  Copy it, rename it with your alias, and modify your copy.
  If you do, include your command to run it in the docstring above and in README.md.
"""

# === DECLARE IMPORTS (bring in free code from elsewhere) ===

from pathlib import Path
from typing import Final

from datafun_toolkit.logger import log_path
import pandas as pd

from bizintel.utils_data import (
    check_quality,
    inspect_basic,
    load_data,
    summarize_numeric,
)
from bizintel.utils_logger import LOG, log_header

# === DECLARE GLOBAL CONSTANTS AND CONFIGURATION ===

# Raw data folder path (relative to the root project folder).
DATA_RAW: Final[Path] = Path("data/raw")

# Prepared data folder path (relative to the root project folder).
DATA_PREPARED: Final[Path] = Path("data/prepared")

# Input files.
CUSTOMERS_FILE: Final[Path] = DATA_RAW / "customers_data.csv"
PRODUCTS_FILE: Final[Path] = DATA_RAW / "products_data.csv"
SALES_FILE: Final[Path] = DATA_RAW / "sales_data.csv"

# Output files.
CUSTOMERS_PREPARED: Final[Path] = DATA_PREPARED / "customers_data_prepared.csv"
PRODUCTS_PREPARED: Final[Path] = DATA_PREPARED / "products_data_prepared.csv"
SALES_PREPARED: Final[Path] = DATA_PREPARED / "sales_data_prepared.csv"


# === Section 2. Define Reusable Functions ===

# === Section 2.1 DEFINE A PREPARE CUSTOMERS FUNCTION ===

# Define a reusable function that takes the customers DataFrame,
# cleans it, and returns a prepared DataFrame ready for the warehouse.


def prepare_customers(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and prepare the customers DataFrame.

    WHY: Inconsistent region values and duplicate rows
    will cause problems in the warehouse and in reporting.
    We fix them here before loading.

    Args:
        df: Raw customers DataFrame.

    Returns:
        Cleaned customers DataFrame.
    """
    LOG.info("Preparing customers data")

    # Make a copy to avoid modifying the original DataFrame.
    # This ensures the original raw DataFrame is not changed.
    df = df.copy()

    LOG.info("Customers Prep 1. Normalize Region values")

    # Select the Region column from the DataFrame.
    # A column is a Series - a single column of values.
    region_column = df["Region"]

    # Use the built-in .str property to access string methods on every value.
    # .str.strip() removes leading and trailing whitespace from each value.
    stripped = region_column.str.strip()

    # .str.title() capitalizes the first letter of each word in each value.
    # So "east", "EAST", and " East " all become "East".
    titled = stripped.str.title()

    # Put the cleaned values back into the Region column of the DataFrame.
    df["Region"] = titled

    # Call the dropna() method to remove any rows where the Region value is missing (NaN).
    df["Region"] = df["Region"].dropna()

    # Call the unique() method and tolist() method chained together
    # to get unique region values after normalization and assign them to a list named regions.
    # You can modify your copy to chain more functions together.
    # This example is designed for teaching and clarity not production.
    regions: list[str] = df["Region"].unique().tolist()

    # Call the built-in Python sorted() function to sort the list of unique region values.
    regions_sorted: list[str] = sorted(regions)

    # Log the sorted unique region values
    # to verify cleaning and preparation.
    LOG.info(f"  Regions after normalization: {regions_sorted}")

    # NOTE: 'South-West' does not match any standard region.
    # In your copy of the data prep logic, you can
    # split into South and West,
    # or map to nearest region,
    # or keep as its own region.
    # The analyst makes a LOT of decisions during cleaning.
    # Think about what is "best" for your data and intent.
    # Always document your decisions and rationale.

    LOG.info("Customers Prep 2. Remove duplicate rows")

    # Remove duplicate rows - keep the first occurrence.
    # before and after let us see how many rows were removed.
    # Remember that df.shape[0] gives the number of rows in the DataFrame.
    before: int = df.shape[0]
    df = df.drop_duplicates()
    after: int = df.shape[0]

    LOG.info(f"  Rows before: {before}")
    LOG.info(f"  Rows after: {after}")
    LOG.info(f"  Removed {before - after} duplicate row(s)")
    LOG.info(f"  Customers prepared: {df.shape[0]} rows")
    return df


# === Section 2.2 DEFINE A PREPARE PRODUCTS FUNCTION ===

# Define a reusable function that takes the products DataFrame,
# cleans it, and returns a prepared DataFrame ready for the warehouse.


def prepare_products(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and prepare the products DataFrame.

    WHY: Even clean-looking data should be verified.
    We confirm types and check for unexpected values.

    Args:
        df: Raw products DataFrame.

    Returns:
        Cleaned products DataFrame.
    """
    LOG.info("Preparing products data")

    # Make a copy to avoid modifying the original DataFrame.
    # This ensures the original raw DataFrame is not changed.
    df = df.copy()

    LOG.info("Products Prep 1. Convert UnitPrice to numeric")

    # Select the UnitPrice column from the DataFrame.
    # A column is a Series - a single column of values.
    price_column = df["UnitPrice"]

    # Call pd.to_numeric() to convert the column to numeric values.
    # errors="coerce" means any value that cannot be converted
    # (like text or symbols) will be replaced with NaN (not a number).
    price_numeric = pd.to_numeric(price_column, errors="coerce")

    # Put the converted values back into the UnitPrice column.
    df["UnitPrice"] = price_numeric

    # Log how many prices could not be converted.
    bad_prices: int = int(df["UnitPrice"].isna().sum())
    LOG.info(f"  Non-numeric prices replaced with NaN: {bad_prices}")

    LOG.info("Products Prep 2. Remove duplicate rows")

    # Remove duplicate rows - keep the first occurrence.
    # before and after let us see how many rows were removed.
    before: int = df.shape[0]
    df = df.drop_duplicates()
    after: int = df.shape[0]

    LOG.info(f"  Rows before: {before}")
    LOG.info(f"  Rows after: {after}")
    LOG.info(f"  Removed {before - after} duplicate row(s)")
    LOG.info(f"  Products prepared: {df.shape[0]} rows")
    return df


# === Section 2.3 DEFINE A PREPARE SALES FUNCTION ===

# Define a reusable function that takes the sales DataFrame,
# cleans it, and returns a prepared DataFrame ready for the warehouse.


def prepare_sales(
    df: pd.DataFrame,
    valid_customer_ids: set[int],
    valid_product_ids: set[int],
) -> pd.DataFrame:
    """Clean and prepare the sales DataFrame.

    WHY: Sales data links customers and products.
    Invalid foreign keys mean orphaned records in the warehouse
    that cannot be joined to any customer or product.

    Args:
        df: Raw sales DataFrame.
        valid_customer_ids: Set of valid CustomerIDs from customers table.
        valid_product_ids: Set of valid ProductIDs from products table.

    Returns:
        Cleaned sales DataFrame.
    """
    LOG.info("Preparing sales data")

    # Make a copy to avoid modifying the original DataFrame.
    # This ensures the original raw DataFrame is not changed.
    df = df.copy()

    LOG.info("Sales Prep 1. Convert SaleDate to datetime")

    # Select the SaleDate column from the DataFrame.
    date_column = df["SaleDate"]

    # Call pd.to_datetime() to convert the column to datetime values.
    # errors="coerce" means any value that cannot be converted
    # (like an invalid date such as 2023-13-01) becomes NaT (not a time).
    date_converted = pd.to_datetime(date_column, errors="coerce")

    # Put the converted values back into the SaleDate column.
    df["SaleDate"] = date_converted

    # Log how many dates could not be parsed.
    bad_dates: int = int(df["SaleDate"].isna().sum())
    if bad_dates > 0:
        LOG.warning(f"  {bad_dates} row(s) with invalid SaleDate - will be removed")

    LOG.info("Sales Prep 2. Convert SaleAmount to numeric")

    # Select the SaleAmount column from the DataFrame.
    amount_column = df["SaleAmount"]

    # Call pd.to_numeric() to convert the column to numeric values.
    # errors="coerce" means any value that cannot be converted
    # (like the "?" in the raw data) becomes NaN (not a number).
    amount_numeric = pd.to_numeric(amount_column, errors="coerce")

    # Put the converted values back into the SaleAmount column.
    df["SaleAmount"] = amount_numeric

    # Log how many amounts could not be parsed.
    bad_amounts: int = int(df["SaleAmount"].isna().sum())
    if bad_amounts > 0:
        LOG.warning(f"  {bad_amounts} row(s) with invalid SaleAmount - will be removed")

    LOG.info("Sales Prep 3. Remove rows with missing date or amount")

    # Remove rows where SaleDate or SaleAmount could not be parsed.
    # dropna() removes rows where any of the listed columns has NaN or NaT.
    before: int = df.shape[0]
    df = df.dropna(subset=["SaleDate", "SaleAmount"])
    after: int = df.shape[0]

    LOG.info(f"  Rows before: {before}")
    LOG.info(f"  Rows after: {after}")
    LOG.info(f"  Removed {before - after} row(s) with missing date or amount")

    LOG.info("Sales Prep 4. Check CustomerID foreign key integrity")

    # A foreign key is a column in one table that must match
    # a primary key in another table.
    # Here we check that every CustomerID in sales
    # exists in the customers table.
    # The tilde (~) means "not" - so invalid_customers is True
    # for every row where the CustomerID is NOT in valid_customer_ids.
    invalid_customers = ~df["CustomerID"].isin(valid_customer_ids)

    # Count how many rows have an invalid CustomerID.
    invalid_customer_count: int = int(invalid_customers.sum())

    if invalid_customer_count > 0:
        LOG.warning(
            f"  {invalid_customer_count} row(s) with CustomerID "
            "not found in customers table - will be removed"
        )

        # Keep only rows where the CustomerID is valid.
        # df[~invalid_customers] filters the DataFrame to keep only rows
        # where invalid_customers is False (meaning the CustomerID IS valid).
        df = df[~invalid_customers]

    LOG.info("Sales Prep 5. Check ProductID foreign key integrity")

    # Check that every ProductID in sales exists in the products table.

    # Generate a list of invalid ProductIDs by checking
    # which ProductIDs in the sales DataFrame
    # are not present in the set of valid ProductIDs
    # from the products DataFrame.

    # df["ProductID"] selects the ProductID column from the DataFrame.
    # .isin(valid_product_ids) returns True for each row where the ProductID
    # is found in our set of valid product IDs, and False if it is not found.

    # The tilde ~ is the "not" operator in Python for boolean Series.
    # It flips every True to False and every False to True.
    # So invalid_products is True for rows where the ProductID is NOT valid.
    invalid_products = ~df["ProductID"].isin(valid_product_ids)

    # Count how many rows have an invalid ProductID.
    invalid_product_count: int = int(invalid_products.sum())

    if invalid_product_count > 0:
        LOG.warning(
            f"  {invalid_product_count} row(s) with ProductID "
            "not found in products table - will be removed"
        )
        # Keep only rows where the ProductID is valid.
        # df[~invalid_products] filters the DataFrame to keep only rows
        # where invalid_products is False (meaning the ProductID IS valid).
        df = df[~invalid_products]

    LOG.info("Sales Prep 6. Remove duplicate rows")

    # Remove duplicate rows - keep the first occurrence.
    before_count: int = df.shape[0]
    df = df.drop_duplicates()
    after_count: int = df.shape[0]

    LOG.info(f"  Rows before: {before_count}")
    LOG.info(f"  Rows after: {after_count}")

    LOG.info(f"  Removed {before_count - after_count} duplicate row(s)")
    LOG.info(f"  Sales prepared: {df.shape[0]} rows")
    return df


# === Section 2.4 DEFINE A SAVE FUNCTION ===

# Define a reusable function that saves a prepared DataFrame
# to a CSV file in the data/prepared/ folder.


def save_prepared(df: pd.DataFrame, filepath: Path, name: str) -> None:
    """Save a prepared DataFrame to CSV.

    WHY: Saving prepared data to a separate folder keeps raw data
    untouched and gives downstream steps a clean input to work from.

    Args:
        df: Prepared DataFrame to save.
        filepath: Path to the output CSV file.
        name: A short name for logging.

    Returns:
        None
    """
    # Create the output folder if it does not exist
    # parents=True means create any missing parent folders as well.
    # exist_ok=True means
    # do not raise an error (it's ok) if the folder already exists.
    filepath.parent.mkdir(parents=True, exist_ok=True)

    # Call the df.to_csv() method to save the DataFrame to a CSV file.
    # Pass in the filepath where the file should be saved.
    # Set the index parameter to False to avoid saving the index column.
    # This is important because the index is not part of the original data
    # and should not be included in the saved file.
    df.to_csv(filepath, index=False)

    # Use df.shape[0] to get the number of rows in the DataFrame.
    row_count: int = df.shape[0]

    # Log useful information about the saved file,
    # including the number of rows and the file path.
    LOG.info(f"Saved {name}")
    LOG.info(f"  Rows: {row_count}")
    LOG.info(f"  Path: {filepath}")


# === MAIN FUNCTION ===


def main() -> None:
    """Main function to run the data preparation logic.

    This is where the main logic starts
    when this script is run.
    """
    # First, log the header for the BI module to indicate the start of the workflow.
    log_header(LOG, "BI")

    LOG.info("========================")
    LOG.info("START main()")
    LOG.info("========================")

    log_path(LOG, "Raw data:     ", DATA_RAW)
    log_path(LOG, "Prepared data:", DATA_PREPARED)

    LOG.info("Task 1. LOAD. Call a function to load each dataset......")
    df_customers = load_data(CUSTOMERS_FILE, "customers")
    df_products = load_data(PRODUCTS_FILE, "products")
    df_sales = load_data(SALES_FILE, "sales")

    LOG.info("Task 2. INSPECT. Call a function to inspect each dataset...")
    inspect_basic(df_customers, "customers")
    inspect_basic(df_products, "products")
    inspect_basic(df_sales, "sales")

    LOG.info("Task 3. CHECK QUALITY BEFORE........")
    check_quality(df_customers, "customers")
    check_quality(df_products, "products")
    check_quality(df_sales, "sales")

    LOG.info("Task 4. SUMMARIZE BEFORE.......... ")
    summarize_numeric(df_customers, "customers")
    summarize_numeric(df_products, "products")
    summarize_numeric(df_sales, "sales")

    LOG.info("Task 5. PREPARE DATASETS.........")
    df_customers_prepared = prepare_customers(df_customers)
    df_products_prepared = prepare_products(df_products)

    # Prepare sales requires valid customer and product IDs,
    # so we prepare customers and products first.
    # Build sets (like a list but no duplicates)
    # of valid IDs for foreign key checks in sales
    # Define a set of integers for CustomerID.
    # Define a set of integers for ProductID.
    # We will pass these sets to the prepare sales function
    # to check that each foreign key in sales is valid
    # (exists in the corresponding set).
    valid_customer_ids: set[int] = set(df_customers_prepared["CustomerID"])
    valid_product_ids: set[int] = set(df_products_prepared["ProductID"])

    df_sales_prepared = prepare_sales(
        df_sales,
        valid_customer_ids,
        valid_product_ids,
    )

    LOG.info("Task 6. CHECK QUALITY AFTER PREPARATION........")
    check_quality(df_customers_prepared, "customers prepared")
    check_quality(df_products_prepared, "products prepared")
    check_quality(df_sales_prepared, "sales prepared")

    LOG.info("Task 7. SUMMARIZE AFTER PREPARATION........")
    summarize_numeric(df_customers_prepared, "customers prepared")
    summarize_numeric(df_products_prepared, "products prepared")
    summarize_numeric(df_sales_prepared, "sales prepared")

    LOG.info("Task 8. SAVE PREPARED DATASETS........")
    save_prepared(df_customers_prepared, CUSTOMERS_PREPARED, "customers")
    save_prepared(df_products_prepared, PRODUCTS_PREPARED, "products")
    save_prepared(df_sales_prepared, SALES_PREPARED, "sales")

    LOG.info("Workflow complete")
    LOG.info("========================")
    LOG.info("Executed successfully!")
    LOG.info("========================")


# === CONDITIONAL EXECUTION GUARD ===

if __name__ == "__main__":
    # This conditional ensures that main() is only called
    # when this script is run directly, not when imported.
    main()
