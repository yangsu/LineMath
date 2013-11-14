import sublime, sublime_plugin

class LineMathCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        for region in self.view.sel():
            if not region.empty():
                selected = self.view.substr(region)
                convert = float if '.' in selected else int
                try:
                    num = float(selected)
                    self.view.replace(edit, region, str(convert(num + 1)))
                except:
                    msg = "%s is not a number" % selected.strip()
                    sublime.message_dialog(msg)
                    pass
