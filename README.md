# Dictionary-Maker
Sorts Wiktionary entries into seperate files based on the letters they contain.

This program parses a Wiktionary dump file, dividing the words contained based on the letters each word contains. The Wiktionary dump file I used (and possibly the only file this program works with) is, compiled `2018-02`:

> https://dumps.wikimedia.org/enwiktionary/20180220/enwiktionary-20180220-abstract.xml.gz

The website containing the dump is:

> https://dumps.wikimedia.org/enwiktionary/20180220/

The file needs to be put in the same directory as the python script.

## Dependencies
This program has the following dependencies:
* `keyboard`

This library is necessary for user input with the `FileUtility.navigator()`, an unnecessary method of the progam. The `keyboard` dependency can be removed by either deleting this method, or by removing the import of `FileUtility` on line `21` of `Parser`.
