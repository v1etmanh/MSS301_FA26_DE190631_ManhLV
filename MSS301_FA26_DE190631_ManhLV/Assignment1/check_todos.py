import docx

doc = docx.Document('Assignment 1_DE190685_ManhLV.docx')

todos = []
current_todo = None

for i, p in enumerate(doc.paragraphs):
    text = p.text.strip()
    drawings = len(p._p.xpath('.//w:drawing'))
    # Filter out table of contents (which has 1.1.TODO, 1.2.TODO, etc.)
    # In body, headings are: 'TODO 0.1 Tạo thư mục gốc', 'TODO 0.2...', 'TODO 0.3', etc.
    is_toc = any(text.startswith(f"{x}.") for x in range(1, 15))
    if 'TODO ' in text and not is_toc:
        if current_todo:
            todos.append(current_todo)
        current_todo = {
            'header_idx': i,
            'header_text': text,
            'last_img_idx': None,
            'all_img_indices': []
        }
    elif current_todo:
        if drawings > 0:
            current_todo['all_img_indices'].append(i)
            current_todo['last_img_idx'] = i

if current_todo:
    todos.append(current_todo)

print(f"Total detected TODO sections: {len(todos)}")
with open('detected_todos.txt', 'w', encoding='utf-8') as f:
    for t in todos:
        line = f"Header P{t['header_idx']}: {t['header_text']} -> Images: {t['all_img_indices']}"
        f.write(line + "\n")
print(f"Done writing {len(todos)} todos to detected_todos.txt")
