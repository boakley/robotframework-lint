# Change Log

## 0.7.0 - 2016-03-07
- fix for issue #30 - preserve table headings

## 0.6.1 - 2015-07-22

- added `walk` method to RobotFile class, that somehow got 
  left out in the 0.6 version.

## 0.6 - 2015-07-21

### New rules
- TooFewTestSteps
- TooFewKeywordSteps

### Issues closed
- Issue #24 - InvalidTable isn't catching everything
- Issue #25 - Rules to detect empty tests and keywords
- Issue #27 - add --describe option
- Issue #28 - --rulefile isn't working
- Issue #30 - When ResourceRule class has configure method, rflint says the rule is unknown.
- Issue #31 - A GeneralRule class rule is not passed an object with a type attribute
	
### Other changes
- small improvements to the custom parser

## 0.5 - 2015-01-26

### New rules
- Configurable rules
- New General rules:
  - LineTooLong
  - FileTooLong
  - TrailingBlankLines
- New testcase rules
  - TooManySteps (provided by guykisel)
  - TooManyTestCases (provided by guykisel)

### Issues closed
- issue #22 - FileTooLong rule
- issue #19 - rules should accept arguments
- issue #5  - "bare" comments are not parsed properly

### Other changes
- Rflint now distinguishes between resource files and test suites
  by checking whether the file has a testcase table or not
- General rules now have access to the raw text of a file, so
  they can do their own parsing if they want (issue #5)


## 0.4 - 2014-12-22

### New rules

- new Suite rules:
  - PeriodInSuiteName
  - InvalidTable

- new Testcase rules:
  - PeriodInTestName

### Issues closed:
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

