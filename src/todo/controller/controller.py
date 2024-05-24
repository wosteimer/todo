from collections.abc import Awaitable, Callable

type Controller[T, R] = Callable[[T], Awaitable[R]]
