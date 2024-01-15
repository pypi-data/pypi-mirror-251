# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Chat(Component):
    """A Chat component.
Component to serve as Loader for Graphs

Keyword arguments:

- id (string; required):
    Unique ID to identify this component in Dash callbacks.

- messages (list of boolean | number | string | dict | lists; optional):
    default messages.

- title (boolean | number | string | dict | list; default 'Dashpool Chat AI'):
    title of the chat.

- url (string; required):
    url to load the data."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dashpool_components'
    _type = 'Chat'
    @_explicitize_args
    def __init__(self, id=Component.REQUIRED, url=Component.REQUIRED, messages=Component.UNDEFINED, title=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'messages', 'title', 'url']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'messages', 'title', 'url']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        for k in ['id', 'url']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')

        super(Chat, self).__init__(**args)
