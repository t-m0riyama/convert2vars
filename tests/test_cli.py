import click
import pathlib
import re
import sys

from click.testing import CliRunner

base_path = (pathlib.Path(__file__)).parent.parent
sys.path.append(str(base_path) + '/bin')
#sys.path.append(str(base_path) + '/lib')
sys.path.append(str(base_path))
# from convert2vars import cli, convert
from convert2vars import *

runner = CliRunner()

def test_usage():
    result = runner.invoke(cli, ['--help'])
    assert result.exit_code == 0
    assert 'Usage: cli' in result.output

def test_convert_usage():
    result = runner.invoke(convert, ['--help'])
    assert result.exit_code == 0
    assert 'Usage: convert' in result.output

def test_convert_parameter():
    runner = CliRunner()
    result = runner.invoke(convert, ['-i', 'tests/parameters/test01.ini', '-t' 'tests/templates/template01.yml'], catch_exceptions=False)
    #result = runner.invoke(cli, ['-c', '/config/convert2vars.yml'], catch_exceptions=False)
    
    # result = runner.invoke(convert, ['-i', 'tests/parameters/test01.ini'])
    # assert result.exit_code == 0
    # assert result.output == 'HOGE'
    # assert re.match(r".*varString: XYZ.*", result.output) is not None
    # assert re.match(r".*varNumber: 123.*", result.output) is not None
    print(result)
    assert 'varString: XYZ' in result.output
    assert 'varNumber: 123' in result.output

# test_convert_parameter()
