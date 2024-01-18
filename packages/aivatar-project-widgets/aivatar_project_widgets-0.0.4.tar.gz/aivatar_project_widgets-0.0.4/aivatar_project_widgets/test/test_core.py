"""Core Test."""

# Import future modules
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

# Import built-in modules

# Import third-party modules
import pytest

# Import local modules
from aivatar_project_widgets import AivProjectWindow


class TestAivProjectWindow:
    @pytest.fixture(autouse=True)
    def setup(self, mocker, qtbot):
        self.widget = AivProjectWindow()
        qtbot.addWidget(self.widget)

    # def test_show_widget(self):
    #     assert self.widget.pushButton_test.text() == "test"
