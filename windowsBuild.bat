set version=%1
set outputfile=\WindowsBuildOutput.txt

ECHO "Building LINDO API For Windows\n\n\n".>"WindowsBuildOutput.txt"

py -3.7 -m venv \myenv37
CALL \myenv37\Scripts\activate.bat
ECHO "Python 3.7\n".>"WindowsBuildOutput.txt"
pip install build
py -m build
pip install dist\lindo-%version%-cp37-cp37m-win_amd64.whl
py -m lindo_test >>"WindowsBuildOutput.txt"
py samples\lp.py >>"WindowsBuildOutput.txt"
CALL \myenv37\Scripts\deactivate.bat

py -3.8 -m venv \myenv38
CALL \myenv38\Scripts\activate.bat
ECHO "Python 3.8\n".>"WindowsBuildOutput.txt"
pip install build
py -m build
pip install dist\lindo-%version%-cp38-cp38-win_amd64.whl
py -m lindo_test >>"WindowsBuildOutput.txt"
py samples\lp.py >>"WindowsBuildOutput.txt"
CALL \myenv38\Scripts\deactivate.bat

py -3.9 -m venv \myenv39
CALL \myenv39\Scripts\activate.bat
ECHO "Python 3.9\n".>"WindowsBuildOutput.txt"
pip install build
py -m build
pip install dist\lindo-%version%-cp39-cp39-win_amd64.whl
py -m lindo_test >>"WindowsBuildOutput.txt"
py samples\lp.py >>"WindowsBuildOutput.txt"
CALL \myenv39\Scripts\deactivate.bat

py -3.10 -m venv \myenv310
CALL \myenv310\Scripts\activate.bat
ECHO "Python 3.10\n".>"WindowsBuildOutput.txt"
pip install build
py -m build
pip install dist\lindo-%version%-cp310-cp310-win_amd64.whl
py -m lindo_test >>"WindowsBuildOutput.txt"
py samples\lp.py >>"WindowsBuildOutput.txt"
CALL \myenv310\Scripts\deactivate.bat