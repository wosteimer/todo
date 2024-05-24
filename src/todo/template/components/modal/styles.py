from builder.styler import Styler
from builder.tags import Div

# fmt: off
Background = Styler.stylize(Div, """
    position: absolute;
    display: flex;
    flex-direction: column-reverse;
    background-color: rgba(0, 0, 0, 0.0);
    border-radius: 0.8rem;
    width: 100%;
    height: 100%;
    visibility: hidden;
    transition: background-color 0.25s linear, visibility 0.25s linear;

    &.hide{
        visibility: hidden;
        background-color: rgba(0, 0, 0, 0.0);
    }

    &.show,
    &.htmx-request{
        visibility: visible;
        background-color: rgba(0, 0, 0, 0.6);
    }
""")

Container = Styler.stylize(Div, """
    height: 12.8rem;
    margin: 0 0.8rem 0 0.8rem;
    display: flex;
    justify-content: center;
    padding: 2.4rem 1.6em 0 1.6rem;
    border-radius: 1.6rem 1.6rem 0 0;
    transform: translateY(12.8rem);

    @include color-scheme{
        background-color: color-scheme-get("secondary-background");
        border: 0.1rem solid color-scheme-get("border");
    }

    .show &{
        transform: translateY(0);
    }

    .hide &{
        animation: modal-hide 0.25s ease-in-out;
        transform: translateY(12.8rem);
    }
    
    .htmx-added &{
        animation: modal-show 0.25s ease-in-out;
    }
""")
# fmt: on
