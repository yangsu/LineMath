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

class LineMathCommand(sublime_plugin.TextCommand):
    syntax = re.compile('[+\-\*\/\^](\d+(\.\d*))?')

    def checkSyntax(self, text):
        return self.syntax.match(text)

    def execExp(self, num, text):
        print(num + text)
        return eval(num + text)

    def run(self, edit, exp):
        if self.checkSyntax(exp):
            for region in self.view.sel():
                if not region.empty():
                    selected = self.view.substr(region)
                    convert = float if '.' in selected else int
                    result = self.execExp(selected, exp)
                    self.view.replace(edit, region, str(convert(result)))

        else:
            msg = "Invalid syntax: %s" % exp
            sublime.message_dialog(msg)