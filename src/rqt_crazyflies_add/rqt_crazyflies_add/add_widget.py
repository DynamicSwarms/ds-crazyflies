from python_qt_binding.QtCore import QMargins, Signal, QTimer, QSize
from python_qt_binding.QtWidgets import (
    QWidget,
    QListWidget,
    QListWidgetItem,
    QHeaderView,
    QHBoxLayout,
    QSizePolicy,
)
from python_qt_binding.QtWidgets import QMessageBox

from rqt_crazyflies_add.saved_crazyflie import SavedCrazyflie

import os
from python_qt_binding import loadUi
from ament_index_python import get_resource

_, package_path = get_resource("packages", "rqt_crazyflies_add")
from rqt_crazyflies_add.add_api import AddApi


from qt_gui.settings import Settings
from python_qt_binding.QtWidgets import QFileDialog
import yaml


class AddWidget(QWidget):

    # To be connected to PluginContainerWidget
    sig_sysmsg = Signal(str)
    sig_sysprogress = Signal(str)

    # To make selections from CLA
    sig_selected = Signal(str, bool)

    def __init__(self, context):
        super(AddWidget, self).__init__()

        # Set window title
        self.setWindowTitle("Crazyflie Add")
        self.setObjectName("Crazyflie Add")

        self._add_api = AddApi(context.node)

        _hlayout_top = QHBoxLayout(self)

        # List Widget to hold status widgets
        self._add_widget = loadUi(
            os.path.join(
                package_path,
                "share",
                "rqt_crazyflies_add",
                "resource",
                "crazyflies_add.ui",
            ),
        )
        _hlayout_top.addWidget(self._add_widget)

        self.set_initial_position_visible(
            self._add_widget.comboBox.currentText() != "default"
        )
        self._add_widget.comboBox.currentTextChanged.connect(
            lambda text: self.set_initial_position_visible(text != "default")
        )

        self._add_widget.spinBox.valueChanged.connect(self.update_label_with_hex)
        self._add_widget.spinBox_2.valueChanged.connect(self.update_label_with_hex)

        self._add_widget.hardware_add_button.clicked.connect(self.on_hardware_add)
        self._add_widget.hardware_save_button.clicked.connect(self.on_hardware_save)

        self._add_widget.webots_add_button.clicked.connect(self.on_webots_add)
        self._add_widget.webots_save_button.clicked.connect(self.on_webots_save)

        self._add_widget.add_all_button.clicked.connect(self.on_add_all)
        self._add_widget.load_from_yaml_button.clicked.connect(self.on_load_from_yaml)
        self._add_widget.save_to_yaml_button.clicked.connect(self.on_save_to_yaml)

        self._saved_grid_pos = 0
        self._saved: list[SavedCrazyflie] = []
        self.GRID_SIZE = 4

    @property
    def _sorted_saved(self) -> list[SavedCrazyflie]:
        return sorted(self._saved, key=lambda cf: cf.id)

    ####### TABS Logic ###############

    def get_id(self):
        val1 = self._add_widget.spinBox.value()
        val2 = self._add_widget.spinBox_2.value()
        return val1 * 16 + val2

    def get_channel(self) -> int:
        return self._add_widget.spinBox_3.value()

    def get_xyz(self) -> list[float]:
        x = self._add_widget.x_spin_box.value()
        y = self._add_widget.y_spin_box.value()
        z = self._add_widget.z_spin_box.value()
        return [x, y, z]

    def update_label_with_hex(self):
        self._add_widget.label_2.setText(f"(int) {self.get_id()}")

    def set_initial_position_visible(self, visible: bool):
        for i in range(self._add_widget.horizontalLayout_3.count()):
            if self._add_widget.horizontalLayout_3.itemAt(i).widget():
                self._add_widget.horizontalLayout_3.itemAt(i).widget().setVisible(
                    visible
                )

    def on_hardware_add(self):
        self._add_api.add_hardware_crazyflie(
            id=self.get_id(),
            channel=self._add_widget.spinBox_3.value(),
            type=self._add_widget.comboBox.currentText(),
            initial_position=self.get_xyz(),
        )

    def on_webots_add(self):
        self._add_api.add_webots_crazyflie(id=self.get_id())

    ######### Save Logic #################

    def on_hardware_save(self):
        cf = SavedCrazyflie(
            self.get_id(),
            "hardware",
            self.get_channel(),
            self._add_widget.comboBox.currentText(),
            self.get_xyz(),
        )
        self._save(cf)

    def on_webots_save(self):
        cf = SavedCrazyflie(self.get_id(), "webots")
        self._save(cf)

    def on_save_delete(self, cf: SavedCrazyflie):
        self._saved.remove(cf)
        cf.setParent(None)
        self._rewrite_from_array()

    def on_save_add(self, cf: SavedCrazyflie):
        if cf.type == "hardware":
            self._add_api.add_hardware_crazyflie(
                id=cf.id,
                channel=cf.channel,
                type=cf.hw_type,
                initial_position=cf.initial_position,
            )
        else:
            self._add_api.add_webots_crazyflie(id=cf.id)

    def on_add_all(self):
        reply = QMessageBox.question(
            self,
            "Confirm Add All",
            "Are you sure you want to add all Crazyflies in the list?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if reply == QMessageBox.Yes:
            for cf in self._sorted_saved:
                self.on_save_add(cf)

    def on_load_from_yaml(self):
        options = QFileDialog.Options()
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Open Crazyflies YAML",
            "",
            "YAML Files (*.yaml *.yml);;All Files (*)",
            options=options,
        )
        if filename:
            with open(filename, "r") as f:
                data = yaml.safe_load(f)
                crazyflies = data.get("flies", [])
                self._saved.clear()
                for cf_dict in crazyflies:
                    self._save(SavedCrazyflie.from_yaml(cf_dict))
            self._rewrite_from_array()

    def on_save_to_yaml(self):
        options = QFileDialog.Options()
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Save Crazyflies YAML",
            "",
            "YAML Files (*.yaml *.yml);;All Files (*)",
            options=options,
        )
        if filename:
            data = {"flies": [cf.to_yaml() for cf in self._sorted_saved]}
            with open(filename, "w") as f:
                yaml.safe_dump(data, f)

    ############## Save Grid Internals ##############

    def _save(self, cf: SavedCrazyflie):
        cf._button_delete.clicked.connect(lambda: self.on_save_delete(cf))
        cf._button_add.clicked.connect(lambda: self.on_save_add(cf))
        self._saved.append(cf)
        self._rewrite_from_array()

    def _rewrite_from_array(self):
        while self._add_widget.save_grid.count():
            item = self._add_widget.save_grid.takeAt(0)
            widget = item.widget()
            if widget:
                widget.setParent(None)
        self._saved_grid_pos = 0
        for cf in self._sorted_saved:
            self._add_widget.save_grid.addWidget(
                cf,
                self._saved_grid_pos // self.GRID_SIZE,
                self._saved_grid_pos % self.GRID_SIZE,
            )
            self._saved_grid_pos += 1

        # Fill up the row to GRID_SIZE with empty QWidget placeholders
        if (self._saved_grid_pos % self.GRID_SIZE) != 0:
            remaining = self.GRID_SIZE - (self._saved_grid_pos % self.GRID_SIZE)
            for _ in range(remaining):
                placeholder = QWidget()
                if self._saved:
                    placeholder.setSizePolicy(self._saved[0].sizePolicy())
                    placeholder.setMinimumSize(self._saved[0].minimumSizeHint())
                    placeholder.setMaximumSize(self._saved[0].maximumSize())
                    placeholder.setFixedSize(self._saved[0].sizeHint())
                self._add_widget.save_grid.addWidget(
                    placeholder,
                    self._saved_grid_pos // self.GRID_SIZE,
                    (self._saved_grid_pos % self.GRID_SIZE) + _,
                )

    def shutdown(self):
        pass

    def save_settings(self, plugin_settings: Settings, instance_settings: Settings):
        # Save the list of SavedCrazyflie objects
        saved_data = []
        for cf in self._sorted_saved:
            saved_data.append(cf.to_dict())
        plugin_settings.set_value("saved_crazyflies", saved_data)

    def restore_settings(self, plugin_settings: Settings, instance_settings: Settings):
        # Restore the list of SavedCrazyflie objects
        saved_data = plugin_settings.value("saved_crazyflies", [])
        self._saved.clear()
        if saved_data is not None:
            for cf_dict in saved_data:
                self._save(SavedCrazyflie.from_dict(cf_dict))
