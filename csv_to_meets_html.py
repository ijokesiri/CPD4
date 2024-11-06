import csv
import os
import re
import random
from urllib.parse import quote

def csv_to_html(csv_filename, output_folder):
    # Derive the HTML filename by replacing the CSV extension with '.html' in the meets folder
    html_filename = os.path.join(output_folder, os.path.splitext(os.path.basename(csv_filename))[0] + '.html')

    with open(csv_filename, mode='r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        rows = list(reader)

        # Ensure there are at least 5 rows for valid HTML generation
        if len(rows) < 5:
            print("CSV file must have at least 5 rows.")
            return

        # Extract values from the first five rows
        link_text = rows[0][0]
        h2_text = rows[1][0]
        link_url = rows[2][0]
        summary_text = rows[3][0]

        # Initialize HTML content
        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{link_text}</title>
<link rel="stylesheet" href="../css/reset.css">
<link rel="stylesheet" href="../css/style.css">
</head>
<body>
<a href="#main">Skip to Main Content</a>
<nav>
    <ul>
        <li><a href="../index.html">Home Page</a></li>
        <li><a href="#summary">Summary</a></li>
        <li><a href="#team-results">Team Results</a></li>
        <li><a href="#individual-results">Individual Results</a></li>
        <li><a href="#gallery">Gallery</a></li>
    </ul>
</nav>
<header>
    <h1><a href="{link_url}">{link_text}</a></h1>
    <h2>{h2_text}</h2>
</header>
<main id="main">
    <section class="summary" id="summary">
    <h2>Race Summary</h2>
    <p>{summary_text}</p>
    </section>

    <section id="team-results">
        <h2>Team Results</h2>
        <table>
"""

        # Process the remaining rows (after the first five) for Team Results and Individual Results
        table_start = True
        for row in rows[4:]:
            if len(row) == 3:
                if row[0] == "Place":
                    html_content += f"<tr><th>{row[0]}</th><th>{row[1]}</th><th>{row[2]}</th></tr>\n"
                else:
                    html_content += f"<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td></tr>\n"
            elif len(row) == 8 and row[5].strip().lower() == 'ann arbor skyline':
                if table_start:
                    table_start = False
                    html_content += "</table>\n</section>\n<section id='individual-results'>\n<h2>Individual Results</h2>"
                
                place, grade, name, _, time, _, _, profile_pic = row
                html_content += f"""
<section class="athlete-section" id="athletes">
    <div class="athlete-card">
        <div class="athlete">
            <figure> 
                <img src="../images/profiles/{profile_pic}" width="200" alt="Profile picture of {name}"> 
                <figcaption>{name}</figcaption>
            </figure>
            <dl>
                <dt>Place</dt><dd>{place}</dd>
                <dt>Time</dt><dd>{time}</dd>
                <dt>Grade</dt><dd>{grade}</dd>
            </dl>
        </div>
    </div>
</section>
"""

        # Generate image gallery
        html_content += """</section>\n<section id="gallery">\n<h2>Gallery</h2>"""
        html_content += create_meet_image_gallery(link_url)

        # Close the HTML document
        html_content += """
   </section>
   </main>   
   <footer>
        <p>Skyline High School<br>
        <address>2552 North Maple Road<br>Ann Arbor, MI 48103</address><br>
        <a href="https://sites.google.com/aaps.k12.mi.us/skylinecrosscountry2021/home">XC Skyline Page</a><br>
        Follow us on Instagram <a href="https://www.instagram.com/a2skylinexc/" aria-label="Instagram"><i class="fa-brands fa-instagram"></i></a>
    </footer>
</body>
</html>
"""

        # Save HTML content to a file in the meets folder
        with open(html_filename, 'w', encoding='utf-8') as htmlfile:
            htmlfile.write(html_content)
        print(f"HTML file '{html_filename}' created successfully.")

def process_meet_files():
    meets_folder = os.path.join(os.getcwd(), "meets")
    csv_files = [f for f in os.listdir(meets_folder) if f.endswith('.csv')]

    if not csv_files:
        print(f"No CSV files found in folder: {meets_folder}")
        return

    for csv_file in csv_files:
        csv_file_path = os.path.join(meets_folder, csv_file)
        csv_to_html(csv_file_path, meets_folder)

def extract_meet_id(url):
    match = re.search(r"/meet/(\d+)", url)
    if match:
        return match.group(1)
    else:
        raise ValueError("Meet ID not found in URL.")

def select_random_photos(folder_path, num_photos=12):
    all_files = os.listdir(folder_path)
    image_files = [f for f in all_files if f.endswith(('.png', '.jpg', '.jpeg', '.gif'))]
    
    if len(image_files) < num_photos:
        raise ValueError("Not enough images in the folder.")
    
    return random.sample(image_files, num_photos)

def generate_image_tags(image_files, folder_path):
    return "\n".join(f'<img src="../{os.path.join(folder_path, img)}" width="200" alt="">' for img in image_files)

def create_meet_image_gallery(url):
    meet_id = extract_meet_id(url)
    folder_path = f'images/meets/{meet_id}/'
    
    if not os.path.exists(folder_path):
        return "<p>No images available for this meet.</p>"
    
    selected_photos = select_random_photos(folder_path)
    return generate_image_tags(selected_photos, folder_path)

def generate_index_page():
    html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Athlete Website: Home Page</title>
    <link rel="stylesheet" href="css/style.css">
</head>
<body>
    <header>
        <h1>Athlete Website</h1>
        <div class="topnav">
            <a href="meets.html">Meets</a>
        </div>
    </header>
    <div id="main-content">
        <h2>Welcome to the Athlete Information Site</h2>
        <p>This website provides information about athletes, their records, and upcoming meets.</p>
    </div>
    <footer>
        <p>Skyline High School</p>
    </footer>
</body>
</html>
'''
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)

def generate_meets_list_page():
    html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Meets List</title>
    <link rel="stylesheet" href="css/style.css">
</head>
<body>
    <header>
        <h1>Meets List</h1>
        <div class="topnav">
            <a href="index.html">Home</a>
        </div>
    </header>
    <div id="main-content">
        <h2>List of Meets</h2>
        <ul>
'''

    meets_folder = 'meets'
    meet_files = sorted({f for f in os.listdir(meets_folder) if f.endswith('.html')})
    for meet_file in meet_files:
        meet_name = os.path.splitext(meet_file)[0]
        meet_name_encoded = quote(meet_name)
        html_content += f'<li><a href="{meets_folder}/{meet_name_encoded}.html">{meet_name}</a></li>\n'

    html_content += '''
        </ul>
    </div>
    <footer>
        <p>Skyline High School</p>
    </footer>
</body>
</html>
'''

    with open('meets.html', 'w', encoding='utf-8') as f:
        f.write(html_content)

# Run the functions
process_meet_files()
generate_index_page()
generate_meets_list_page()
