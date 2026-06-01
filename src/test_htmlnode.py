import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, TextType, text_node_to_html_node

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("h1", "Test Header")
        node2 = HTMLNode("h1", "Test Header")
        self.assertEqual(node, node2)

    def test_eq2(self):
        node = HTMLNode("h4", 
                        None,
                        [HTMLNode("a", "Learn to code", None, {"href": "https://www.boot.dev"})],
                        )
        node2 = HTMLNode("h4", 
                        None,
                        [HTMLNode("a", "Learn to code", None, {"href": "https://www.boot.dev"})],
                        )
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = HTMLNode("h1", "Test Header")
        node2 = HTMLNode("h1", "Test Header2")
        self.assertNotEqual(node, node2)

    def test_props_to_html(self):
        node = HTMLNode("a", "Learn to code", None, {"href": "https://www.boot.dev"})
        props_to_html = node.props_to_html()
        self.assertEqual(props_to_html,
                         ' href="https://www.boot.dev"')
        
    def test_leaf_eq(self):
        node = LeafNode("p", "Hello, world!")
        node2 = LeafNode("p", "Hello, world!")
        self.assertEqual(node, node2)
    
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Learn to code", {"href": "https://www.boot.dev"})
        self.assertEqual(node.to_html(),
                         '<a href="https://www.boot.dev">Learn to code</a>')
        
    def test_parent_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_parent_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    
    def test_parent_to_html_with_props(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node], {"class": "container"})
        self.assertEqual(
            parent_node.to_html(),
            '<div class="container"><span>child</span></div>',
        )
    
    def test_parent_to_html_with_props_and_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node], {"class": "container"})
        self.assertEqual(
            parent_node.to_html(),
            '<div class="container"><span><b>grandchild</b></span></div>',
        )

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
    
    def test_bold(self):
        node = TextNode("This is bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is bold text")

    def test_italic(self):
        node = TextNode("This is italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is italic text")

    def test_code(self):
        node = TextNode("This is code text", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is code text")

    def test_link(self):
        node = TextNode("This is a link", TextType.LINK, "https://www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link")
        self.assertEqual(html_node.props, {"href": "https://www.boot.dev"})

    def test_image(self):
        node = TextNode("This is an image", TextType.IMAGE, "https://www.boot.dev/image.jpg")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, None)
        self.assertEqual(html_node.props, {"src": "https://www.boot.dev/image.jpg", "alt": "This is an image"})


if __name__ == "__main__":
    unittest.main()