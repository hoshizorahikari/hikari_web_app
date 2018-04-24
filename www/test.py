import orm
from models import User
import asyncio


async def test(loop):
    await orm.create_pool(loop, user='root', password='mysql', db='myblog')
    u1 = User(name='hikari', email='hikari@example.com', pwd='1234', image='hikari.jpg',admin=True)
    u2 = User(name='maki', email='maki@example.com', pwd='makimakima', image='about:blank')
    u3 = User(name='rin', email='rin@example.com', pwd='nyannyannyan', image='about:blank')
    # u.name = 'hikari'
    # u.email = 'hikari@example.com'
    # u.pwd = '1234'
    # u.image = 'about:blank'
    await u1.save()
    await u2.save()
    await u3.save()

    await orm.destroy_pool()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test(loop))
    loop.close()
