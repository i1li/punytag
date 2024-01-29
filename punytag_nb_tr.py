import pandas as pd
import idna
import regex as re

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

# Load the CSV file
file_path = 'HNS-transaction-history-latest.csv'
df = pd.read_csv(file_path)

# Apply punycode_convert_validate to the 'extra.domain' column
punycode_info = df['extra.domain'].apply(lambda x: punycode_convert_validate(x) if isinstance(x, str) else ('', ''))

# Remove invalid and blank characters from 'unicode' column
df['unicode'] = [re.sub(r'(?:\\x[\da-fA-F]{2})+|\\u(?:[\da-fA-F]{4})+', '', info[0]) if info[0] and info[0] != df.at[i, 'extra.domain'] else '' for i, info in enumerate(punycode_info)]

# Tag names as 'PUNY_INVALID' if either invalid characters removed or 'unicode' is still the same as 'extra.domain'
df['PUNY_INVALID'] = [1 if (info[0] != df.at[i, 'unicode']) or (info[0] and df.at[i, 'unicode'] == df.at[i, 'extra.domain']) else '' for i, info in enumerate(punycode_info)]

# Apply tags based on punycode conversion results
df['PUNY_IDNA'] = [1 if info[1] == 'PUNY_IDNA' else '' for info in punycode_info]
df['PUNY_ALT'] = [1 if info[1] == 'PUNY_ALT' and info[0] else '' for info in punycode_info]  # Remove 'PUNY_ALT' tag when 'unicode' is empty

# Remove 'PUNY_ALT' tag when 'unicode' is blank
df.loc[df['unicode'] == '', 'PUNY_ALT'] = ''

# Create the 'tags' column
tags_columns = ['PUNY_IDNA', 'PUNY_ALT', 'PUNY_INVALID']
df['tags'] = df.apply(lambda row: ','.join(tag for tag in tags_columns if row[tag] == 1), axis=1)

# Remove individual tag columns
df.drop(columns=tags_columns, inplace=True)

# Reorder the first few columns
df = df[['extra.domain', 'unicode', 'tags'] + [col for col in df.columns if col not in ['extra.domain', 'unicode', 'tags']]]

# Save the modified DataFrame back to CSV
df.to_csv(file_path, index=False)
print(f"Program completed successfully. Output saved to {file_path}")
