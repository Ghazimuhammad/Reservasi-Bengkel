import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QToolBar, QAction
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import seaborn as sns
import pandas as pd


# Assuming you have a DataFrame named df
data = {'Category': ['A', 'B', 'C'], 'Values1': [3, 5, 7], 'Values2': [10, 5, 3], 'Values3': [10, 8, 2]}
df = pd.DataFrame(data)

class CustomFigureCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        super().__init__(fig)
        self.setParent(parent)

class GraphWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        central_widget = QWidget()
        layout = QVBoxLayout()

        # Add the navigation toolbar to the layout
        toolbar = NavigationToolbar(self, self)
        layout.addWidget(toolbar)

        # Create the first bar plot using Seaborn
        canvas1 = CustomFigureCanvas(self)
        layout.addWidget(canvas1)
        ax1 = canvas1.figure.add_subplot(111)
        sns.barplot(x='Category', y='Values1', data=df, ax=ax1)

        # Create the second bar plot using Seaborn
        canvas2 = CustomFigureCanvas(self)
        layout.addWidget(canvas2)
        ax2 = canvas2.figure.add_subplot(111)
        sns.barplot(x='Category', y='Values2', data=df, ax=ax2)

        # Create the line plot using Seaborn
        canvas3 = CustomFigureCanvas(self)
        layout.addWidget(canvas3)
        ax3 = canvas3.figure.add_subplot(111)
        sns.lineplot(x=[1, 2, 3], y=df['Values3'], ax=ax3)

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

def run():
    app = QApplication(sys.argv)
    mainWindow = GraphWindow()
    mainWindow.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    run()
