from . import consumers


internal_routing={
    'progress-worker': consumers.BackgroundTaskConsumer,
}

