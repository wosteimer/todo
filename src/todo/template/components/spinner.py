from builder.styler import Styler
from builder.tags import Div

# fmt: off
Spinner = Styler.stylize(Div, """
    display: none;
    width: 12px;
    height: 12px;
    border-radius: 50%;
    border: 1px solid #98979B;
    border-top: 1px solid #f6f5f4;
    animation: spin 0.8s infinite linear;
    
    .htmx-request &{
        display: block;
    }
""")
# fmt: on
