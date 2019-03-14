from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter, ChannelNameRouter
import progress.routing
import progress_worker.routing

# from channels.routing import include

# channel_routing = [
#     include('progress.routing.public_routing', path=r'^/prog/'),
#     include('progress.routing.internal_routing')
# ]

application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': AuthMiddlewareStack(
        URLRouter(
            progress.routing.public_routing
        )
    ),

    'channel': ChannelNameRouter(
        progress_worker.routing.internal_routing
    ),
})

