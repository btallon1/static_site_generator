import unittest
from inline_processing import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes
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

    def test_extract_markdown_images_2(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png"), ("second image", "https://i.imgur.com/3elNhQu.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](www.boot.dev)"
        )
        self.assertListEqual([("link", "www.boot.dev")], matches)

    def test_split_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_image_single(self):
        node = TextNode(
            "![image](https://www.example.COM/IMAGE.PNG)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://www.example.COM/IMAGE.PNG"),
            ],
            new_nodes,
        )
    
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
            )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                )
            ],
            new_nodes
        )

    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            nodes
        )