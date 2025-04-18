from langchain.agents import tool
from langchain_experimental.utilities import PythonREPL
from typing import Annotated


repl = PythonREPL()


@tool
def execute_python(
	code: Annotated[str, 'The python code to execute to generate your chart.'],
):
	"""Use this to execute python code. If you want to see the output of a value, you should print it out with `print(...)`. This is visible to the user."""
	try:
		result = repl.run(code)
	except BaseException as e:
		return f'Failed to execute. Error: {repr(e)}'
	return f'Succesfully executed:\n`python\n{code}\n`\nStdout: {result}'
