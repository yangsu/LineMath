import sublime, sublime_plugin, re

class PromptLineMathCommand(sublime_plugin.WindowCommand):
    def run(self):
        self.window.show_input_panel("Expression:", "", self.on_done, None, None)
        pass

    def on_done(self, text):
        try:
            active_view = self.window.active_view()
            if active_view:
                active_view.run_command("line_math", {"exp": text})
        except ValueError:
            pass


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


ref = '$'


class LineMathCommand(sublime_plugin.TextCommand):
    def execExp(self, num, text):
        numstr = "(%s)" % num
        if ref in text:
            exp = text.replace(ref, numstr)
        else:
            exp = numstr + text
        return eval(exp)

    def run(self, edit, exp):
        for region in self.view.sel():
            if not region.empty():
                selected = self.view.substr(region)
                if not is_number(selected):
                    msg = "%s is not a number" % selected
                    sublime.message_dialog(msg)
                    break

                convert = float if '.' in selected else int
                try:
                    result = self.execExp(selected, exp)
                    self.view.replace(edit, region, str(convert(result)))
                except:
                    msg = "Invalid syntax: %s" % exp
                    sublime.message_dialog(msg)
                    break
