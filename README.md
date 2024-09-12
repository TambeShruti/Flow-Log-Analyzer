# Flow-Log-Analyzer


This program parses a file containing flow log data and maps each row to a tag based on a lookup table defined in a CSV file. It handles case-insensitive matches and supports flow log files up to 10 MB and lookup files with up to 10,000 mappings.

## Requirements

- Python 3.x
- Standard Python libraries: `csv`, `os`, `unittest`, `collections`

## Files

1. **`main.py`**: Contains the main implementation of the program.
2. **`test_flow_log_processing.py`**: Contains unit tests for the program.
3. **`flow_logs.txt`**: Sample input file with flow log data.
4. **`lookup.csv`**: Sample lookup table for mapping destination ports and protocols to tags.
5. **`output.csv`**: Output file where results are written.

## Assumptions

- The program only supports the default log format and version 2. Custom log formats are not supported.
- The lookup table is case-insensitive, and both the protocol names in the flow logs and lookup table should be in lowercase.
- The flow log file size is assumed to be up to 10 MB, and the lookup file can have up to 10,000 mappings.

## Usage

1. **Prepare Input Files**:
   - Ensure `flow_logs.txt` and `lookup.csv` are available in the same directory as `main.py`.

2. **Run the Program**:
   ```bash
   python main.py

The program will read the `lookup.csv` file, process the `flow_logs.txt` file, and write the results to `output.csv`.

## How It Works

1. **Load Lookup Table**:
   - The `load_lookup_table` function reads the `lookup.csv` file and creates a dictionary mapping `(dstport, protocol)` tuples to tags.

2. **Process Flow Logs**:
   - The `process_flow_logs` function reads the `flow_logs.txt` file, parses each row to extract the destination port and protocol, maps them using the lookup table, and counts the occurrences of each tag and port/protocol combination.

3. **Write Results**:
   - The `write_results` function writes the tag counts and port/protocol combination counts to `output.csv`.

## Tests

Unit tests are provided in `test_flow_log_processing.py`:

- **`test_load_lookup_table`**: Verifies correct loading of the lookup table.
- **`test_process_flow_logs`**: Checks the processing of flow logs and mapping to tags.
- **`test_write_results`**: Validates the output file contents.

Run the tests with:
```bash
python -m unittest test_flow_log_processing.py
```
## Time Complexity and Space Complexity Analysis:
- Loading the lookup table (`load_lookup_table`):
  Time: O(L), where L is the number of rows in the lookup CSV file.
- Processing flow logs (`process_flow_logs`):
  Time: O(F), where F is the number of lines in the flow log file.
- Writing results (`write_results`):
  Time: O(T + P), where T is the number of unique tags, and P is the number of unique port/protocol combinations.

Space Complexity:
- Loading the lookup table:
  Space: O(L), for storing all the mappings from the lookup file.
- Processing flow logs:
  Space: O(F + L), for storing tag counts and port/protocol combinations in dictionaries, plus the lookup table.

Overall Complexity:
- Time: O(F + L)
- Space: O(F + L)
  This means the performance depends on the size of the flow log file (F) and the number of mappings in the lookup table (L).

## Additional Analysis
The program uses a dictionary for efficient lookups, ensuring that even with large files, the processing remains fast.
Case-insensitive matches are handled by converting protocol names to lowercase.

## Known Issues
The program does not support custom log formats or versions other than the default.
