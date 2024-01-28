import pandas as pd
import idna
import regex as re
import math

def punycode_convert_validate(punycode_str):
    if punycode_str.startswith("xn--"):
        try:
            decoded = punycode_str.encode('ascii').decode('idna', errors='strict')
            return decoded, 'PUNY_IDNA'
        except UnicodeError:
            try:
                unicode_str = idna.decode(punycode_str)
                return unicode_str, 'PUNY_ALT'
            except Exception as e:
                error_message = str(e)
                unicode_match = re.search(r"'([^']*)'", error_message)
                if unicode_match:
                    return unicode_match.group(1), 'PUNY_ALT'
                else:
                    return punycode_str, 'PUNY_INVALID'
    else:
        return '', ''

# Load the CSV file with header
file_path = 'bob_tr.csv'
df = pd.read_csv(file_path)

# Function to process each row
def process_row(row):
    if isinstance(row['domains'], str):
        names = row['domains'].split(',')
        puny_names = []
        for name in names:
            unicode_name, tag = punycode_convert_validate(name.strip())
            if tag.startswith('PUNY'):
                puny_names.append(f"{name.strip()} ({unicode_name})")
            else:
                puny_names.append(name.strip())
        return ', '.join(puny_names)
    elif isinstance(row['domains'], float) and math.isnan(row['domains']):
        return ''  # Return empty string if cell is NaN
    else:
        return str(row['domains'])  # Return cell value as string

# Apply the processing function to each row in 'domains' column
df['domains'] = df.apply(process_row, axis=1)

# Save the modified DataFrame back to CSV without 'name', 'unicode', or 'tags' columns
df.to_csv(file_path, index=False)
print(f"Program completed successfully. Output saved to {file_path}")
