# streamlit-selectable-textarea

Streamlit components with selectable text fields

## Installation instructions

```sh
pip install streamlit-selectable-textarea
```

## Usage instructions

```python
import streamlit as st
from st_selectable_textarea import st_selectable_textarea

text_input = st.text_input("Enter a text", value="Streamlit")

dragged_area = st_selectable_textarea(value=text_input, key="foo")

st.write(label="result", value=dragged_area)

```