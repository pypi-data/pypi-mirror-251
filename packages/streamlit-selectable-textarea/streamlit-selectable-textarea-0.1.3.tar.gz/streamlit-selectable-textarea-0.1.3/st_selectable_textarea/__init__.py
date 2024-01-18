__version__ = '0.1.3'
import os
import streamlit.components.v1 as components

_RELEASE = True


if not _RELEASE:
    _component_func = components.declare_component(
        "st_selectable_textarea",
        url="http://localhost:3001",
    )
else:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _component_func = components.declare_component(
        "st_selectable_textarea", path=build_dir)


def st_selectable_textarea(value="", key=None):
    """Create a new instance of "st_selectable_textarea".

    Parameters
    ----------
    value: str
        The text to display in the component.
    key: str or None
        An optional key that uniquely identifies this component. If this is
        None, and the component's arguments are changed, the component will
        be re-mounted in the Streamlit frontend and lose its current state.

    Returns
    -------
    str
        Returns the value text dragged with the mouse in the textarea.

    """
    component_value = _component_func(value=value, key=key, default=0)
    return component_value


if not _RELEASE:
    import streamlit as st
    text_input = st.text_input("Enter a text", value="Streamlit")

    dragged_area = st_selectable_textarea(value=text_input, key="foo")
    st.text_area(label="RES", value=dragged_area)
    st.text_area(label="RS", value="asdds")
