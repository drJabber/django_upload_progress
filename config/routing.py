from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter, ChannelNameRouter
import progrock.routing
import progress_worker.routing

application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': AuthMiddlewareStack(
        URLRouter(
            progrock.routing.public_routing
        )
    ),

    'channel': ChannelNameRouter(
        progress_worker.routing.internal_routing
    ),
})

