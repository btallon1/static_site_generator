import unittest
from htmlnode import HTMLNode, LeafNode

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
        print(f"node.props = {node.props}")
        self.assertEqual(node.to_html(),
                         '<a href="https://www.boot.dev">Learn to code</a>')
        

if __name__ == "__main__":
    unittest.main()