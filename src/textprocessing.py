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
    extracted_images = re.findall(r"!\[(\w+)\]\((.*?)\)", text)
    return extracted_images

def extract_markdown_links(text: str) -> list[tuple]:
    extracted_links = re.findall(r"\[(\w+)\]\((.*?)\)", text)
    return extracted_links

