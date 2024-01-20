"""Class that renders scripts for a widget in CS-Studio"""

from lxml import etree as et


class OpiScripts:
    """Class that renders scripts for a widget in CS-Studio"""

    def render(self, widget_node, tag_name, scripts):
        """Does actual rendering"""

        if len(scripts) != 0:
            scripts_node = et.SubElement(widget_node, "scripts")
            for script in scripts:
                # Embedded Script
                if script.embed:
                    # Create a path_node with specific attributes
                    path_node = et.SubElement(scripts_node,
                                              "path",
                                              pathString="EmbeddedPy",
                                              checkConnect="true",
                                              sfe="false",
                                              seoe="false")

                    # Add the script name
                    et.SubElement(path_node, "scriptName").text = script.name

                    # Read the script file and embed it into the XML
                    with open(script.script_path, 'r', encoding="utf-8") as file:
                        script_text = file.read()

                    et.SubElement(path_node, "scriptText").text = et.CDATA(script_text)

                # Non-embedded script
                else:
                    path_node = et.SubElement(scripts_node, "path")
                    path_node.set("pathString", script.script_path)

                # Add the PVs
                for process_variable, trigger in script.pvs:
                    et.SubElement(path_node, "pv", trig=str(trigger)).text = str(process_variable)
