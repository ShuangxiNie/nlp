import os
import mammoth
# from docx import Document

# def remove_headers_footers_comments(doc_path):
#     document = Document(doc_path)
#     sections = document.sections

#     for section in sections:
#         header = section.header
#         for paragraph in header.paragraphs:
#             paragraph.clear()

#         footer = section.footer
#         for paragraph in footer.paragraphs:
#             paragraph.clear()

#     for comment in document.comments:
#         comment._element.getparent().remove(comment._element)

#     temp_doc_path = "temp.docx"
#     document.save(temp_doc_path)
#     return temp_doc_path

# def extract_images(doc_path, output_dir):
#     document = Document(doc_path)
#     if not os.path.exists(output_dir):
#         os.makedirs(output_dir)
    
#     for i, rel in enumerate(document.part.rels.values()):
#         if "image" in rel.target_ref:
#             image = rel.target_part.blob
#             image_filename = f"image_{i+1}.png"
#             image_path = os.path.join(output_dir, image_filename)
#             with open(image_path, "wb") as img_file:
#                 img_file.write(image)

def convert_word2md(file_obj):
    """
    将 word 对象转换成 md
    """
    return mammoth.convert_to_markdown(file_obj)


def convert_word_to_markdown(input_file, output_file, image_dir):
    # # Remove headers, footers, and comments
    # temp_doc_path = remove_headers_footers_comments(input_file)

    # # Extract images
    # extract_images(temp_doc_path, image_dir)

    # Convert to markdown
    with open(input_file, "rb") as docx_file:
        result = convert_word2md(docx_file)
        markdown_text = result.value

    # # Replace image references in markdown
    # for i, _ in enumerate(os.listdir(image_dir)):
    #     image_ref = f"image_{i+1}.png"
    #     markdown_image_syntax = f"![Image](./{image_dir}/{image_ref})"
    #     markdown_text = markdown_text.replace(f"{{IMAGE_{i}}}", markdown_image_syntax)

    with open(output_file, "w") as markdown_file:
        markdown_file.write(markdown_text)

    # # Clean up temporary file
    # os.remove(temp_doc_path)






if __name__ == "__main__":
    input_file = "data/document.docx"
    output_file = "data/output.md"
    image_dir = "data/images"
    convert_word_to_markdown(input_file, output_file, image_dir)
