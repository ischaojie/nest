import pytest
from click.testing import CliRunner
from nest import trans_cli


class TestTranslate:

    @pytest.fixture(autouse=True)
    def setup(self):
        self.runner = CliRunner()

    def test_trans_cli(self):
        result = self.runner.invoke(trans_cli, ['hello'])
        assert result.exit_code == 0
        assert '你好' in result.output
    
    def test_trans_cli_engine(self):
        result = self.runner.invoke(trans_cli, ['hello', '--engine=youdao'])
        assert 'youdao' in result.output

    def test_trans_cli_source_and_to(self):
        pass
