from ..core import *
from .Markers import *

class HTMLDoubleTagFactory:
    @staticmethod
    def create_tag_class(tag_name, standard_attrs=None, bool_attrs=None):
        class DynamicHTMLTag(DoubleMarker):
            def __init__(self, innerText="", innerHTML=None, **attrs):
                super().__init__(
                    tag_name.lower(),
                    innerHTML if innerHTML is not None else HTMLSet() << String(innerText),
                    **attrs
                )
                
                if standard_attrs:
                    for attr in standard_attrs:
                        if attr in attrs:
                            self.setAttribute(attr.replace("_",""), attrs[attr])
                
                if bool_attrs:
                    for attr in bool_attrs:
                        if attrs.get(attr, False):
                            self.setBoolAttributes(attr)
        
        return DynamicHTMLTag

    @staticmethod
    def __create_custom_tag_help__(tag_name, standard_attrs=None, bool_attrs=None):
        """Create and register a custom HTML tag dynamically.
        
        :param tag_name: (str) Name of the custom tag
        :param standard_attrs: (list) List of standard attributes
        :param bool_attrs: (list) List of boolean attributes
        
        :return: The created custom tag class
        :raises ValueError: If tag_name is not a string or is empty, or if the tag already exists

        Example:

            MyTag = HTMLDoubleTagFactory.create_custom_tag(
                'MyTag',
                standard_attrs=['data-id'],
                bool_attrs=['active']
            )
            tag = MyTag('Content', data_id='123', active=True)
        """
        if not isinstance(tag_name, str) or not tag_name:
            raise ValueError("Tag name must be a non-empty string")
            
        if tag_name in globals():
            raise ValueError(f"Tag '{tag_name}' already exists")
            
        tag_class = HTMLDoubleTagFactory.create_tag_class(
            tag_name,
            standard_attrs or [],
            bool_attrs or []
        )
        
        globals()[tag_name] = tag_class
        return tag_class

__TAG_CONFIGS = DoubleMarkers

for tag_name, config in __TAG_CONFIGS.items():
    globals()[tag_name] = HTMLDoubleTagFactory.create_tag_class(
        tag_name,
        config['standard_attrs'],
        config['bool_attrs']
    )


def customDoubleTag(tag_name, standard_attrs=None, bool_attrs=None):
    """Create and register a custom HTML tag dynamically.
        
        :param tag_name: (str) Name of the custom tag
        :param standard_attrs: (list) List of standard attributes
        :param bool_attrs: (list) List of boolean attributes
        
        :return: The created custom tag class
        :raises ValueError: If tag_name is not a string or is empty, or if the tag already exists

        Example:

            MyTag = customDoubleTag(
                'MyTag',
                standard_attrs=['data-id'],
                bool_attrs=['active']
            )
            tag = MyTag('Content', data_id='123', active=True)
    """
    return HTMLDoubleTagFactory.__create_custom_tag_help__(
        tag_name,
        standard_attrs or [],
        bool_attrs or []
    )
