#!/bin/python

from .task import MBIOTask
from .xmlconfig import XMLConfig


class MBIOTaskPulsar(MBIOTask):
    def onInit(self):
        self._timeout=0
        self._period=1
        self._outputs=[]

    def onLoad(self, xml: XMLConfig):
        mbio=self.getMBIO()
        self._period=xml.getFloat('period', 1)
        items=xml.children('output')
        if items:
            for item in items:
                value=mbio[item.get('key')]
                if value and value.isWritable():
                    self._outputs.append(value)

    def poweron(self):
        self._timeout=self.timeout(self._period)
        return True

    def poweroff(self):
        return True

    def run(self):
        if self._outputs:
            if self.isTimeout(self._timeout):
                self._timeout=self.timeout(self._period)
                for value in self._outputs:
                    value.toggle()
            return min(5.0, self.timeToTimeout(self._timeout))


class MBIOTaskVirtualIO(MBIOTask):
    def onInit(self):
        pass

    def onLoad(self, xml: XMLConfig):
        items=xml.children('digital')
        if items:
            for item in items:
                name=item.get('name')
                if name:
                    self.valueDigital(name, default=item.getBool('default'), writable=True)

        items=xml.children('analog')
        if items:
            for item in items:
                name=item.get('name')
                unit=item.get('unit')
                resolution=item.getFloat('resolution', 0.1)
                if name:
                    self.value(name, unit=unit, default=item.getBool('default'), writable=True, resolution=resolution)

    def poweron(self):
        return True

    def poweroff(self):
        return True

    def run(self):
        for value in self.values:
            # value.updateValue(value.value)
            if value.isPendingSync():
                value.clearSyncAndUpdateValue()
        return 1.0


if __name__ == "__main__":
    pass
