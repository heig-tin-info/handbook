from bs4 import BeautifulSoup  # pip install beautifulsoup4

html = open("doc.html").read()

soup = BeautifulSoup(html, 'html.parser')

def extract_code(soup):
    code_texts = []
    for code in soup.find_all("code"):
        lines = []
        for line in code.find_all('span', recursive=False):
            line_text = line.get_text()
            lines.append(line_text)
        code_texts.append("".join(lines))
    return code_texts

extracted_code = extract_code(soup)
for code in extracted_code:
    print(":::")
    print(code)
    print(":::")
