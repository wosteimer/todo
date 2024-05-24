from builder.styler import Styler
from builder.tags import Button, Form, Input, Span

# fmt: off
Container = Styler.stylize(Form, """
    display: flex;
    width: 100%;
""")

Submit = Styler.stylize(Button, """
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 700;
    border-radius: 0 0.4rem 0.4rem 0;
    cursor: pointer;
    width: 12.8rem;
    height: 3.2rem;

    &.htmx-request {
        pointer-events: none;
    }

    @include color-scheme{
        background-color: color-scheme-get("primary");
        color: color-scheme-get("on-primary");
        transition: background-color 250ms;

        &.htmx-request {
            background-color: color-scheme-get("hover");
        }

        &:hover {
            background-color: color-scheme-get("primary-hover");
        }
    }
""")

SubmitText = Styler.stylize(Span, """
   .htmx-request &{
       display: none; 
   }
""")

TextField = Styler.stylize(Input, """
    @include color-scheme{
        border: 0.1rem solid color-scheme-get("border");
        background-color: color-scheme-get("background");
        color: color-scheme-get("on-background");
        border-right: none;

        &:focus {
            border: 0.1rem solid color-scheme-get("hover");
        }
    }

    width: 100%;
    height: 3.2rem;
    border-right: none;
    border-radius: 0.4rem 0 0 0.4rem;
    padding-left: 1.6rem;

    &:focus {
        border-right: none;
        outline: none;
    }

""")
# fmt: on
