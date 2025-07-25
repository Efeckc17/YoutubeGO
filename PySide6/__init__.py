
# PySide6 stub module for headless environments without Qt libraries.
# Provides minimal subset of Qt classes / enums used in the project's tests.

import types
import sys
from threading import Thread

# Helper Signal implementation -------------------------------------------------
class _SignalInstance:
    def __init__(self):
        self._slots = []

    def connect(self, slot):
        if callable(slot):
            self._slots.append(slot)

    def emit(self, *args, **kwargs):
        # Copy the list to allow slots to disconnect during emission safely
        for slot in list(self._slots):
            slot(*args, **kwargs)

class Signal:
    """Mimic PySide6.QtCore.Signal with a very small feature-set."""
    def __init__(self, *arg_types):
        self.arg_types = arg_types
        # An id is needed to differentiate between Signal descriptors inside a class
        self._id = id(self)

    def __get__(self, instance, owner):
        if instance is None:
            return self
        cache = instance.__dict__.setdefault("_qt_signals", {})
        if self._id not in cache:
            cache[self._id] = _SignalInstance()
        return cache[self._id]

# QtCore -----------------------------------------------------------------------
QtCore = types.ModuleType("PySide6.QtCore")

# Basic enum container
class _QtEnum(int):
    def __or__(self, other):
        return _QtEnum(int(self) | int(other))

    __and__ = __or__

class Qt(_QtEnum):
    KeepAspectRatio = 0x01
    SmoothTransformation = 0x02
    transparent = 0x04
    white = 0x08
    NoPen = 0x10
    WindowMinimized = 0x20
    LeftButton = 0x40
    RightButton = 0x80
    AA_Use96Dpi = 0x100
    AlignCenter = 0x200
    PointingHandCursor = 0x400
    AlignLeft = 0x800
    AlignVCenter = 0x1000
    AlignRight = 0x2000
    ScrollBarAlwaysOff = 0x4000
    ScrollBarAlwaysOn = 0x8000
    Checked = 0x10000
    Popup = 0x20000
    FramelessWindowHint = 0x40000
    WA_TranslucentBackground = 0x80000
    BottomDockWidgetArea = 0x100000
    UserRole = 0x200000
    red = 0x300000

QtCore.Qt = Qt
QtCore.Signal = Signal

class QObject:
    def __init__(self, *args, **kwargs):
        super().__init__()

QtCore.QObject = QObject

class QRunnable:
    def run(self):
        pass

QtCore.QRunnable = QRunnable

class QThreadPool:
    def __init__(self, *args, **kwargs):
        pass

    def start(self, runnable):
        # Execute synchronously on a thread so that run() completes but in background
        if hasattr(runnable, "run"):
            t = Thread(target=runnable.run)
            t.daemon = True
            t.start()

QtCore.QThreadPool = QThreadPool

class QTimer:
    @staticmethod
    def singleShot(ms, func):
        func()

QtCore.QTimer = QTimer

class QDateTime:
    def __init__(self):
        pass

    @staticmethod
    def currentDateTime():
        return QDateTime()

    @staticmethod
    def fromString(text, fmt):
        # Very naive parser – not needed for assertions in tests
        return QDateTime()

    def toString(self, fmt="yyyy-MM-dd HH:mm:ss"):
        return "1970-01-01 00:00:00"

    def __le__(self, other):
        return True

QtCore.QDateTime = QDateTime

# QtGui ------------------------------------------------------------------------
QtGui = types.ModuleType("PySide6.QtGui")

class QPixmap:
    def __init__(self, *args, **kwargs):
        if len(args) >= 2 and all(isinstance(a, int) for a in args[:2]):
            self._w, self._h = args[0], args[1]
        else:
            self._w = self._h = 0
        self._mask = None

    def isNull(self):
        return self._w == 0 and self._h == 0

    def scaled(self, w, h, aspect_mode=None, transform_mode=None):
        pm = QPixmap(w, h)
        return pm

    def fill(self, color):
        # No-op for stub
        pass

    def width(self):
        return self._w

    def height(self):
        return self._h

    def size(self):
        return self

    # Mask related helpers
    def setMask(self, mask):
        self._mask = mask

    def createMaskFromColor(self, color):
        return None

QtGui.QPixmap = QPixmap

class QPainter:
    Antialiasing = 1
    def __init__(self, *args, **kwargs):
        pass

    def setRenderHint(self, *args, **kwargs):
        pass

    def setBrush(self, *args, **kwargs):
        pass

    def setPen(self, *args, **kwargs):
        pass

    def drawEllipse(self, *args, **kwargs):
        pass

    def end(self):
        pass

QtGui.QPainter = QPainter

class QBrush:
    def __init__(self, *args, **kwargs):
        pass

QtGui.QBrush = QBrush

class QColor:
    def __init__(self, *args, **kwargs):
        pass

QtGui.QColor = QColor

class QIcon:
    def __init__(self, *args, **kwargs):
        pass

QtGui.QIcon = QIcon

class QFont:
    def __init__(self, *args, **kwargs):
        pass

QtGui.QFont = QFont

class QAction(QObject):
    def __init__(self, *args, **kwargs):
        super().__init__()
        # Provide an actual signal instance so `.connect` works
        self.triggered = _SignalInstance()

    def setShortcut(self, shortcut):
        pass

QtGui.QAction = QAction

# QtWidgets --------------------------------------------------------------------
QtWidgets = types.ModuleType("PySide6.QtWidgets")

# Base widget
class QWidget(QtCore.QObject):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self._visible = False
        self._window_title = ""
        self._geometry = [0, 0, 640, 480]

    # Geometry helpers
    def setGeometry(self, x, y, w, h):
        self._geometry = [x, y, w, h]

    def geometry(self):
        class _Rect:
            def __init__(self, g):
                self._g = g
            def width(self):
                return self._g[2]
            def height(self):
                return self._g[3]
        return _Rect(self._geometry)

    def setMinimumSize(self, w, h):
        pass

    def show(self):
        self._visible = True

    def hide(self):
        self._visible = False

    def isVisible(self):
        return self._visible

    def setReadOnly(self, ro):
        pass

    def setMinimumWidth(self, w):
        pass

    def setMinimumHeight(self, h):
        pass

    def setMaximumWidth(self, w):
        pass

    # Generic action handling ---------------------------------------------------
    def addAction(self, action):
        if not hasattr(self, '_actions'):
            self._actions = []
        self._actions.append(action)

    def setWindowTitle(self, title):
        self._window_title = title

    def windowTitle(self):
        return self._window_title

    def setFixedWidth(self, w):
        pass

    def setAttribute(self, *args, **kwargs):
        pass

    def setWindowFlags(self, *args, **kwargs):
        pass

    def setCursor(self, *args, **kwargs):
        pass

    def setToolTip(self, *args, **kwargs):
        pass

    def setAlignment(self, *args, **kwargs):
        pass

    def mapToGlobal(self, pos):
        return pos

    def rect(self):
        class _Rect:
            def __init__(self, w):
                self._w = w
            def bottomLeft(self):
                return type("Point", (), {"x": lambda self: 0, "y": lambda self: 0})()
        return _Rect(self)

    def showNormal(self):
        self._visible = True

    def addPermanentWidget(self, w, *args, **kwargs):
        self.addWidget(w)

QtWidgets.QWidget = QWidget

class QApplication(QWidget):
    _inst = None
    def __init__(self, argv=None):
        super().__init__()
        QApplication._inst = self

    @staticmethod
    def instance():
        return QApplication._inst

    def exec(self):
        return 0

    def processEvents(self):
        pass

    @staticmethod
    def primaryScreen():
        class _Screen:
            def geometry(self_inner):
                class _Geom:
                    def width(self):
                        return 1920
                    def height(self):
                        return 1080
                return _Geom()
        return _Screen()

QtWidgets.QApplication = QApplication

class QMenuBar(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._menus = []
    def addMenu(self, title):
        menu = QMenu(self)
        self._menus.append((title, menu))
        return menu
QtWidgets.QMenuBar = QMenuBar

class QMainWindow(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._central_widget = None

    def setCentralWidget(self, w):
        self._central_widget = w

    def centralWidget(self):
        return self._central_widget

    def close(self):
        self.hide()

    def menuBar(self):
        if not hasattr(self, "_menu_bar"):
            self._menu_bar = QMenuBar(self)
        return self._menu_bar

    def addDockWidget(self, *args, **kwargs):
        pass

QtWidgets.QMainWindow = QMainWindow

# Layout stubs -----------------------------------------------------------------
class _BaseLayout:
    def __init__(self, parent=None):
        self.parent = parent
        self.widgets = []
    def addWidget(self, w, *args, **kwargs):
        self.widgets.append(w)
    def setSpacing(self, *args, **kwargs):
        pass
    def setContentsMargins(self, *args, **kwargs):
        pass

class QVBoxLayout(_BaseLayout):
    pass
QtWidgets.QVBoxLayout = QVBoxLayout
class QHBoxLayout(_BaseLayout):
    pass
QtWidgets.QHBoxLayout = QHBoxLayout

class QGridLayout(_BaseLayout):
    pass
QtWidgets.QGridLayout = QGridLayout

# Basic interactive widgets ----------------------------------------------------
class QLabel(QWidget):
    def __init__(self, text="", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._text = text
        self._pixmap = None
    def setText(self, txt):
        self._text = txt
    def text(self):
        return self._text
    def setPixmap(self, pixmap):
        self._pixmap = pixmap
    def pixmap(self):
        return self._pixmap
    def setAlignment(self, *args, **kwargs):
        pass
QtWidgets.QLabel = QLabel

class QPushButton(QWidget):
    def __init__(self, text="", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._text = text
        self.clicked = _SignalInstance()
    def text(self):
        return self._text
    def click(self):
        self.clicked.emit()
QtWidgets.QPushButton = QPushButton

class QLineEdit(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._text = ""
        self.returnPressed = Signal()
        self.textEdited = Signal(str)
        self.editingFinished = Signal()
    def text(self):
        return self._text
    def setText(self, txt):
        self._text = txt
        self.textEdited.emit(txt)
    def clear(self):
        self._text = ""
        self.textEdited.emit("")
    def width(self):
        return 100
QtWidgets.QLineEdit = QLineEdit

class QListWidgetItem:
    def __init__(self, text=""):
        self._text = text
        self._data = {}
    def text(self):
        return self._text
    def setTextAlignment(self, *args, **kwargs):
        pass
    def setData(self, role, value):
        self._data[role] = value
    def data(self, role):
        return self._data.get(role)
    def row(self):
        return -1
QtWidgets.QListWidgetItem = QListWidgetItem

class QListWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._items = []
        self._current_row = 0
        self.currentRowChanged = Signal(int)

    def addItem(self, item):
        self._items.append(item)
    def setFixedWidth(self, w):
        pass
    def setSelectionMode(self, *args, **kwargs):
        pass
    def setFlow(self, *args, **kwargs):
        pass
    def setSpacing(self, *args, **kwargs):
        pass
    def setVerticalScrollMode(self, *args, **kwargs):
        pass
    def setHorizontalScrollBarPolicy(self, *args, **kwargs):
        pass
    def setVerticalScrollBarPolicy(self, *args, **kwargs):
        pass
    def setCurrentRow(self, idx):
        self._current_row = idx
        self.currentRowChanged.emit(idx)
    def currentRow(self):
        return self._current_row
    def count(self):
        return len(self._items)
QtWidgets.QListWidget = QListWidget

# Table ------------------------------------------------------------------------
class QTableWidgetItem:
    def __init__(self, text=""):
        self._text = text
    def text(self):
        return self._text
    def row(self):
        return getattr(self, "_row", -1)
QtWidgets.QTableWidgetItem = QTableWidgetItem

class QTableWidget(QWidget):
    MultiSelection = 1
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._columns = 0
        self._data = []  # list of rows, each row is list of items
        self._selection = set()
    # Column/Row management
    def setColumnCount(self, count):
        self._columns = count
    def columnCount(self):
        return self._columns
    def setHorizontalHeaderLabels(self, labels):
        pass
    def insertRow(self, row_idx):
        while len(self._data) <= row_idx:
            self._data.append([None] * self._columns)
    def rowCount(self):
        return len(self._data)
    def setRowCount(self, count):
        self._data = self._data[:count]
    def setItem(self, row, col, item):
        self.insertRow(row)
        self._data[row][col] = item
        item._row = row
    def item(self, row, col):
        try:
            return self._data[row][col]
        except IndexError:
            return None
    def setRowHidden(self, row, hide):
        if not hasattr(self, "_hidden_rows"):
            self._hidden_rows = set()
        if hide:
            self._hidden_rows.add(row)
        else:
            self._hidden_rows.discard(row)
    def removeRow(self, row):
        if 0 <= row < len(self._data):
            del self._data[row]
    # Selection
    def setSelectionMode(self, mode):
        pass
    def selectRow(self, row):
        # Select all items in the row
        for col in range(self._columns):
            item = self.item(row, col)
            if item:
                self._selection.add(item)
    def selectedItems(self):
        return list(self._selection)

    def isRowHidden(self, row):
        return hasattr(self, "_hidden_rows") and row in self._hidden_rows

QtWidgets.QTableWidget = QTableWidget

class QStackedWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._widgets = []
        self._current = 0
    def addWidget(self, w):
        self._widgets.append(w)
    def count(self):
        return len(self._widgets)
    def setCurrentIndex(self, idx):
        self._current = idx
    def currentIndex(self):
        return self._current
QtWidgets.QStackedWidget = QStackedWidget

# Misc widgets / placeholders ---------------------------------------------------
class QProgressBar(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._value = 0
    def setValue(self, v):
        self._value = v
    def setFormat(self, fmt):
         self._format = fmt

QtWidgets.QProgressBar = QProgressBar

class QMessageBox:
    @staticmethod
    def warning(parent, title, message):
        pass
QtWidgets.QMessageBox = QMessageBox

class QDialog(QWidget):
    Accepted = 1
    def exec_(self):
        return QDialog.Accepted
QtWidgets.QDialog = QDialog

class QFrame(QWidget):
    VLine = 0
QtWidgets.QFrame = QFrame

# Other simple placeholders
class QDockWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._widget = None
    def setWidget(self, w):
        self._widget = w
QtWidgets.QDockWidget = QDockWidget

class QTextEdit(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._text=""
    def append(self, txt):
        self._text += txt + "\n"
QtWidgets.QTextEdit = QTextEdit

QtWidgets.QStatusBar = QWidget
QtWidgets.QMenuBar = QWidget
class QSystemTrayIcon(QWidget):
    Information = 1
    def __init__(self, icon=None, parent=None):
        super().__init__(parent)
        self._icon = icon
        self._visible = True
        self._menu = None
    def setContextMenu(self, menu):
        self._menu = menu
    def contextMenu(self):
        return self._menu
    def isVisible(self):
        return self._visible
    def show(self):
        self._visible = True
QtWidgets.QSystemTrayIcon = QSystemTrayIcon

class QMenu(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._actions = []
        self._menus = []
    def addAction(self, action):
        # Fallback for widgets that support adding actions
        if not hasattr(self, '_actions'):
            self._actions = []
        self._actions.append(action)
    def actions(self):
        return self._actions
    def addMenu(self, title):
        menu = QMenu(self)
        self._menus.append((title, menu))
        return menu

QtWidgets.QFormLayout = _BaseLayout
QtWidgets.QDialogButtonBox = QWidget
QtWidgets.QCheckBox = QWidget
QtWidgets.QHeaderView = QWidget
QtWidgets.QComboBox = QWidget
QtWidgets.QGroupBox = QWidget
QtWidgets.QDateTimeEdit = QWidget
QtWidgets.QAbstractItemView = QWidget
QtWidgets.QGraphicsDropShadowEffect = QWidget
QtWidgets.QFileDialog = QWidget

# Dynamic fallback for any missing widget classes
def _create_placeholder_widget(name):
    return type(name, (QWidget,), {})

def _qtwidgets_getattr(attr):
    cls = _create_placeholder_widget(attr)
    setattr(QtWidgets, attr, cls)
    return cls

QtWidgets.__getattr__ = _qtwidgets_getattr

# Register submodules in sys.modules -------------------------------------------
sys.modules["PySide6.QtCore"] = QtCore
sys.modules["PySide6.QtGui"] = QtGui
sys.modules["PySide6.QtWidgets"] = QtWidgets

# Re-export for `from PySide6 import ...` (rarely used in this codebase)
setattr(sys.modules[__name__], "QtCore", QtCore)
setattr(sys.modules[__name__], "QtGui", QtGui)
setattr(sys.modules[__name__], "QtWidgets", QtWidgets)

# Create a minimal QtTest submodule required by pytest-qt -----------------------
QtTest = types.ModuleType("PySide6.QtTest")

class _QTest:
    @staticmethod
    def qWait(ms):
        pass
    @staticmethod
    def mouseClick(widget, button, delay=0):
        # Invoke widget.click() if available as a best-effort simulation
        if hasattr(widget, "click"):
            widget.click()
    @staticmethod
    def keyClicks(widget, text, delay=0):
        if hasattr(widget, "setText"):
            widget.setText(text)

QtTest.QTest = _QTest
sys.modules["PySide6.QtTest"] = QtTest

QtCore.qDebug = lambda *args, **kwargs: None
QtCore.qWarning = lambda *args, **kwargs: None
QtCore.qInfo = lambda *args, **kwargs: None
QtCore.qFatal = lambda *args, **kwargs: None
QtCore.qCritical = lambda *args, **kwargs: None
QtCore.Slot = lambda *args, **kwargs: (lambda f: f)
QtCore.Property = lambda *args, **kwargs: property(lambda self: None)
QtCore.qInstallMessageHandler = lambda handler: None