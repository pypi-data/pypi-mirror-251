# coding=utf-8

from .escape2 import AnsiEscapeCodes

import getpass
import sys
import re
import os


class AnsiConsole(AnsiEscapeCodes):
    def __init__(self):
        self._encoding = 'utf-8'

    def getesc(self, style):
        styles = ""

        if isinstance(style, list):
            styles += "".join(style)
        elif isinstance(style, str):
            styles += style
        elif isinstance(style, bytes):
            styles += style.decode(self._encoding)

        return styles

    def append(self, style):
        esc = self.getesc(style=style).encode(self._encoding)
        return sys.stdout.write(esc)

    def reset(self, end=''):
        sys.stdout.write("{}{}".format(self.Styles.RESET, end))

    def printf(self, text, style=None, end='\n'):
        self.append(style)

        prompt = ""

        if isinstance(text, bytes):
            prompt += text.decode(self._encoding)

        elif isinstance(text, str):
            prompt += text

        else:
            prompt += str(text)

        write_result = sys.stdout.write("{}{}".format(prompt, end))
        self.reset()

        return write_result

    def grd_printf(self, text, color1, color2, end='\n'):
        ltext = ""

        if isinstance(text, bytes):
            ltext += text.decode(self._encoding)

        elif isinstance(text, str):
            ltext += text

        else:
            ltext += str(text)

        if isinstance(color1, tuple):
            start_color = color1

        elif color1.startswith("#"):
            start_color = tuple(
                int(color1[i:i + 2], 16)
                for i in range(1, len(color1), 2)
            )

        else:
            raise ValueError(
                "The parameter accepts only the color hex and the r,g,b"
            )

        if isinstance(color2, tuple):
            end_color = color2

        elif color2.startswith("#"):
            end_color = tuple(
                int(color2[i:i + 2], 16)
                for i in range(1, len(color2), 2)
            )

        else:
            raise ValueError(
                "The parameter accepts only the color hex and the r,g,b"
            )

        text_length = len(ltext)

        gradient_step = (
            float(end_color[0] - start_color[0]) / max(text_length - 1, 1),
            float(end_color[1] - start_color[1]) / max(text_length - 1, 1),
            float(end_color[2] - start_color[2]) / max(text_length - 1, 1)
        )

        for i, char in enumerate(ltext):
            current_color = (
                int(start_color[0] + i * gradient_step[0]),
                int(start_color[1] + i * gradient_step[1]),
                int(start_color[2] + i * gradient_step[2])
            )
            fore_color = self.Colors.Fore.from_rgb(*current_color)
            self.printf(char, style=fore_color, end='')

        self.reset(end=end)

    def _parse_ansi_escape(self, escape_code):
        match = re.match(r'\033\[38;2;(\d+);(\d+);(\d+)m', escape_code)
        if match:
            red, green, blue = map(int, match.groups())
            return red, green, blue

        else:
            raise ValueError("Invalid ANSI escape code format")

    def inputf(self, text, style=None, end=''):
        self.append(style)

        prompt = ""

        if isinstance(text, bytes):
            prompt += text.decode(self._encoding)

        elif isinstance(text, str):
            prompt += text

        else:
            raise TypeError(
                "This method takes only str and bytes"
            )

        self.printf(prompt, style=style, end=end)
        usr_input = raw_input()
        self.reset()
        return usr_input

    def passf(self, text, style=None, end=''):
        self.append(style)

        prompt = ""

        if isinstance(text, bytes):
            prompt += text.decode(self._encoding)

        elif isinstance(text, str):
            prompt += text

        else:
            raise TypeError(
                "This method takes only str and bytes"
            )

        self.printf(prompt, style=style, end=end)
        usr_input = getpass.getpass('')
        self.reset()
        return usr_input

    def formatf(self, text, style, end=''):
        return "{}{}{}{}".format(style, text, self.Styles.RESET, end)

    def clearf(self):
        if os.name == "posix":
            return os.system("clear")

        elif os.name == "nt":
            return os.system("cls")

        else:
            raise RuntimeError("Unsupported operating system")

    def titlef(self, title):
        ltitle = ""

        if not title:
            if os.name == 'nt':
                ctypes = __import__('ctypes')
                buf_size = 256 - 1
                buf = ctypes.create_unicode_buffer(buf_size)
                ctypes.windll.kernel32.GetConsoleTitleW(buf, buf_size)
                return buf.value

            elif os.name == 'posix':
                return os.getenv('TERM_PROGRAM', 'Unknown Terminal')

            else:
                raise RuntimeError("Unsupported operating system")

        if isinstance(title, bytes):
            ltitle = title.decode(self._encoding)

        elif isinstance(title, str):
            ltitle = title

        else:
            ltitle = str(title)

        write_result = sys.stdout.write("\033]0;{}\007".format(ltitle))
        sys.stdout.flush()
        return write_result
