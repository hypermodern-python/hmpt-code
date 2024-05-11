def _send(objects, sender):
    """send them with the sender..."""
    for obj in objects[0].get_all():
        if p := obj.get_parent():
            sender.run(p)
        elif obj is not None and obj._next is not None:
            _send_next_object(obj._next, sender)
