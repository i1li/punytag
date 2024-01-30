import pandas as pd
import idna
import regex as re
import codecs
def punycode_convert_validate(punycode_str):
    if punycode_str.startswith("xn--"):
        try:
            decoded = punycode_str.encode('ascii').decode('idna', errors='strict')
            return decoded
        except UnicodeError:
            try:
                unicode_str = idna.decode(punycode_str)
                return unicode_str
            except Exception as e:
                error_message = str(e)
                unicode_match = re.search(r"'([^']*)'", error_message)
                if unicode_match:
                    return unicode_match.group(1)
                else:
                    return ''
    else:
        return punycode_str
def unicode_to_punycode(unicode_string):
    punycode_encoder = codecs.getencoder('punycode')
    punycode_string, _ = punycode_encoder(unicode_string)
    punycode_with_prefix = f"xn--{punycode_string.decode('ascii')}"
    return punycode_with_prefix
def process_csv(input_file, output_file):
    try:
        df = pd.read_csv(input_file, header=None, names=['name'])  
        df['name'] = df['name'].astype(str)  
        if 'puny2' in input_file:
            df['punycode'] = df['name']  
            df['unicode'] = df['name'].apply(punycode_convert_validate)  
            df['unicode'] = df['unicode'].apply(lambda x: re.sub(r'(?:\\x[\da-fA-F]{2})+|\\u(?:[\da-fA-F]{4})+', '', x))  
            print("Processed punycode data")
        elif 'uni2' in input_file:
            df['unicode'] = df['name']  
            df['punycode'] = df['name'].apply(unicode_to_punycode)  
            print("Processed unicode data")
        df.drop(columns=['name'], inplace=True)  
        df.to_csv(output_file, index=False)  
        print(f"Saved processed data to {output_file}")
    except FileNotFoundError:
        print(f"Error: {input_file} not found.")
    except Exception as e:
        print(f"Error occurred during processing {input_file}: {str(e)}")
process_csv('puny2.csv', 'puny2uni.csv')
process_csv('uni2.csv', 'uni2puny.csv')
process_csv('puny2.txt', 'puny2uni.csv')
process_csv('uni2.txt', 'uni2puny.csv')
