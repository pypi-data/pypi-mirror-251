from .ui_compiled.ValidationDialog import Ui_ValidationDialog
from PyQt6.QtCore import QCoreApplication
from PyQt6.QtWidgets import QDialog
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from .MainWindow import MainWindow


class ValidationDialog(Ui_ValidationDialog, QDialog):
    def __init__(self, main_window: "MainWindow") -> None:
        super().__init__()

        self.setupUi(self)

        self._main_window = main_window

    def open_dialog(self) -> None:
        try:
            self.output_box.setPlainText(str(self._main_window.get_desktop_entry().get_validation_messages()))
        except FileNotFoundError:
            self.output_box.setPlainText(QCoreApplication.translate("ValidationDialog", "desktop-file-validate was not found"))

        self.exec()
