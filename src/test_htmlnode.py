import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):

    # testing HTMLNode
    def test_init_with_all_parameters(self):
        """Test initialization with all parameters provided"""
        node = HTMLNode(
            tag="a",
            value="Click here",
            children=["child1", "child2"],
            props={"href": "https://www.google.com", "target": "_blank"}
        )
        self.assertEqual(node.tag, "a")
        self.assertEqual(node.value, "Click here")
        self.assertEqual(node.children, ["child1", "child2"])
        self.assertEqual(node.props, {"href": "https://www.google.com", "target": "_blank"})
    
    def test_init_with_defaults(self):
        """Test initialization with all default parameters (None)"""
        node = HTMLNode()
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)
    
    def test_init_partial_parameters(self):
        """Test initialization with only some parameters"""
        node = HTMLNode(tag="p", value="Paragraph text")
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "Paragraph text")
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)
    
    def test_to_html_raises_not_implemented(self):
        """Test that to_html raises NotImplementedError"""
        node = HTMLNode()
        with self.assertRaises(NotImplementedError):
            node.to_html()
    
    def test_props_to_html_with_props(self):
        """Test props_to_html with properties"""
        node = HTMLNode(props={"href": "https://www.google.com", "target": "_blank"})
        result = node.props_to_html()
        # Note: dict order is preserved in Python 3.7+
        self.assertEqual(result, ' href="https://www.google.com" target="_blank"')
    
    def test_props_to_html_with_single_prop(self):
        """Test props_to_html with single property"""
        node = HTMLNode(props={"class": "container"})
        result = node.props_to_html()
        self.assertEqual(result, ' class="container"')
    
    def test_props_to_html_with_none_props(self):
        """Test props_to_html returns empty string when props is None"""
        node = HTMLNode(props=None)
        result = node.props_to_html()
        self.assertEqual(result, "")
    
    def test_props_to_html_with_empty_dict(self):
        """Test props_to_html with empty dictionary"""
        node = HTMLNode(props={})
        result = node.props_to_html()
        self.assertEqual(result, "")
    
    def test_repr_with_all_values(self):
        """Test __repr__ with all values set"""
        node = HTMLNode(
            tag="a",
            value="Link text",
            children=None,
            props={"href": "https://www.google.com", "target": "_blank"}
        )
        repr_string = repr(node)
        self.assertIn("Tag: a", repr_string)
        self.assertIn("Value: Link text", repr_string)
        self.assertIn("Children: None", repr_string)
        self.assertIn("Props:", repr_string)
        self.assertIn("href", repr_string)
        self.assertIn("https://www.google.com", repr_string)
    
    def test_repr_with_none_values(self):
        """Test __repr__ with all None values"""
        node = HTMLNode()
        repr_string = repr(node)
        self.assertIn("Tag: None", repr_string)
        self.assertIn("Value: None", repr_string)
        self.assertIn("Children: None", repr_string)
        self.assertIn("Props: None", repr_string)
    
    def test_props_to_html_multiple_props(self):
        """Test props_to_html with multiple properties in specific order"""
        node = HTMLNode(props={
            "id": "main",
            "class": "wrapper",
            "data-test": "value"
        })
        result = node.props_to_html()
        # Check that all props are present
        self.assertIn('id="main"', result)
        self.assertIn('class="wrapper"', result)
        self.assertIn('data-test="value"', result)
        # Check that each starts with a space
        self.assertTrue(result.startswith(" "))

    # testing LeafNode
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_leaf_no_value(self):
        node = LeafNode("p", None, None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_leaf_no_tag(self):
        node = LeafNode("", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), 'Click me!')

    # testing ParentNode
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
           
if __name__ == "__main__":
    unittest.main()
