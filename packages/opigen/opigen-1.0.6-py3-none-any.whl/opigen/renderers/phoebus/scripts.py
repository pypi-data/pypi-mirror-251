"""Class that renders scripts for a widget in Phoebus"""

from lxml import etree as et


class OpiScripts:
    """Class that renders scripts for a widget in Phoebus"""

    def render(self, widget_node, tag_name, scripts):
        """Does actual rendering"""

        if len(scripts) != 0:
            scripts_node = et.SubElement(widget_node, "scripts")
            for script in scripts:
                # Embedded Script
                if script.embed:
                    # Create a script_node with specific attributes
                    script_node = et.SubElement(scripts_node, "script", file="EmbeddedPy")

                    # Read the script file and embed it into the XML
                    with open(script.script_path, 'r', encoding="utf-8") as file:
                        script_text = file.read()

                    et.SubElement(script_node, "text").text = et.CDATA(script_text)

                # Non-embedded script
                else:
                    script_node = et.SubElement(scripts_node, "script", file=script.script_path)

                # Add the PVs
                for process_variable, trigger in script.pvs:
                    et.SubElement(script_node, "pv_name",
                                  trigger=str(trigger)).text = str(process_variable)
