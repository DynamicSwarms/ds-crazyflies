from python_qt_binding.QtWidgets import QPushButton, QLabel, QWidget
from python_qt_binding.QtWidgets import QVBoxLayout, QHBoxLayout
from python_qt_binding.QtCore import Qt


class SavedCrazyflie(QWidget):
    def __init__(
        self,
        id: int,
        type: str,
        channel: int = None,
        hw_type: str = None,
        initial_position: list[float] = None,
    ):
        super(SavedCrazyflie, self).__init__()
        self.id = id
        self.type = type
        self.channel = channel
        self.hw_type = hw_type
        self.initial_position = initial_position

        name_str = f"HW {id:02X}" if type == "hardware" else f"WB {id:02X}"
        if type == "hardware":
            name_str += f"\nCh:{channel}|"
            name_str += "t" if hw_type == "tracked" else "d"
            if hw_type == "tracked":
                pos_str = ",".join([f"{p:.1f}" for p in initial_position])
                name_str += f"\nPos:[{pos_str}]"

        self._label = QLabel(name_str)
        self._label.setToolTip(name_str)
        self._button_delete = QPushButton("")
        self._button_delete.setIcon(
            self.style().standardIcon(self.style().SP_TrashIcon)
        )
        self._button_add = QPushButton("Add")

        layout = QVBoxLayout()
        layout.addWidget(self._label)

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self._button_add)
        btn_layout.addWidget(self._button_delete)
        layout.addLayout(btn_layout)
        self.setLayout(layout)

        palette = self.palette()
        palette.setColor(self.backgroundRole(), Qt.white)
        self.setPalette(palette)
        self.setAutoFillBackground(True)

    def to_dict(self):
        return {
            "id": self.id,
            "type": self.type,
            "channel": self.channel,
            "hw_type": self.hw_type,
            "initial_position": self.initial_position,
        }

    def to_yaml(self):
        return {
            "id": self.id,
            "channel": self.channel,
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data.get("id"),
            type=data.get("type"),
            channel=data.get("channel"),
            hw_type=data.get("hw_type"),
            initial_position=data.get("initial_position"),
        )

    @classmethod
    def from_yaml(cls, data: dict):
        return cls(
            id=data.get("id"),
            type="hardware",
            channel=data.get("channel"),
            hw_type="default",
        )
