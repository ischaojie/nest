import pytest
from click.testing import CliRunner
from nest import wea_cli


class TestWeather:

    @pytest.fixture(autouse=True)
    def setup(self):
        self.runner = CliRunner()

    # def test_wea_cli_default(self):
    #     result = self.runner.invoke(wea_cli, ['beijing'])
    #     assert result.exit_code == 0
    #     assert 'beijing' in result.output
    