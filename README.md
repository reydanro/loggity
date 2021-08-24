# Loggity
A Sublime Text 3 plugin to filter timestamped log messages in a text file. 

A timestamped log message:
- starts from a line that begins with a timestamp (e.g. `2021-08-21 10:32:06`)
- contains all following lines of text until the start of the next log message.

When filtering a log message, the entire body will be analyzed. If the search term is found, the entire log message is included/excluded from the results. 

# Installation
**MacOS**
Clone this repo in `~/Library/Application Support/Sublime Text 3/Packages/Loggity`
Sublime Text should pick up the new plugin automatically.

# Usage
The plugin supports filtering by inclusion/exclusion using a string or regex.

MacOS: Use the command search CMD+SHIFT+P and search for `Loggity`. The 4 filtering options should appear in the menu.
Alternatively, you can access these through the Edit -> Loggity menu too.
