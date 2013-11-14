import sublime, sublime_plugin, re

class PromptLineMathCommand(sublime_plugin.WindowCommand):
    def run(self):
        self.window.show_input_panel("Expression:", "", self.on_done, None, None)
        pass

    def on_done(self, text):
        try:
            active_view = self.window.active_view()
            if active_view:
                active_view.run_command("split_selection_into_lines")
                active_view.run_command("line_math", {"exp": text})
        except ValueError:
            pass


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False




class LineMathCommand(sublime_plugin.TextCommand):
    ref = '$'
    generatorSyntax = re.compile('^[\d\-:]+$')

    def execExp(self, num, text):
        numstr = "(%s)" % num
        if self.ref in text:
            exp = text.replace(self.ref, numstr)
        else:
            exp = numstr + text
        return eval(exp)

    def syntaxError(self, exp):
        msg = "Invalid syntax: %s" % exp
        sublime.message_dialog(msg)

    def runLineMath(self, edit, exp):
        for region in self.view.sel():
            if not region.empty():
                selected = self.view.substr(region)
                if not is_number(selected):
                    msg = "%s is not a number" % selected
                    sublime.message_dialog(msg)
                    return

                try:
                    result = self.execExp(selected, exp)
                    result = re.sub(r'\.0', '', str(result))
                    self.view.replace(edit, region, result)
                except:
                    self.syntaxError(exp)
                    return


    def runGenerator(self, edit, exp):
        parts = exp.split(':')
        start = int(parts[0])
        try:
            if len(parts) == 2:
                step = 1
                end = int(parts[1]) if parts[1] else None
            elif len(parts) == 3:
                step = int(parts[1]) if parts[1] else 1
                end = int(parts[2]) if parts[2] else None
            else:
                self.syntaxError(exp)
                return
        except:
            self.syntaxError(exp)
            return

        i = start
        for region in self.view.sel():
            if not end or i <= end:
                self.view.replace(edit, region, str(i))
            i += step

    def run(self, edit, exp):
        if self.generatorSyntax.match(exp):
            self.runGenerator(edit, exp)
        else:
            self.runLineMath(edit, exp)
