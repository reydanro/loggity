# Loggity
A Sublime Text 3 plugin to facilitate working with timestamped log messages in a text file. 

A timestamped log message will:
- start from a line that begins with a timestamp (e.g. `2021-08-21 10:32:06`)
- contain all following lines of text until the start of the next log message.

**Filtering** Loggity will allow you to filter log messages based on a string or a regex, either to include or exclude messages. When filtering a log message, the entire body will be analyzed. If the search term is found, the entire log message is included/excluded from the results. 

**Syntax Highlighting** Loggity introduces a new type of file (Loggity File) that will add the ability for custom syntax highlighting. To benefit from this, you will need to customize your color scheme and add a few more semantic colors:
```
// Documentation at https://www.sublimetext.com/docs/color_schemes.html
{
	"variables":
	{
	},
	"globals":
	{
	},
	"rules":
	[
        {
            "name": "Loggity Timestamp",
            "scope": "loggity.timestamp",
            "foreground": "orange"
        },
        {
            "name": "Loggity Verbose",
            "scope": "loggity.verbose",
            "foreground": "gray"
        },
        {
            "name": "Loggity Object Instance",
            "scope": "loggity.object_instance",
            "foreground": "mediumpurple",
        },
        {
            "name": "Loggity Comment",
            "scope": "loggity.comment",
            "foreground": "var(grey)",
        },
        {
            "name": "Loggity Comment",
            "scope": "loggity.comment.important",
            "foreground": "white",
            "background": "black",
            "font_style": "bold"
        },
        {
            "name": "Loggity Comment",
            "scope": "loggity.comment.question",
            "foreground": "red",
            "background": "black",
            "font_style": "bold"
        },
	]
}
```



# Installation
**Package Control**
1. Install the package control module in sublime (https://packagecontrol.io/installation)
2. In package control, then add a repository that points to: https://github.com/reydanro/loggity
3. Search and install the `Loggity` package from package control.

**Manual (MacOS)**
1. Clone this repo in `~/Library/Application Support/Sublime Text 3/Packages/Loggity`
2. Sublime Text should pick up the new plugin automatically.

# Usage
The plugin supports filtering by inclusion/exclusion using a string or regex.

MacOS: Use the command search CMD+SHIFT+P and search for `Loggity`. The 4 filtering options should appear in the menu.
Alternatively, you can access these through the Edit -> Loggity menu too.

For syntax highlighting select `Loggity File` from the selector on the bottom right of Sublime after you open the file. 
