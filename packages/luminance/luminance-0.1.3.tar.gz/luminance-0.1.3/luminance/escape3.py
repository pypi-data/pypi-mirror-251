import re


class AnsiEscapeCodes:
    CSI = '\033['
    OSC = '\033]'
    BEL = '\a'

    class Colors:
        class Back:
            BLACK = '\033[40m'
            RED = '\033[41m'
            GREEN = '\033[42m'
            YELLOW = '\033[43m'
            BLUE = '\033[44m'
            PURPLE = '\033[45m'
            CYAN = '\033[46m'
            WHITE = '\033[107m'
            ORANGE = '\033[48;5;208m'
            MAGENTA = '\033[48;5;5m'
            GRAY = '\033[48;5;244m'

            DARK_RED = '\033[48;2;139;0;0m'
            DARK_GREEN = '\033[48;2;0;100;0m'
            DARK_YELLOW = '\033[48;2;139;139;0m'
            DARK_BLUE = '\033[48;2;0;0;139m'
            DARK_PURPLE = '\033[48;2;139;0;139m'
            DARK_CYAN = '\033[48;2;0;139;139m'
            DARK_GRAY = '\033[100m'

            ULTRA_LIGHT_RED = '\033[48;2;255;0;0m'
            ULTRA_LIGHT_GREEN = '\033[48;2;0;255;0m'
            ULTRA_LIGHT_YELLOW = '\033[48;2;255;255;0m'
            ULTRA_LIGHT_BLUE = '\033[48;2;0;0;255m'
            ULTRA_LIGHT_PURPLE = '\033[48;2;255;0;255m'
            ULTRA_LIGHT_CYAN = '\033[48;2;0;255;255m'

            LIGHT_RED = '\033[101m'
            LIGHT_GREEN = '\033[102m'
            LIGHT_YELLOW = '\033[103m'
            LIGHT_BLUE = '\033[104m'
            LIGHT_PURPLE = '\033[105m'
            LIGHT_CYAN = '\033[106m'
            LIGHT_GRAY = '\033[48;2;169;169;169m'
            LIGHT_ORANGE = '\033[48;5;202m'

            @classmethod
            def from_rgb(cls, red, green, blue):
                return f'\033[48;2;{red};{green};{blue}m'

            @classmethod
            def from_hex(cls, hex_color):
                if not re.match(r'^#(?:[0-9a-fA-F]{3}){1,2}$', hex_color):
                    raise ValueError("Invalid hex color format")

                hex_color = hex_color.lstrip('#')
                rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

                return cls.from_rgb(*rgb)

            @classmethod
            def from_name(cls, color_name):
                color_name = color_name.upper()

                if color_name not in AnsiEscapeCodes.Colors.Back.__dict__:
                    raise ValueError(
                        f"Unknown color name: {color_name}"
                    )

                return getattr(cls, color_name)

            @classmethod
            def from_cmyk(cls, cyan, magenta, yellow, key):
                red = int((1 - min(1, cyan / 100.0) * (
                    1 - key / 100.0
                )) * 255)

                green = int((1 - min(1, magenta / 100.0) * (
                    1 - key / 100.0
                )) * 255)

                blue = int((1 - min(1, yellow / 100.0) * (
                    1 - key / 100.0
                )) * 255)

                return f'\033[48;2;{red};{green};{blue}m'

        class Fore:
            BLACK = '\033[30m'
            RED = '\033[31m'
            GREEN = '\033[32m'
            YELLOW = '\033[33m'
            BLUE = '\033[34m'
            PURPLE = '\033[35m'
            CYAN = '\033[36m'
            GRAY = '\033[37m'
            WHITE = '\033[97m'
            ORANGE = '\033[38;5;208m'
            MAGENTA = '\033[38;5;5m'

            LIGHT_MAGENTA = '\033[38;5;13m'
            LIGHT_RED = '\033[91m'
            LIGHT_GREEN = '\033[92m'
            LIGHT_YELLOW = '\033[93m'
            LIGHT_BLUE = '\033[94m'
            LIGHT_PURPLE = '\033[95m'
            LIGHT_CYAN = '\033[96m'
            LIGHT_GRAY = '\033[90m'
            LIGHT_ORANGE = '\033[38;5;202m'

            ULTRA_LIGHT_RED = '\033[38;2;255;200;200m'
            ULTRA_LIGHT_GREEN = '\033[38;2;200;255;200m'
            ULTRA_LIGHT_YELLOW = '\033[38;2;255;255;200m'
            ULTRA_LIGHT_BLUE = '\033[38;2;200;200;255m'
            ULTRA_LIGHT_PURPLE = '\033[38;2;255;200;255m'
            ULTRA_LIGHT_CYAN = '\033[38;2;200;255;255m'

            DARK_RED = '\033[38;2;139;0;0m'
            DARK_GREEN = '\033[38;2;0;100;0m'
            DARK_YELLOW = '\033[38;2;139;139;0m'
            DARK_BLUE = '\033[38;2;0;0;139m'
            DARK_PURPLE = '\033[38;2;139;0;139m'
            DARK_CYAN = '\033[38;2;0;139;139m'
            DARK_GRAY = '\033[38;2;169;169;169m'

            @classmethod
            def from_rgb(cls, red, green, blue):
                return f'\033[38;2;{red};{green};{blue}m'

            @classmethod
            def from_hex(cls, hex_color):
                if not re.match(r'^#(?:[0-9a-fA-F]{3}){1,2}$', hex_color):
                    raise ValueError("Invalid hex color format")

                hex_color = hex_color.lstrip('#')
                rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

                return cls.from_rgb(*rgb)

            @classmethod
            def from_name(cls, color_name):
                color_name = color_name.upper()

                if color_name not in AnsiEscapeCodes.Colors.Fore.__dict__:
                    raise ValueError(f"Unknown color name: {color_name}")

                return getattr(cls, color_name)

            @classmethod
            def from_cmyk(cls, cyan, magenta, yellow, key):
                red = int((1 - min(1, cyan / 100.0) * (
                    1 - key / 100.0
                )) * 255)

                green = int((1 - min(1, magenta / 100.0) * (
                    1 - key / 100.0
                )) * 255)

                blue = int((1 - min(1, yellow / 100.0) * (
                    1 - key / 100.0
                )) * 255)

                return f'\033[38;2;{red};{green};{blue}m'

    class Styles:
        RESET = '\033[0m'
        BOLD = '\033[1m'
        DIM = '\033[2m'
        UNDERLINE = '\033[4m'
        BLINK = '\033[5m'
        REVERSE = '\033[7m'
        HIDDEN = '\033[8m'
        STRIKETHROUGH = '\033[9m'
        MAGICAL = '\033[6m'
        SLOW_BLINK = '\033[25m'
        FAST_BLINK = '\033[6m'
        ITALIC = '\033[3m'
        OVERLINE = '\033[53m'
        DOUBLE_UNDERLINE = '\033[21m'
        FRAMED = '\033[51m'
        ENCIRCLED = '\033[52m'
        OVERLINED = '\033[55m'
        BOLD_FAINT = '\033[20m'
        POSITIVE_IMG = '\033[27m'

    class Cursor:
        UP = '\033[A'
        DOWN = '\033[B'
        FORWARD = '\033[C'
        BACKWARD = '\033[D'
        POS = '\033[H'
        CLEAR = '\033[2J'
        CLEAR_FORWARD = '\033[0J'
        CLEAR_BACKWARD = '\033[1J'
        CLEAR_LINE = '\033[2K'
        CLEAR_LINE_FORWARD = '\033[0K'
        CLEAR_LINE_BACKWARD = '\033[1K'
        SAVE_POS = '\033[s'
        RESTORE_POS = '\033[u'
