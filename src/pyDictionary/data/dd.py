import gzip
import shutil

# Input and output file paths
input_file = "dictionary.json"
output_file = "dictionary.json.gz"

# Open the input and output and compress
with open(input_file, "rb") as f_in:
    with gzip.open(output_file, "wb") as f_out:
        shutil.copyfileobj(f_in, f_out)

print("Compression complete:", output_file)
