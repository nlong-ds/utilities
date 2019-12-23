# csv-splitter
The alleged script prompts takes a huge .txt file and cuts it into chunks according to the user desire. It is a convenient solution to split huge lists into more manageable files that can actually be opened and analyzed through spreadsheets (e.g. excel, google sheets).

## How to use:
Create a folder with two files only:
- The script itself
- The file you wish to split into smaller chunks. 
**important**: the file format should be a .txt. This helps the `pd.read_csv` method by avoiding compicancies due to encoding. 

### Libraries required:
- os, pandas
