class Theme:
    _theme = ''

    light_color = '#242424'
    dark_color = '#fff'

    light_bgcolor = '#fff'
    dark_bgcolor = '#292929'

    light_border = '#d1d1d1'
    dark_order = '#666666'

    light_hover_bgcolor = '#f5f5f5'
    dark_hover_bgcolor = '#3d3d3d'

    light_hover_order = '#c7c7c7'
    dark_hover_order = '#757575'

    light_pressed_order = '#b3b3b3'
    dark_pressed_order = '#6b6b6b'

    light_disabled_order = '#e0e0e0'
    dark_disabled_order = '#424242'

    @classmethod
    def color(cls) -> str:
        return cls.light_color if cls.is_light() else cls.dark_color

    @classmethod
    def bgcolor(cls) -> str:
        return cls.light_bgcolor if cls.is_light() else cls.dark_bgcolor

    @classmethod
    def order(cls) -> str:
        return cls.light_border if cls.is_light() else cls.dark_order

    @classmethod
    def hover_bgcolor(cls) -> str:
        return cls.light_hover_bgcolor if cls.is_light() else cls.dark_hover_bgcolor

    @classmethod
    def hover_order(cls) -> str:
        return cls.light_hover_order if cls.is_light() else cls.dark_hover_order

    @classmethod
    def pressed_pressed(cls) -> str:
        return cls.light_pressed_order if cls.is_light() else cls.dark_pressed_order

    @classmethod
    def disabled_order(cls) -> str:
        return cls.light_disabled_order if cls.is_light() else cls.dark_disabled_order

    @classmethod
    def is_dark(cls) -> bool:
        return cls._theme == 'dark'

    @classmethod
    def is_light(cls) -> bool:
        return not cls.is_dark()
