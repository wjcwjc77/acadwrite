from markitdown import MarkItDown

md = MarkItDown(enable_plugins=False) # Set to True to enable plugins
result = md.convert("tsinghua_template.dotx")

with open("converted_markdown.md", "w", encoding="utf-8") as file:
    file.write(result.text_content)