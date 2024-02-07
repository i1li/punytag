import pandas as pd
import codecs
import os
def read_csv(file_path):
    df = pd.read_csv(file_path, dtype={'tags': str})
    df['tags'] = df['tags'].apply(lambda x: x.strip() + ', All Names' if isinstance(x, str) and len(x.strip()) > 0 else 'All Names')
    return df
def format_name(row, dark_mode=False):
    if row['name'].startswith('xn--'):
        unicode_value = str(row.get('unicode', ''))
        if unicode_value.lower() == 'nan' or not unicode_value.strip():
            link_class = 'dark-mode' if dark_mode else ''
            return f'<a target="_blank" rel="noreferrer" class="{link_class}" href="https://www.namebase.io/domains/{row["name"]}">{row["name"]}</a>'
        try:
            unicode_bytes = codecs.decode(unicode_value, 'unicode_escape')
            unicode_char = unicode_bytes.encode('latin-1').decode('utf-8')
        except (ValueError, OverflowError) as e:
            unicode_char = str(e).split(':')[-1].strip()
        formatted_unicode = f' {unicode_char}'
        link_class = 'dark-mode' if dark_mode else ''
        return f'<a target="_blank" rel="noreferrer" class="{link_class}" href="https://www.namebase.io/domains/{row["name"]}">{formatted_unicode} ({row["name"]})</a>'.replace("'", "")
    return f'<a target="_blank" rel="noreferrer" href="https://www.namebase.io/domains/{row["name"]}">{row["name"]}</a>'
def check_and_tag_unicode(df):
    invalid_unicode = [
        '\U0001f2df', '\u0ccf', '\u0cce', '\u05cf', '\U0001f2c8', '\u0ffb', '\u0ff4', '\u0ff6', '\U0001eb51'
    ]
    for index, row in df.iterrows():
        if isinstance(row['unicode'], str):
            unicode_value = row['unicode']
            for char in invalid_unicode:
                if char in unicode_value:
                    df.at[index, 'tags'] = 'PUNY_INVALID' if not isinstance(row['tags'], str) else 'PUNY_INVALID, ' + row['tags']
                    unicode_value = unicode_value.replace(char, '')
            df.at[index, 'tags'] = df.at[index, 'tags'].replace('puny_alt', '').replace('puny_idna', '').strip()
            df.at[index, 'unicode'] = unicode_value
    return df
def generate_navigation_and_tag_groups(df, dark_mode=False):
    navigation_links_html = ""
    tag_groups_content = ""
    tags_dict = {}
    for _, row in df.iterrows():
        tags_list = str(row['tags']).split(',')
        for tag in tags_list:
            tag = tag.strip()
            if tag not in tags_dict:
                tags_dict[tag] = []
            tags_dict[tag].append(format_name(row, dark_mode))
    tags_sorted = ['All Names'] + sorted(set(tags_dict.keys()) - {'All Names'})
    for tag in tags_sorted:
        section_id = tag.lower().replace(' ', '-')
        names_under_tag = ''.join(f'<div class="col" data-tags="{tag}">{name}</div>' for name in tags_dict[tag])
        tag_groups_content += f'<div id="{section_id}" class="tag-section"><h2>{tag}</h2><div class="grid">{names_under_tag}</div></div>'
        navigation_links_html += f'<div class="navigation" onclick="showTagSection(\'{tag}\')">{tag}</div>'
    return navigation_links_html, tag_groups_content
def write_html_file(file_path, html_content):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(html_content)
def main(csv_file_path):
    df = read_csv(csv_file_path)
    df = check_and_tag_unicode(df)
    navigation_links_content, tag_groups_content = generate_navigation_and_tag_groups(df)
    css_style = """
<style>
.zoom-buttons {
    position: absolute;
    top: 50px;
    right: 10px;
    z-index: 1000;
}
.mode-toggle {
    position: absolute;
    top: 10px;
    right: 10px;
    z-index: 1000;
}
button {
    font-size: .9em;
    font-weight: 555;
    background-image: radial-gradient( circle farthest-corner at 22.4% 21.7%, rgba(4,189,228,1) 0%, rgba(2,83,185,1) 100.2% );
}
body {
    background-color: #ffffff;
    color: #000000;
}
body.dark-mode, a:link.dark-mode, a:visited.dark-mode {
    background-color: #000000;
    color: #ffffff;
}
body {
    padding: .7em;
    font-weight: 600;
    text-align: center;
    text-transform: full-size-kana;
}
a:link, a:visited {
    color: black;
    text-decoration: overline dashed;
    text-decoration-thickness: 1px;
}
a:hover {
    text-decoration: wavy underline;
    text-decoration-thickness: 1px;
}
input {
    padding: .7em;
    font-size: 1em;
    font-weight: bold;
    background-image: radial-gradient( circle farthest-corner at 22.4% 21.7%, rgba(4,189,228,1) 0%, rgba(2,83,185,1) 100.2% );
}
.grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: .5em;
    padding: .5em;
}
.col {
    padding: .7em;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}
.col:hover {
    text-transform: full-width;
    text-transform: uppercase;
    text-overflow: ellipsis;
    font-size: 1.1em;
    overflow: clip;
    margin: -1em;
    margin-top: -.1em;
}
.navigation-container {
    display: flex;
    flex-wrap: wrap;
    gap: .5em;
    padding: .5em;
    background-image: linear-gradient(to right, #33001b, #C70039);
    border-color: #ff0084;
    border: #ff0084;
    border-style: dotted; 
    }
.navigation {
    padding: .5em;
    min-width: 150px;
    cursor: pointer;
    color: blue;
    text-transform: full-width;
    text-shadow: 1px 1px 2px red, 0 0 1em blue, 0 0 0.2em blue;
    text-shadow: .5px .5px 1px gray, 0 0 .1em silver, 0 0 0.1em green;
    background-color: rgba(111, 111, 111, 0.5);
}
.navigation:hover {
    text-decoration: dashed underline;
    text-transform: full-width;
    text-shadow: 1px 1px 2px blue, 0 0 1em red, 0 0 0.2em red;
    text-shadow: .5px .5px 1px red, 0 0 .5em silver, 0 0 0.1em orange;
    border-color: rgba( 255, 151, 0 , .5);
    border-style: double;
    margin: -3px;
    background-color: rgba( 97, 0, 255 , 0.6 );
}
</style>
    """
    javascript_code = """
<script>
let darkMode = true;
const prefersLightMode = window.matchMedia && window.matchMedia('(prefers-color-scheme: light)').matches;
if (prefersLightMode) {
    toggleDarkMode();
}
function toggleDarkMode() {
    darkMode = !darkMode;
    document.body.classList.toggle("dark-mode");
    const links = document.querySelectorAll('a');
    links.forEach((link) => {
        if (darkMode) {
            link.classList.add('dark-mode');
        } else {
            link.classList.remove('dark-mode');
        }
    });
}
const modeToggle = document.getElementById('mode-toggle');
modeToggle.addEventListener('click', toggleDarkMode);
document.getElementById("zoom-in").addEventListener("click", function() {
    document.body.style.fontSize = parseInt(window.getComputedStyle(document.body).fontSize) + 3 + "px";
});
document.getElementById("zoom-out").addEventListener("click", function() {
    document.body.style.fontSize = parseInt(window.getComputedStyle(document.body).fontSize) - 3 + "px";
});
function showTagSection(tag) {
    var sectionId = tag.toLowerCase().replace(' ', '-');
    var section = document.getElementById(sectionId);
    if (section) {
        var sections = document.getElementsByClassName('tag-section');
        for (var i = 0; i < sections.length; i++) {
            sections[i].style.display = "none";
        }
        section.style.display = "block";
    }
}
function shuffleNames() {
    var tagSections = document.querySelectorAll('.tag-section');
    tagSections.forEach(function (section) {
        var names = Array.from(section.querySelectorAll('.col'));
        var currentIndex = names.length, randomIndex;
        while (currentIndex > 0) {
            randomIndex = Math.floor(Math.random() * currentIndex);
            currentIndex--;
            [names[currentIndex], names[randomIndex]] = [names[randomIndex], names[currentIndex]];
        }
        var grid = section.querySelector('.grid');
        grid.innerHTML = '';
        names.forEach(function (name) {
            grid.appendChild(name);
        });
    });
}
function searchNames() {
    var input = document.getElementById('search-input');
    if (input) {
        var filter = input.value.toLowerCase();
        var names = document.getElementsByClassName('col');
        for (var i = 0; i < names.length; i++) {
            var name = names[i].innerText.toLowerCase();
            if (name.includes(filter)) {
                names[i].style.display = "block";
            } else {
                names[i].style.display = "none";
            }
        }
    }
}
var searchInput = document.getElementById('search-input');
if (searchInput) {
    searchInput.addEventListener('keyup', function() {
        searchNames();
    });
}
showTagSection('All Names');
shuffleNames();
function getRandomColor() {
    let color = Math.floor(Math.random() * 16777215).toString(16);
    while (color.length < 6) {
        color = '0' + color;
    }
    return '#' + color;
}
const links = document.querySelectorAll('a');
links.forEach((link) => {
    const randomColor = getRandomColor();
    link.style.textDecorationColor = randomColor;
    if (darkMode) {
        document.body.classList.add("dark-mode");
        link.classList.add('dark-mode');
    } else {
        document.body.classList.remove("dark-mode");
        link.classList.remove('dark-mode');
    }
});
window.addEventListener('DOMContentLoaded', () => {
    const addTooltipToNames = () => {
        const cols = document.querySelectorAll('.col');
        cols.forEach(col => {
            col.setAttribute('title', col.textContent.trim());
        });
    };

    addTooltipToNames();
});
    </script>
    """
    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Portfolio</title>
{css_style}
</head>
<body>
<div class="buttons-container">
<div class="mode-toggle">
    <button id="mode-toggle">🌙 / ☀️</button>
</div>
<div class="zoom-buttons">
    <button id="zoom-out">-</button>
    <button id="zoom-in">+</button>
</div>
</div>
<div class="navigation-container">
{navigation_links_content}
</div>
<div class="content">
    <input type="text" id="search-input" placeholder="Search...">
    {tag_groups_content}
</div>
{javascript_code}
</body>
</html>
    """
    project_dir = os.path.dirname(os.path.abspath(__file__))
    write_html_file(os.path.join(project_dir, 'index.html'), html_content)
if __name__ == "__main__":
    main('Namebase-domains-export.csv')