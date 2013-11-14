# Line Math

A Sublime Text Package that makes it very easy to transform selected text using math or other basic of python expressions and to generate sequences of numbers

## Installation

Using [Package Control](https://sublime.wbond.net/installation), install "LineMath"

Or:

Open the Sublime Text Packages folder

* OS X: `~/Library/Application Support/Sublime Text 3/Packages/`
* Windows: `%APPDATA%/Sublime Text 3/Packages/`
* Linux: `~/.Sublime Text 3/Packages/ or ~/.config/sublime-text-3/Packages`

```bash
git clone https://github.com/yangsu/LineMath.git
```

## Usage

Use either the keyboard shortcut `Ctrl+Alt+l` or select "LineMath: Expression" from the Command Palette to bring up a prompt.

![LineMath prompt](https://www.evernote.com/shard/s13/sh/23454c65-c92f-45f9-b088-04ac3d23b980/c6631ee00f5010b731122469069fe6da/deep/0/linemath.py---LineMath-and-linemath.py---youtube-download.png)

### Expression

Create a set of selections (find all, vertical selection, manual multiple selection, etc.) that you want to transform. Bring up the prompt.

Write any simple expressions such as `+1` (increment each selection by 1) or any small snippet of python code such as `math.pow($, 2) + random.randint()`, using `$` to refer to text associated with each selection. Press enter to execute.

#### Demo

### Generator

You can also use a special kind of expression to generate number sequences. The syntax is `<start>:<end>` or `<start>:<step>:<end>`. `<end>` is optional. When no `<end>` is specifed, the generator will generate 1 number per selection if there are multiple selections and a sequence of numbers of a predefined size will be generated inline.

#### Demo

## Preferences

* `ref_symbol`: symbol in expressions to refer to the value of the selected text. Default: `$`
* `remove_trailing_zeroes`: remove trailing zeroes after the decimal point. Default: `true`
* `generator_delimiter`: delimiter used to separate `<start>`, `<step>`, and end `<values>` for generators expressions. Default: `:`
* `generator_default_count`: how many numbers to generate when generating in a single selection. Default: `10`
* `generator_output_separator`: separator used to output generated when  generating in a single selection. Default `, `
