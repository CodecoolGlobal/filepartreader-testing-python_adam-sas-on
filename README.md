# Assignment: FilePartReader testing in Python

In this assignment, we will work with files, because we can't have enough file readers. :) Your job is to implement 2 classes and cover them with tests.

This is a Python version of the [FilePartReader testing with JUnit](https://github.com/CodecoolGlobal/filepartreader-testing-with-junit-adam-sas-on) exercise.

## Implementation

### FilePartReader class

#### It has one constructor:

* it sets the class' instance variables to some invalid default value

#### It has three instance methods:

* `setup()`
  - its parameters are:
    - `file_path` as a string
    - `from_line` as an integer
    - `to_line` as an integer
  - it throws a `ValueError`:
    - if `to_line` is smaller than `from_line`
    - if `from_line` is smaller than 1
* `read()`
  - opens the file on `file_path`, and gives back it's content as a string
  - it doesn't catch the exception being raised, if the file isn't present on `file_path`, we can expect a `FileNotFoundError`
* `read_lines()`
  - reads the file with `read()`
  - it gives back every line from its content between `from_line` and `to_line` (both of them are included), and returns these lines as a list of strings. Take care because if `from_line` is 1, it means the very first row in the file. Also, if `from_line` is 1 and `to_line` is 1 also, we will read only the very first line.

### FileAnalyzer class

#### It has one constructor:

* its parameter is a `FilePartReader` object

#### It has three instance methods:

* `get_lines_ordered_aphabetically()`:
  - calls `FilePartReader.read_lines()`
  - returns the lines ordered alphabetically as a list
* `get_lines_containing_substring( substring )`:
  - calls `FilePartReader.read_lines()`
  - returns the lines which contain the `substring`
* `get_palindromes()`:
  - calls `FilePartReader.read_lines()`
  - returns the lines that are palindromes

## Testing

When you are ready, your job is to cover your code with tests, and make an assertion for all the statements in the bullet points. When testing `FilePartReader` class, you can have a test file with which you can test the read method.

