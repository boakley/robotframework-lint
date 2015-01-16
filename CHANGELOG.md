# Change Log

## 0.4 - 2014-12-22

### New rules

- new Suite rules:
  - PeriodInSuiteName
  - InvalidTable

- new Testcase rules:
  - PeriodInTestName

### Issues closed:
- a warning is written to stderr if you give a file that doesn't exist
- a warning is written to stderr if a file file can't be imported
- issue #1  - Add -A/--argumentfile
- issue #2  - Need verbose option for --list
- issue #3  - --list output includes unnecessary quotes
- issue #4  - Add ability to process directories
- issue #7  - Add "rflint" script for easier use
- issue #13 - non-breaking spaces in a test file
- issue #15 - only list files that have errors/warnings
- issue #20 - Add --rulefile option for loading rules by filename
- issue #21 - "file not found" should be printed for bad filenames 	

### Other changes
- internally, a parsed file is now either an instance of rflint.SuiteFile
  or rflint.ResourceFile, depending on whether the file has a testcase
  table in it. Prior to this change, the object was always of class RobotFile. 
  Both of these classes are a subclass of rflint.RobotFile, so any old
  code that depends on that should continue to work.

- All internal rule classes  now have a "doc" attribute for
  returning the docstring without leading whitespace on each line.

## 0.3 - 2014-12-02
### Added
- new command line options:
  - --version
- added some acceptance tests

### Fixed
- RequireTestDocumentation no longer will generate a message if the 
  suite is templated, since documentation in templated tests is cumbersome

