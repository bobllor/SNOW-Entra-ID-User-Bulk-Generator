# SNOW-Entra-ID-User-Bulk-Generator
A CLI program to auto generate a CSV for bulk user creation in Azure Entra ID by using reports generated through Service NOW.

This is no longer being maintained.
- The new instance of ServiceNow broke this script's bulk generation.
- The code itself is low quality (due to my experience at the time).

Only the "Manul Input" is worth being used, but it has its issues with 3 files per entry.
<br/>
I uploaded the `manual-extract.sh` bash script to alleviate this issue, move that file into the output directory and run the script.
- It automatically moves the text files out into the output directory.
- It creates a temporary CSV file that concatenates the entries in all CSV files into a single one, for easier bulk generation.

I am planning to rewrite this with a GUI instead of a CLI interface with React.