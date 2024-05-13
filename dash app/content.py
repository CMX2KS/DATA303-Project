def import_html(filepath):
    with open(filepath, 'r+', encoding='utf-8') as file:
        return file.read()
    
content = {1:import_html('section_content/Section 1.txt'),
           2:import_html('section_content/Section 2.txt'),
           3:import_html('section_content/Section 3.txt'),
           4:import_html('section_content/Section 4.txt')}

def get_section(key):
    return content[key]