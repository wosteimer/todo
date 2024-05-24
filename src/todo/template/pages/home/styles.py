from builder.styler import Styler
from builder.tags import Div
from builder.tags import Footer as FooterTag
from builder.tags import Header as HeaderTag
from builder.tags import Main as MainTag

# fmt: off
Container = Styler.stylize(Div,
    """
    overflow: hidden;
    display: flex;
    position: absolute;
    flex-direction: column;
    max-width: 32rem;
    height: 72rem;
    border-radius: 0.8rem;

    @include color-scheme{
        background-color: color-scheme-get("secondary-background");
        color: color-scheme-get("on-background");
        border: 0.1rem solid color-scheme-get("border");
    }

    @media (max-height: 720px) {
        height: 100%;
        border-radius: 0;
        border-top: none;
        border-bottom: none;
    }

    @media (max-width: 320px) {
        border-radius: 0;
        border-left: none;
        border-right: none;

    }
""")

Header = Styler.stylize(HeaderTag, """
    padding: 1.6rem 1.2rem;
    @include color-scheme{
        border-bottom: 0.1rem solid color-scheme-get("border");
    }
""")

Main = Styler.stylize(MainTag, """
    height: 100%;
    padding-top: 0.8rem;
    overflow-y: scroll;
    overflow-x: hidden;
""")

Footer = Styler.stylize(FooterTag, """
    font-size: 1.2rem;
    align-items: center;
    height: 5.6rem;
    display: flex;
    justify-content: center;
    align-items: center;
    opacity: 0.8;

    & .fa-heart {
        padding: 0 0.4rem;

    }

    & a{
        padding-left: 0.4rem;
    }

    @include color-scheme{
        color: color-scheme-get("on-backgroud");
        border-top: 0.1rem solid color-scheme-get("border");

        & .fa-heart {
            color: color-scheme-get("red");

        }

        & a{
            color: color-scheme-get("primary");
        }
    }
""")
# fmt: on
