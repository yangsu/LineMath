import sublime
import sublime_plugin
import re
import sys
import math
import random

SETTINGS_FILE = "LineMath.sublime-settings"
st2 = (sys.version_info[0] == 2)
settings = {}


def plugin_loaded():
    global settings
    settings = sublime.load_settings(SETTINGS_FILE)

if st2:
    sublime.set_timeout(plugin_loaded, 0)


class PromptLineMathCommand(sublime_plugin.WindowCommand):
    def run(self):
        self.window.show_input_panel("Expression:", "", self.done, None, None)
        pass

    def done(self, text):
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


def count_regions(selection):
    count = 0
    for region in selection:
        count += 1
    return count


class LineMathCommand(sublime_plugin.TextCommand):
    def __init__(self, view):
        self.view = view
        self.ref = settings.get('ref_symbol')
        regex = '^[\d\-%s]+$' % settings.get('generator_delimiter')
        self.generatorSyntax = re.compile(regex)

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
                    if settings.get('remove_trailing_zeroes'):
                        result = re.sub(r'\.0', '', str(result))
                    self.view.replace(edit, region, result)
                except:
                    self.syntaxError(exp)
                    return

    def runGenerator(self, edit, exp):
        parts = exp.split(settings.get('generator_delimiter'))
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

        selection = self.view.sel()
        count = count_regions(selection)
        if count == 1:
            for region in self.view.sel():
                count = settings.get('generator_default_count')
                end = end if end is not None else start + count * step
                numbers = [str(i) for i in range(start, end + step, step)]
                self.view.replace(edit, region, ','.join(numbers))
        else:
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
