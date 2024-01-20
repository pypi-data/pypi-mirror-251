import os
import shutil
import lxml.etree as et

from .actions import OpiActions
from .axes import OpiAxis
from .borders import OpiBorder
from .colors import OpiColor
from .fonts import OpiFont
from .points import OpiPoints
from .rules import OpiRule
from .scalings import OpiDisplayScaling, OpiScaling
from .scripts import OpiScripts
from .tabs import OpiTabs
from .text import OpiText
from .traces import OpiTraces
from .widget import OpiWidget


def get_opi_renderer(widget):
    tr = OpiText()
    wr = OpiWidget(tr)

    wr.add_renderer('actions', OpiActions())
    # tabs
    wr.add_renderer('tabs', OpiTabs())

    cr = OpiColor()
    wr.add_renderer('background_color', cr)
    wr.add_renderer('foreground_color', cr)
    wr.add_renderer('line_color', cr)
    wr.add_renderer('bulb_border_color', cr)
    wr.add_renderer('off_color', cr)
    wr.add_renderer('on_color', cr)
    wr.add_renderer('line_color', cr)
    wr.add_renderer('border_color', cr)
    wr.add_renderer('led_border_color', cr)

    # Tank widget
    wr.add_renderer('color_fillbackground', cr)
    wr.add_renderer('fill_color', cr)

    wr.add_renderer('rules', OpiRule(tr, cr))

    wr.add_renderer('border', OpiBorder(tr, cr))

    wr.add_renderer('font', OpiFont())

    wr.add_renderer('auto_scale_widgets', OpiDisplayScaling(tr))
    wr.add_renderer('scale_options', OpiScaling(tr))

    # Necessary for rendering of XYGraph
    wr.add_renderer('traces', OpiTraces(cr))
    wr.add_renderer('axes', OpiAxis(cr))

    wr.add_renderer('scripts', OpiScripts())

    wr.add_renderer('points', OpiPoints())
    return OpiRenderer(widget, wr)


class OpiRenderer(object):

    def __init__(self, model, widget_renderer):
        self._model = model
        self._node = None
        self._widget_renderer = widget_renderer
        # required resources distributed with the generated OPI.
        self._resources = {}

    def assemble(self, model=None, parent=None):
        if model is None:
            model = self._model
        self._node = self._widget_renderer.render(model, parent,
                                                  self._resources)

    def get_node(self):
        return self._node

    def __str__(self):
        self.assemble()
        return str(et.tostring(self._node))

    def write_resources(self, filename):
        if self._resources:
            opi_dirpath = os.path.abspath(os.path.dirname(filename))
            for res_abspath, opi_relpath in self._resources.items():
                dst_abspath = os.path.join(opi_dirpath, opi_relpath)
                os.makedirs(os.path.dirname(dst_abspath), exist_ok=True)
                shutil.copy(res_abspath, dst_abspath)

    def write_to_file(self, filename):
        self.assemble()
        tree = et.ElementTree(self._node)
        tree.write(filename,
                   pretty_print=True,
                   encoding='UTF-8',
                   xml_declaration=True)
        self.write_resources(filename)