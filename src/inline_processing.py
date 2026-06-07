import re

from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        split_node_text = node.text.split(delimiter)
        if len(split_node_text) % 2 == 0:
            raise ValueError(f"Invalid markdown text: Missing closing delimiter in node {node}")
        split_nodes = []
        for i in range(len(split_node_text)):
            if i % 2 == 0:
                split_nodes.append(TextNode(split_node_text[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(split_node_text[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes

def extract_markdown_images(text: str) -> list[tuple]:
    extracted_images = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return extracted_images

def extract_markdown_links(text: str) -> list[tuple]:
    extracted_links = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return extracted_links

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        node_text = node.text
        images = extract_markdown_images(node.text)
        if len(images) == 0:
            new_nodes.append(node)
            continue
        for image in images:
            alt_text, url = image[0], image[1]
            delimiter = f"![{alt_text}]({url})"
            split_node_text = node_text.split(delimiter)
            if len(split_node_text) != 2:
                raise ValueError(f"Invalid Markdown image syntax: Missing delimiter in node {node}")
            if split_node_text[0] != "":
                new_nodes.append(TextNode(split_node_text[0], TextType.TEXT))
            new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))
            node_text = split_node_text[1]
        if node_text != "":
            new_nodes.append(TextNode(node_text, TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        node_text = node.text
        links = extract_markdown_links(node.text)
        if len(links) == 0:
            new_nodes.append(node)
            continue
        for link in links:
            link_text, url = link[0], link[1]
            delimiter = f"[{link_text}]({url})"
            split_node_text = node_text.split(delimiter)
            if len(split_node_text) != 2:
                raise ValueError(f"Invalid Markdown link syntax: Missing delimiter in node {node}")
            if split_node_text[0] != "":
                new_nodes.append(TextNode(split_node_text[0], TextType.TEXT))
            new_nodes.append(TextNode(link_text, TextType.LINK, url))
            node_text = split_node_text[1]
        if node_text != "":
            new_nodes.append(TextNode(split_node_text[1], TextType.TEXT))
    return new_nodes

def text_to_textnodes(text: str) -> list[TextNode]:
    original_text_node = TextNode(text, TextType.TEXT)
    split_bold = split_nodes_delimiter([original_text_node], "**", TextType.BOLD)
    split_italic = split_nodes_delimiter(split_bold, "*", TextType.ITALIC)
    split_italic2 = split_nodes_delimiter(split_italic, "_", TextType.ITALIC)
    split_code = split_nodes_delimiter(split_italic2, "`", TextType.CODE)
    split_image = split_nodes_image(split_code)
    split_link = split_nodes_link(split_image)
    return split_link