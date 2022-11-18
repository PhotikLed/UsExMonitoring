def set_axis(self):
    self.CPU_graphicsView.setLabel(axis='left', text='Температура в °С')
    self.CPU_graphicsView.setLabel(axis='bottom', text='Время в секундах')

    self.GPU_graphicsView.setLabel(axis='left', text='Температура в °С')
    self.GPU_graphicsView.setLabel(axis='bottom', text='Время в секундах')


def add_legend(self):
    self.CPU_graphicsView.addLegend()
    self.GPU_graphicsView.addLegend()
