# Geographical Data Loader Script

This script loads geographical entities (US states and cities) into your MongoDB database.

## Features

- **Data Validation**: Validates state and city records before insertion
- **Error Handling**: Detailed error reporting with field-level validation
- **Multiple Input Methods**: Load from sample data or custom JSON files
- **Database Connectivity**: Checks MongoDB connection before loading
- **Progress Tracking**: Displays loading progress and summary statistics

## Usage

### Load Sample Data
```bash
python load_geo_data.py --sample
```

This loads 10 US states and 16 sample cities into your database.

### Load from JSON File
```bash
python load_geo_data.py --json data/geo_sample.json
```

### Quiet Mode (Suppress Output)
```bash
python load_geo_data.py --sample --quiet
```

## JSON Format

The input JSON file should have the following structure:

```json
{
  "states": [
    {
      "name": "New York",
      "code": "NY",
      "country_code": "USA"
    }
  ],
  "cities": [
    {
      "name": "New York City",
      "state_code": "NY"
    }
  ]
}
```

## Data Requirements

### States Collection Schema
- `name` (required, string): Full name of the state (e.g., "New York")
- `code` (required, string): State code (e.g., "NY")
- `country_code` (required, string): Country code (e.g., "USA")

### Cities Collection Schema
- `name` (required, string): City name (e.g., "New York City")
- `state_code` (required, string): State code matching a state in the states collection

## Error Handling

The script validates data and reports:
- **Missing fields**: Required fields that are empty or missing
- **Type errors**: Fields with incorrect data types
- **Duplicate keys**: States with duplicate code/country_code combinations
- **Database errors**: Connection issues and MongoDB-specific errors

## Output Example

```
============================================================
Loading sample data...
Connected to MongoDB
============================================================
Loading 10 states...
============================================================
[✓] State #1: New York (NY)
[✓] State #2: California (CA)
[✓] State #3: Texas (TX)
...
============================================================
Loading 16 cities...
============================================================
[✓] City #1: New York City (NY)
[✓] City #2: Buffalo (NY)
...
============================================================
LOADING SUMMARY
============================================================
States loaded:   10
States failed:   0
Cities loaded:   16
Cities failed:   0
============================================================
```

## Exit Codes

- `0`: Success (all data loaded)
- `1`: Failure (connection error, validation errors, or file not found)

## Notes

- The script checks MongoDB connectivity before starting the load operation
- Duplicate state keys are skipped with a message
- City loading continues even if some cities fail
- The script uses the existing database module (`data.db_connect`) for connections
- All geographic data is loaded into the `seDB` database
