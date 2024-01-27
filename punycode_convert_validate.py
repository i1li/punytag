import pandas as pd
import idna
import re

def punycode_convert_validate(punycode_str):
    if punycode_str.startswith("xn--"):
        try:
            decoded = punycode_str.encode('ascii').decode('idna', errors='strict')
            return decoded, 'PUNY_IDNA'
        except UnicodeError:
            try:
                unicode_str = idna.decode(punycode_str)
                return unicode_str, 'PUNY_ALT'
            # Strip the unicode from the error message
            except Exception as e:
                error_message = str(e)
                unicode_match = re.search(r"'([^']*)'", error_message)
                if unicode_match:
                    return unicode_match.group(1), 'PUNY_ALT'
                else:
                    return punycode_str, 'PUNY_INVALID'
    else:
        return '', ''

# Load the CSV file
file_path = 'Namebase-domains-export.csv'
df = pd.read_csv(file_path)

# Apply punycode_convert_validate to the 'name' column
punycode_info = df['name'].apply(punycode_convert_validate)

# Create columns for each tag - 3D = 3 digits (numbers), 3L = 3 letters, 3C = 3 characters, etc
df['3D'] = df['name'].apply(lambda x: 1 if x.isdigit() and len(x) == 3 else '')
df['3L'] = df['name'].apply(lambda x: 1 if x.isalpha() and len(x) == 3 else '')
df['3C'] = df.apply(lambda x: 1 if len(x['name']) == 3 and not x['3L'] and not x['3D'] else '', axis=1)
df['4D'] = df['name'].apply(lambda x: 1 if x.isdigit() and len(x) == 4 else '')
df['4L'] = df['name'].apply(lambda x: 1 if x.isalpha() and len(x) == 4 else '')
df['4C'] = df.apply(lambda x: 1 if len(x['name']) == 4 and not x['4L'] and not x['4D'] else '', axis=1)
df['5D'] = df['name'].apply(lambda x: 1 if x.isdigit() and len(x) == 5 else '')
df['5L'] = df['name'].apply(lambda x: 1 if x.isalpha() and len(x) == 5 else '')
df['6D'] = df['name'].apply(lambda x: 1 if x.isdigit() and len(x) == 6 else '')
df['7D'] = df['name'].apply(lambda x: 1 if x.isdigit() and len(x) == 7 else '')

# Remove invalid and blank characters from 'unicode' column
df['unicode'] = [re.sub(r'(?:\\x[\da-fA-F]{2})+|\\u(?:[\da-fA-F]{4})+', '', info[0]) if info[0] and info[0] != df.at[i, 'name'] else '' for i, info in enumerate(punycode_info)]

# Remove 'PUNY_ALT' tag when 'unicode' is blank
df.loc[df['unicode'] == '', 'PUNY_ALT'] = ''

# Tag names as 'PUNY_INVALID' if either invalid characters removed or 'unicode' is still the same as 'name'
df['PUNY_INVALID'] = [1 if (info[0] != df.at[i, 'unicode']) or (info[0] and df.at[i, 'unicode'] == df.at[i, 'name']) else '' for i, info in enumerate(punycode_info)]

# Apply tags based on punycode conversion results
df['PUNY_IDNA'] = [1 if info[1] == 'PUNY_IDNA' else '' for info in punycode_info]
df['PUNY_ALT'] = [1 if info[1] == 'PUNY_ALT' and info[0] else '' for info in punycode_info]  # Remove 'PUNY_ALT' tag when 'unicode' is empty

# Create the 'tags' column
tags_columns = ['3D', '3L', '3C', '4D', '4L', '4C', '5D', '5L', '6D', '7D', 'PUNY_IDNA', 'PUNY_ALT', 'PUNY_INVALID']
df['tags'] = df.apply(lambda row: ','.join(tag for tag in tags_columns if row[tag] == 1), axis=1)

# Remove individual tag columns
df.drop(columns=tags_columns, inplace=True)

# Reorder the first five columns
df = df[['name', 'unicode', 'price_hns', 'tags', 'description'] + [col for col in df.columns if col not in ['name', 'unicode', 'price_hns', 'tags', 'description']]]

# Save the modified DataFrame back to CSV
df.to_csv(file_path, index=False)
print(f"Program completed successfully. Output saved to {file_path}")
