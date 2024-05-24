from builder.styler import Styler
from builder.tags import Button, Div, I, Li

# fmt: off
Container = Styler.stylize(Li, """
    font-size: 1.2rem;
    position: relative;
    width: 100%;
    height: 3.2rem;
    display: flex;
    align-items: center;
    user-select: none;
    padding: 0 2rem;
    
    &:hover{
        font-weight: 700;
        @include color-scheme{
            color: color-scheme-get("on-primary");
            background-color: color-scheme-get("hover");
        }
    }
    & del{
        opacity: 0.4;
    }

    &.htmx-added{
        animation: slide-in 0.5s forwards;
    }

    &.htmx-swapping:not(.htmx-added) {
        animation: delete-todo 0.5s ease-out;
    }

    &.htmx-swapping:not(.htmx-added)~& {
        animation: up-todos 0.5s ease-out;
    }
""")

Left = Styler.stylize(Div, """
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
""")

Right = Styler.stylize(Button, """
    width: 3.2rem;
    height: 100%;
    background: none;
    opacity: 0.6;
    border-radius: 0.4rem;

    @include color-scheme{
        color: color-scheme-get("on-background");
        &:hover{
            border: 0.1rem solid color-scheme-get("border");
        }
    }

    &:hover{
        opacity: 1;
    }
""")

Checked = Styler.stylize(I, """
    margin-right: 1.6rem;
    color: var(--on-backgroud);
    font-size: 1.4rem;
    @include color-scheme{
        color: color-scheme-get("green");
    }
""")

NoChecked = Styler.stylize(I, """
    margin-right: 1.6rem;
    font-size: 1.4rem;
    @include color-scheme{
        color: color-scheme-get("on-backgroud");
    }
""")

Skeleton = Styler.stylize(Div, """
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: space-between;
    visibility: hidden;

    @include color-scheme{
        background-color: color-scheme-get("skeleton-background");
    }

    .htmx-swapping:not(.htmx-added) &,
    &.htmx-request{
        visibility: visible;
    }

    &>div:first-child{
        width: 100%;
        display: flex;
        align-items: center;
    }
""")                        

FakeCheckBox = Styler.stylize(Div, """
    position: relative;
    width: 1.2rem;
    height: 1.2rem;
    margin: 0 1.6rem 0 2rem;
    border-radius: 0.2rem;

    @include skeleton-shine;

    @include color-scheme{
        background-color: color-scheme-get("skeleton-foreground");
    }
""")

FakeContent = Styler.stylize(Div, """
    position: relative;
    width: 45%;
    height: 1rem;
    border-radius: 0.2rem;

    @include skeleton-shine;

    @include color-scheme{
        background-color: color-scheme-get("skeleton-foreground");
    }
""")

FakeButton = Styler.stylize(Div, """
    position: relative;
    width: 1.6rem;
    height: 1.6rem;
    border-radius: 0.2rem;
    margin-right: 2.6rem;

    @include skeleton-shine;

    @include color-scheme{
        background-color: color-scheme-get("skeleton-foreground");
    }
""")
# fmt: on
