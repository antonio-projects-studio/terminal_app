import asyncio
from terminal_app.decorator import safety_call, set_params


@safety_call
async def func(a, b, c=3) -> None:
    await asyncio.sleep(2)
    print(a, b, c)


async def func2(a, b, c) -> None:
    print(a, b, c)


@safety_call
@set_params(kwargs=dict(a=3))
def func3(a, c) -> None:
    print(a, c)


class A:
    @staticmethod
    def f(a, b, /, c):
        print(a)


async def main(**kwargs) -> None:
    await func(a=3, b=4, m=5)
    await safety_call(func2, kwargs)
    func3(**kwargs)


asyncio.run(main(a=6, b=7, c=8))
