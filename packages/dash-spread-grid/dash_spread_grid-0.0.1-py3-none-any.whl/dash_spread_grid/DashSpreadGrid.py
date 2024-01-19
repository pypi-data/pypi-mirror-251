# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class DashSpreadGrid(Component):
    """A DashSpreadGrid component.


Keyword arguments:

- id (string; optional)

- columns (list; optional)

- data (list; optional)

- formatting (list; optional)

- pinnedBottom (number; default 0)

- pinnedLeft (number; default 0)

- pinnedRight (number; default 0)

- pinnedTop (number; default 0)

- rows (list; optional)"""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dash_spread_grid'
    _type = 'DashSpreadGrid'
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, data=Component.UNDEFINED, columns=Component.UNDEFINED, rows=Component.UNDEFINED, formatting=Component.UNDEFINED, pinnedTop=Component.UNDEFINED, pinnedBottom=Component.UNDEFINED, pinnedLeft=Component.UNDEFINED, pinnedRight=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'columns', 'data', 'formatting', 'pinnedBottom', 'pinnedLeft', 'pinnedRight', 'pinnedTop', 'rows']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'columns', 'data', 'formatting', 'pinnedBottom', 'pinnedLeft', 'pinnedRight', 'pinnedTop', 'rows']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        super(DashSpreadGrid, self).__init__(**args)
