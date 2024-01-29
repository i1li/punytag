# Punytag

Punytag is a tool that adds 2 columns to your [Namebase](https://namebase.io) or [Bob Wallet](https://github.com/kyokan/bob-wallet) export files, which displays tags and unicode names (emojis or foreign characters). Sort your portfolio easier with punycode status and basic tags for Handshake domain names. (HNS is root. If it's not in the rootzone, it's not web3.)

## Features

- Adds columns for "unicode" and "tags" to Namebase or Bob Wallet export files.
- Identifies punycode status as IDNA, Alt, or invalid.
- Provides basic tags for domain names.

## Punycode Tags

- **PUNY_IDNA:** Highest level of compliance, ensuring consistent results across programs.
- **PUNY_ALT:** Second highest level of compliance, may produce inconsistent results due to alternate punycode. The punycode here still displays valid unicode, but the same emoticon or character can also be produced with different punycode. This means you could get inconsistent results when copying and pasting what appears to be the same emoticon or character, but which uses a different punycode.
- **PUNY_INVALID:** Characters don't display correctly, potentially showing as empty space, or error/filler characters.

Names tagged as PUNY_IDNA cannot have other puny tags, while PUNY_ALT and PUNY_INVALID can be tagged individually or together.

PUNY_ALT names can also have the PUNY_INVALID tag if some characters display, while others are invalid, caution should also be taken when considering these names.

Having a tag of only PUNY_INVALID means that this name only displays blank or error characters, use the most caution with these.

## Basic Name Tagging

- **3D:** 3 digits (numbers)
- **3L:** 3 letters (letters only)
- **3C:** 3 characters (letters, numbers, -, _)
- and so on up to 7D

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
6. To update your Namebase portfolio export file, run punytag.py :
    ```bash
    python punytag.py
    ```
   To update your Namebase transactions history export file, run punytag_bob_tr.py :
    ```bash
    python punytag_nb_tr.py
    ```
    To update your Bob Wallet portfolio export file, run punytag_bob.py :
    ```bash
    python punytag_bob.py
    ```
   To update your Bob Wallet transactions history export file, run punytag_bob_tr.py :
    ```bash
    python punytag_bob_tr.py
    ```
7. Close and reopen the CSV file to see the updated columns. Sort the 'tags' column by ascending order for easier navigation.

   Recommended open-source lightweight software for .csv and other docs is: [LibreOffice](https://www.libreoffice.org)
