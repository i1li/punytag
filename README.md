# Punytag

Punytag adds 2 columns to your [Namebase](https://namebase.io) or [Bob Wallet](https://github.com/kyokan/bob-wallet) export files, with tags and Unicode names. Sort your Handshake domain names easier with Unicode rendering (emojis, symbols, foreign characters), Punycode validation status, and basic categorization tags.

Also includes a program to convert any list of Punycode to Unicode, or Unicode to Punycode.

- Identifies punycode status as IDNA, Alt, or invalid.
- Provides basic categorization tags for domain names based on length, letters, numbers, etc.

**What is Handshake (HNS) ?**

IDs and web addresses are the root of our online interactions. Handshake is a sovereign web address, user ID, digital wallet, and payment address. Fully decentralized, only owned and controlled by you!

[HNS is root](https://youtu.be/mhANHB6_lRU&t=28). If it's not in the [root zone](https://en.wikipedia.org/wiki/Alternative_DNS_root#Handshake), it's not web3. Here's a list of more [HNS related repos](https://github.com/stars/i1li/lists/hns).

**What is Punycode?**

"Domain names can only contain a limited set of characters so emoji and foreign character domains are puny encoded — when you type an emoji into a browser, it will look up the punycode of that emoji. In other words, the punycode xn--* string is the actual domain name, and not the emoji rendering." - [Namebase](https://support.namebase.io/en/articles/6770813-why-do-emoji-domains-begin-with-xn-strings)

## Challenge

Neither Bob Wallet, nor Namebase provides proper Punycode validation labeling on their domain pages, or export files. Users are left to manually copy and paste each Punycode into tools like punycoder.com, but even in that case, it doesn't display any Unicode when there are any invalid characters, (when in practice many of those names are still able to get at least partially rendered by the browser.)

The export files also don't include the actual visual representation (Unicode) of the Punycode, making large sets of Punycode names largely unrecognizable from each other, as just a list of names starting with 'xn--', plus random letters and numbers, rather than the recognizable emojis, symbols, and foreign script characters.

## Sortable Tags for Punycode Validation and Basic Name Categorization

- **3D:** 3 digits (numbers) - **3L:** 3 letters (letters only) - **3C:** 3 characters (letters, numbers, -, _) - and so on up to 7
- **PUNY_IDNA:** Highest level of compliance, ensuring consistent results across programs.
- **PUNY_ALT:** Second highest level of compliance, may produce inconsistent results due to alternate punycode. The punycode here still displays valid unicode, but the same emoticon or character can also be produced with different punycode. This means you could get inconsistent results when copying and pasting what appears to be the same emoticon or character, but which uses a different punycode.
- **PUNY_INVALID:** Characters don't display correctly, potentially showing as empty space, or error/filler characters.

Names tagged as PUNY_IDNA cannot have other puny tags, while PUNY_ALT and PUNY_INVALID can be tagged individually or together.

Having a tag of only PUNY_INVALID means that this name only displays blank or error characters, use the most caution with these.

PUNY_ALT names can also have the PUNY_INVALID tag if some characters display, while others are invalid, caution should also be taken when considering these names.

## Getting Started

1. Ensure Python is installed.
2. Open a terminal in the project directory.
3. Install requirements:
    ```bash
    pip install -r requirements.txt
    ```
4. Place the file(s) you'd like updated into the project directory:
   
   Namebase portfolio export (with default name: `Namebase-domains-export.csv`),
   
   Namebase transactions export (with default name: `HNS-transaction-history-latest.csv`),
   
   Bobwallet portfolio export (named: `bob.csv`), or
   
   Bob Wallet transactions export (named: `bob_tr.csv`)
5. To update your Namebase portfolio export file, run `punytag_nb.py` :
    ```bash
    python punytag_nb.py
    ```
   To update your Namebase transactions history export file, run `punytag_nb_tr.py` :
    ```bash
    python punytag_nb_tr.py
    ```
    To update your Bob Wallet portfolio export file, run `punytag_bob.py` :
    ```bash
    python punytag_bob.py
    ```
   To update your Bob Wallet transactions history export file, run `punytag_bob_tr.py` :
    ```bash
    python punytag_bob_tr.py
    ```
6.  Close and reopen the CSV file to see the updated columns. Sort the 'tags' column by ascending order for easier navigation.


7.  To convert any list of Unicode to Punycode, or Punicode to Unicode, save the appropriately named file, with one entry per line, in the project directory:

    Save your Punycode list as `puny2.csv` (or `puny2.txt`),

    Save your Unicode list as `uni2.csv` (or `uni2.txt`)
    To convert one or both of those lists, run `puny2uni.py` :
    ```bash
    python puny2uni.py
    ```

    
Your output is saved as new file(s) named `puny2uni.csv`, and/or `uni2puny.csv`


Recommended open-source lightweight software for .csv and other docs is: [LibreOffice](https://www.libreoffice.org)

