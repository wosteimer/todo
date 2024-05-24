from builder.styler import Styler
from builder.tags import Div

Root = Styler.stylize(
    Div,
    """
    width: 100vw;
    height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    @include color-scheme{
        background-color: color-scheme-get("background");
    }
""",
)
