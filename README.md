# Excel ➜ SQLite Conversion Utility

This repository now includes a Python utility that can ingest messy Excel
survey workbooks and convert them into a queryable SQLite database.  It is
geared toward batches of files where worksheets frequently contain merged
cells, blank spacer rows, or slightly different column names across
submissions.

## Features

* **Automatic unmerging** – merged cells are split and the top-left value is
  propagated into the newly created cells.
* **Header detection** – scans the first few rows to locate the most likely
  header row even if the sheet starts with descriptive text.
* **Column sanitisation** – column names are converted to safe SQLite
  identifiers while preserving the original names in a metadata table.
* **Table metadata** – every worksheet becomes its own table; companion
  metadata tables list the source workbook, worksheet name, and original
  column headers.

## Requirements

Install the Python dependencies (Python 3.9+ is recommended):

```bash
pip install -r requirements.txt
```

## Usage

```bash
python convert_excel_to_sqlite.py --db pmksy.sqlite "data/**/*.xlsx"
```

* ``--db`` (optional) sets the output SQLite database path.
* ``--max-header-scan`` (optional) controls how many leading rows the script
  inspects when guessing the header row (default: 10).

The script will emit one table per worksheet inside the database.  Sanitised
table and column names are used for compatibility.  The tables
``table_metadata`` and ``column_metadata`` store the mapping back to the
original workbook, worksheet title, and header labels.

## Exploring the Output

You can inspect the database using the SQLite CLI:

```bash
sqlite3 pmksy.sqlite ".tables"
```

To understand the column mapping for a specific worksheet table:

```sql
SELECT column_position, column_name, original_header
FROM column_metadata
WHERE table_name = 'test_data_1_2_general_information'
ORDER BY column_position;
```

## Extending the Workflow

* Adjust the ``build_headers`` function if your spreadsheets require
  different sanitisation rules.
* Add post-processing steps (for example, type casting or normalisation into
  a canonical schema) after the DataFrame is created and before it is written
  to SQLite.
* If you want a different database backend (e.g., PostgreSQL or MySQL), swap
  out the ``write_payloads_to_db`` function to connect via SQLAlchemy and use
  ``DataFrame.to_sql`` with the desired engine.

## Handling Large Batches

Point the script at a directory of Excel files by using shell globbing.  The
utility will iterate through every workbook and worksheet, skipping those that
do not contain tabular data after cleaning.  Because the script is idempotent,
rerunning it with the same database path will overwrite existing worksheet
tables, ensuring the database always reflects the most recent spreadsheets.

