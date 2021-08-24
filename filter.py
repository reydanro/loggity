
import functools
import re
import sublime
import sublime_plugin

SETTINGS = "Loggity.sublime-settings"
LOCAL_SETTINGS = 'Loggity Local.sublime-settings'
LOG_START_PATTERN = "\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{6}"

def match_log(log, pattern, use_regex, case_sensitive):
    if use_regex:
        return pattern.search(log) is not None
    else:
        if not case_sensitive:
            log = log.lower()
        return log.find(pattern) >= 0


class LoggityFilterIncludingStringCommand(sublime_plugin.WindowCommand):
    def run(self):
        sublime.active_window().run_command("loggity_filter", {"invert_search": False})

class LoggityFilterExcludingStringCommand(sublime_plugin.WindowCommand):
    def run(self):
        sublime.active_window().run_command("loggity_filter", {"invert_search": True})

class LoggityFilterIncludingRegexCommand(sublime_plugin.WindowCommand):
    def run(self):
        sublime.active_window().run_command("loggity_filter", {"invert_search": False, "use_regex": True})

class LoggityFilterExcludingRegexCommand(sublime_plugin.WindowCommand):
    def run(self):
        sublime.active_window().run_command("loggity_filter", {"invert_search": True, "use_regex": True})


class LoggityFilterCommand(sublime_plugin.WindowCommand):
    def run(self, invert_search=False, use_regex=False):
        settings = sublime.load_settings(SETTINGS)

        local_settings = sublime.load_settings(LOCAL_SETTINGS)
        search_text = local_settings.get('latest_search', '')

        prompt = "Filter logs {} {}: ".format('not matching' if invert_search else 'matching', 'regex' if use_regex else 'string')

        self.invert_search = invert_search
        self.use_regex = use_regex

        sublime.active_window().show_input_panel(prompt, search_text, self.on_select, None, None)

    
    def on_select(self, term):
        if self.window.active_view():
            local_settings = sublime.load_settings(LOCAL_SETTINGS)
            local_settings.set('latest_search', term)
            sublime.save_settings(LOCAL_SETTINGS)

            self.window.active_view().run_command("loggity_filter_view", {"term": term, "invert_search":self.invert_search, "use_regex": self.use_regex})


class LoggityFilterViewCommand(sublime_plugin.TextCommand):
    def run(self, edit, term, invert_search=False, use_regex=False):
        sublime.status_message('Filtering...')
        settings = sublime.load_settings(SETTINGS)
        case_sensitive = settings.get('case_sensitive_search', True)
        self.filter_to_new_buffer(edit, term, use_regex, case_sensitive, invert_search)
        sublime.status_message('')

    def filter_to_new_buffer(self, edit, term, use_regex, case_sensitive, invert_search):
        prog = re.compile(LOG_START_PATTERN)

        if use_regex:
            term_pattern = re.compile(term, re.IGNORECASE if not case_sensitive else 0)
        else:
            if not case_sensitive:
                term = term.lower()
            term_pattern = term

        region = sublime.Region(0, self.view.size())
        lines = (self.view.substr(r) for r in self.view.split_by_newlines(region))

        log = ""
        output = ""
        for line in lines:
            # Aggregate lines until we find a new timestamp start
            if prog.match(line):
                # If we found a new log start pattern, parse the previous accumulated data
                if match_log(log, term_pattern, use_regex, case_sensitive) ^ invert_search:
                    output += log
                log = ""
            log += line + "\n"

        if len(log) > 0: 
            if match_log(log, term_pattern, use_regex, case_sensitive) ^ invert_search:
                output += log


        # Write the result to a new window
        results_view = self.view.window().new_file()
        results_view.set_name('Filter Results {} {}'.format("not matching" if invert_search else "matching", term))
        results_view.set_scratch(True)
        results_view.settings().set('word_wrap', self.view.settings().get('word_wrap'))

        results_view.run_command(
            'append', {'characters': output, 'force': True,
                       'scroll_to_end': False})

        if results_view.size() > 0:
            results_view.set_syntax_file(self.view.settings().get('syntax'))
        else:
            message = ('Filtering logs for "%s" %s\n\n0 matches\n'
                       % (term,
                          '(case-sensitive)' if case_sensitive else
                          '(not case-sensitive)'))
            results_view.run_command(
                'append', {'characters': message, 'force': True,
                           'scroll_to_end': False})
