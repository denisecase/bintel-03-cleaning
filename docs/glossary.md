# Glossary

Use this page to record terms and ideas that help you understand
professional analytics projects.

This project covers data cleaning and preparation:
fixing quality issues in raw data and saving clean files ready for ETVL.

Pro-tip: Expand the VS Code **Outline** view (below the navigator on the right)
to see this file organization at-a-glance.

## Data Cleaning

### data cleaning

Data cleaning is the process of identifying and fixing errors,
inconsistencies, and missing values in a dataset.
Clean data is essential for reliable analysis and accurate reporting.

### prepared data

Prepared data is data that has been cleaned, standardized, and validated.
It is saved separately from raw data so the original is preserved.
Prepared data is the input to the ETVL loading stage.

### standardization

Standardization converts values in a column to a consistent format.
For example, converting "East", "east", and "EAST" all to "East".
Inconsistent values cause errors in grouping, joining, and reporting.

### deduplication

Deduplication is the process of identifying and removing duplicate rows.
A duplicate is a row that is identical to another row in the same table.
Removing duplicates prevents inflated counts and distorted totals.

### imputation

Imputation is the process of filling in missing values with estimated ones.
Common strategies include filling with the mean, median, or a placeholder.
The choice of imputation strategy is an analyst decision.

### coercion

Coercion forces a value into a specific data type.
`pd.to_numeric(errors='coerce')` converts non-numeric values to NaN
instead of raising an error.
Coercion is useful for handling messy real-world data.

### foreign key

A foreign key is a column in one table that references the primary key
of another table.
A sale row with a CustomerID that does not exist in the customers table
is a foreign key violation and should be removed or flagged.

### primary key

A primary key is a column (or set of columns) that uniquely identifies
each row in a table.
CustomerID, ProductID, and TransactionID are primary keys in the smart sales data.

### referential integrity

Referential integrity means that every foreign key value in one table
has a matching primary key in the referenced table.
Checking referential integrity catches orphaned records before loading.

## Verification

### data validation

Data validation checks that data meets expected rules before it is used.
Examples include checking that prices are positive,
dates are valid, and required fields are not empty.

### before and after comparison

A before and after comparison shows the state of data before and after cleaning.
Comparing row counts, unique values, and distributions confirms
that cleaning worked as intended.

### assertion

An assertion is a check in code that verifies a condition is true.
If the condition is false, the program raises an error.
Assertions are a simple way to verify data quality at each pipeline stage.

## ETVL Process

### ETVL

ETVL stands for Extract, Transform, Verify, Load.
It is a structured process for moving data from a source
into a central data store.
Verification is the step that distinguishes ETVL from traditional ETL.

### extract

The extract step reads data from a source such as a CSV file,
a database, or an API.
In this project, extraction means reading the raw CSV files into DataFrames.

### transform

The transform step converts raw data into the format needed
for the target system.
Transformations include cleaning, standardizing, filtering, and reshaping.

### verify

The verify step confirms that transformed data meets quality expectations
before loading.
Verification prevents bad data from entering the warehouse.

### load

The load step writes transformed and verified data into the target system.
In this project, loading means writing prepared CSV files
to the `data/prepared/` folder.
