import unittest
from textprocessing import split_nodes_delimiter, extract_markdown_images, extract_markdown_links
from textnode import TextNode, TextType

class TestTextProcessing(unittest.TestCase):
    def test_split_nodes_delimiter_bold(self):
        old_nodes = [
            TextNode("The following text is **bold text** for testing", TextType.TEXT),
            TextNode("Further **bold text** testing", TextType.TEXT),
        ]
        new_nodes = [
            TextNode("The following text is ", TextType.TEXT),
            TextNode("bold text", TextType.BOLD),
            TextNode(" for testing", TextType.TEXT),
            TextNode("Further ", TextType.TEXT),
            TextNode("bold text", TextType.BOLD),
            TextNode(" testing", TextType.TEXT),
        ]
        output = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
        self.assertEqual(new_nodes, output)

    def test_split_nodes_delimiter_italic(self):
        old_nodes = [
            TextNode("The following text is *italic text* for testing", TextType.TEXT),
            TextNode("Further *italic text* testing", TextType.TEXT),
        ]
        new_nodes = [
            TextNode("The following text is ", TextType.TEXT),
            TextNode("italic text", TextType.ITALIC),
            TextNode(" for testing", TextType.TEXT),
            TextNode("Further ", TextType.TEXT),
            TextNode("italic text", TextType.ITALIC),
            TextNode(" testing", TextType.TEXT),
        ]
        output = split_nodes_delimiter(old_nodes, "*", TextType.ITALIC)
        self.assertEqual(new_nodes, output)

    def test_split_nodes_delimiter_code(self):
        old_nodes = [
            TextNode("The following text is `code` for testing", TextType.TEXT),
            TextNode("Further `code` testing", TextType.TEXT),
        ]
        new_nodes = [
            TextNode("The following text is ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" for testing", TextType.TEXT),
            TextNode("Further ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" testing", TextType.TEXT),
        ]
        output = split_nodes_delimiter(old_nodes, "`", TextType.CODE)
        self.assertEqual(new_nodes, output)

    def test_split_nodes_delimiter_error(self):
        node = TextNode("This node will cause an *error of type ValueError**", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "**", TextType.BOLD)

    def test_split_nodes_delimiter_error2(self):
        node = TextNode("Another error test with `code", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "`", TextType.CODE)

    def test_split_nodes_delim_texttypebold(self):
        old_nodes = [
            TextNode("This node won't be split", TextType.BOLD),
            TextNode("Neither will this node", TextType.BOLD),
        ]
        new_nodes = [
            TextNode("This node won't be split", TextType.BOLD),
            TextNode("Neither will this node", TextType.BOLD),
        ]
        output = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
        self.assertEqual(new_nodes, output)

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](www.boot.dev)"
        )
        self.assertListEqual([("link", "www.boot.dev")], matches)

    