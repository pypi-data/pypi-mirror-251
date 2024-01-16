from .escape3 import AnsiEscapeCodes
import getpass
import sys
import re
import os
from typing import Union, Tuple, List


class AnsiConsole(AnsiEscapeCodes):
    def __init__(self) -> None:
        self._encoding: str = 'utf-8'

    def getesc(self, style: Union[List[str], str, bytes]):
        styles: str = ""

        if isinstance(style, list):
            styles += "".join(style)
        elif isinstance(style, bytes):
            styles += style.decode(self._encoding)
        elif isinstance(style, str):
            styles += style

        return styles

    def append(self, style: Union[List[str], str, bytes]):
        esc = self.getesc(style=style)
        return sys.stdout.write(esc)

    def reset(self, end: str = '') -> None:
        sys.stdout.write(f"{self.Styles.RESET}{end}")

    def printf(
        self,
        text: Union[str, bytes],
        style: Union[List[str], str, bytes] = None,
        end: str = '\n'
    ) -> Tuple[int, int]:

        self.append(style)
        prompt: str = ""
        if isinstance(text, bytes):
            prompt += text.decode(self._encoding)
        elif isinstance(text, str):
            prompt += text
        else:
            prompt += str(text)
        write_result: int = sys.stdout.write(f"{prompt}{end}")
        reset_result: int = self.reset()
        return write_result, reset_result

    def grd_printf(
        self,
        text: str,
        color1: Union[Tuple[int, int, int], str],
        color2: Union[Tuple[int, int, int], str],
        end: str = '\n'
    ) -> None:

        ltext: str = ""
        if isinstance(text, bytes):
            ltext += text.decode(self._encoding)
        elif isinstance(text, str):
            ltext += text
        else:
            ltext += str(text)

        if isinstance(color1, tuple):
            start_color = color1
        elif color1.startswith("#"):
            start_color = tuple(int(color1[i:i + 2], 16) for i in (1, 3, 5))
        else:
            raise TypeError(
                "This method takes only str and bytes"
            )

        if isinstance(color2, tuple):
            end_color = color2
        elif color2.startswith("#"):
            end_color = tuple(int(color2[i:i + 2], 16) for i in (1, 3, 5))
        else:
            raise TypeError(
                "This method takes only str and bytes"
            )

        text_length = len(ltext)

        gradient_step = (
            (end_color[0] - start_color[0]) / max(text_length - 1, 1),
            (end_color[1] - start_color[1]) / max(text_length - 1, 1),
            (end_color[2] - start_color[2]) / max(text_length - 1, 1)
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

    def _parse_ansi_escape(
        self,
        escape_code: Union[str, bytes]
    ) -> Tuple[int, int, int]:

        match = re.match(r'\033\[38;2;(\d+);(\d+);(\d+)m', escape_code)
        if match:
            red, green, blue = map(int, match.groups())
            return red, green, blue
        else:
            raise ValueError("Invalid ANSI escape code format")

    def inputf(
        self,
        text: Union[str, bytes],
        style: Union[List[str], str, bytes] = None,
        end: str = ''
    ) -> str:

        self.append(style)
        prompt: str = ""
        if isinstance(text, bytes):
            prompt += text.decode(self._encoding)
        elif isinstance(text, str):
            prompt += text
        else:
            raise TypeError(
                "This method takes only str and bytes"
            )

        self.printf(prompt, style=style, end=end)
        usr_input = input()
        self.reset()
        return usr_input

    def passf(
        self,
        text: Union[str, bytes],
        style: Union[List[str], str, bytes] = None,
        end: str = ''
    ) -> str:

        self.append(style)
        prompt: str = ""
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

    def formatf(
        self,
        text: Union[str, bytes],
        style: Union[List[str], str, bytes],
        end: str = ''
    ) -> str:

        return f"{style}{text}{self.Styles.RESET}{end}"

    def clearf(self) -> int:
        if os.name == "posix":
            return os.system("clear")
        elif os.name == "nt":
            return os.system("cls")
        else:
            raise RuntimeError("Unsupported operating system")

    def titlef(self, title: Union[bytes, str]) -> int:
        ltitle: str = ""
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

        write_result = sys.stdout.write(f"\033]0;{ltitle}\007")
        sys.stdout.flush()
        return write_result
