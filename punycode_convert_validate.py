import pandas as pd
import idna
import re
def punycode_convert_validate(punycode_str):
    if punycode_str.startswith("xn--"):
        try:
            decoded = punycode_str.encode('ascii').decode('idna', errors='strict')
            return decoded, 'yes'  
        except UnicodeError:  
            try:
                unicode_str = idna.decode(punycode_str)
                return unicode_str, 'no'
            except Exception as e:
                error_message = str(e)
                unicode_match = re.search(r"'([^']*)'", error_message)
                if unicode_match:
                    return unicode_match.group(1), 'no'
                else:
                    return punycode_str, 'no'
    else:
        return '', ''
file_path = 'Namebase-domains-export.csv'
df = pd.read_csv(file_path)
punycode_info = df['name'].apply(punycode_convert_validate)
df['unicode'] = [re.sub(r'(?:\\x[\da-fA-F]{2})+|\\u(?:[\da-fA-F]{4})+', '', info[0]) if info[0] else '' for info in punycode_info]
df.loc[df['unicode'] == df['name'], 'unicode'] = ''
if 'valid_punycode' not in df.columns:
    df.insert(2, 'valid_punycode', '')
df['valid_punycode'] = [info[1] for info in punycode_info]
if 'name' in df.columns:
    output_file_path = 'Namebase-domains-export.csv'
    df.to_csv(output_file_path, index=False)
    print(f"Program completed successfully. Output saved to {output_file_path}")
else:
    print("Error: 'name' column is required in the CSV file.")
