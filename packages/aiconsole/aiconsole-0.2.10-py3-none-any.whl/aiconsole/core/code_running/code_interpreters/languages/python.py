#
# MIT License
#
# Copyright (c) 2023 Killian Lucas
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
#     ____                      ____      __                            __
#    / __ \____  ___  ____     /  _/___  / /____  _________  ________  / /____  _____
#   / / / / __ \/ _ \/ __ \    / // __ \/ __/ _ \/ ___/ __ \/ ___/ _ \/ __/ _ \/ ___/
#  / /_/ / /_/ /  __/ / / /  _/ // / / / /_/  __/ /  / /_/ / /  /  __/ /_/  __/ /
#  \____/ .___/\___/_/ /_/  /___/_/ /_/\__/\___/_/  / .___/_/   \___/\__/\___/_/
#      /_/                                         /_/
#
# This file has been taken from the wonderful project "open-interpreter" by Killian Lucas
# https://github.com/KillianLucas/open-interpreter
#

import ast
import logging
import re

from aiconsole.core.assets.materials.material import Material

from ..subprocess_code_interpreter import SubprocessCodeInterpreter

_log = logging.getLogger(__name__)


class Python(SubprocessCodeInterpreter):
    file_extension = "py"
    proper_name = "Python"

    def __init__(self):
        super().__init__()
        self.start_cmd = "python -i -q -u"

    def preprocess_code(self, code: str, materials: list[Material]):
        return preprocess_python(code, materials)

    def line_postprocessor(self, line):
        if re.match(r"^(\s*>>>\s*|\s*\.\.\.\s*)", line):
            return None
        return line

    def detect_end_of_execution(self, line):
        return "## end_of_execution ##" in line


def preprocess_python(code: str, materials: list[Material]):
    """
    Add active line markers
    Wrap in a try except
    Add end of execution marker
    """

    # If a line starts with "!" then it's a shell command, we need to wrap it appropriately
    code = "\n".join(
        [f"import os; os.system({line[1:]!r})" if line.startswith("!") else line for line in code.split("\n")]
    )

    # Check for syntax errors in user's code
    try:
        ast.parse(code)
    except SyntaxError as e:
        # If there's a syntax error, return the error message directly
        newline = "\n"
        # msg_for_user = f"SyntaxError on line {e.lineno}, column {e.offset}: {e.msg} ({e.text})"

        msg_for_user = (
            f""
            f'File "{e.filename}", line {e.lineno}, column {e.offset}\n '
            f"  {(e.text or '').replace(newline, '')}\n"
            f"  {(e.offset or 0) * ' '}^\n"
            f"SyntaxError: {e.msg}\n"
        )

        return f"print(f'''{msg_for_user}''')\nprint('## end_of_execution ##')"

    api_materials = [material for material in materials if material.content_type == "api"]
    apis = [material.inlined_content for material in api_materials]

    parsed_code = ast.parse("\n\n\n".join(apis))
    parsed_code.body = [b for b in parsed_code.body if not isinstance(b, ast.Expr) or not isinstance(b.value, ast.Str)]
    apis_str = ast.unparse(parsed_code)

    newline = "\n"
    api_lines = [line for line in apis_str.split(newline) if line.strip()]
    code_lines = [line for line in code.split(newline) if line.strip()]

    code = f"""
import traceback
from aiconsole_toolkit.credentials import MissingCredentialException
try:
{newline.join(("    " + line) for line in [*api_lines, *code_lines])}
except MissingCredentialException as e:
    print(e)
except Exception:
    traceback.print_exc()


print("## end_of_execution ##")

""".strip()

    return code
