""" Class that handles rendering of Traces. """

from lxml import etree as et


class OpiTraces(object):
    """Class that handles rendering of Traces."""

    def __init__(self, color_renderer):
        self._color = color_renderer

    def render(self, widget_node, tag_name, traces_model):
        """Renders the actual traces"""
        if len(traces_model) > 0:
            trace_root_node = et.SubElement(widget_node, "traces")
            for legend, x_pv, y_pv, line_width, y_axis, trace_color in traces_model:
                trace_node = et.SubElement(trace_root_node, "trace")
                et.SubElement(trace_node, "name").text = str(legend)
                et.SubElement(trace_node, "x_pv").text = str(x_pv)
                et.SubElement(trace_node, "y_pv").text = str(y_pv)
                et.SubElement(trace_node, "axis").text = str(y_axis)
                et.SubElement(trace_node, "line_width").text = str(line_width)
                et.SubElement(trace_node, "trace_type").text = str(5)  # Bar graph

                # None is passed as color if defaults wish to be used
                if trace_color is not None:
                    self._color.render(trace_node, 'color', trace_color)
