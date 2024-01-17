# CONLL Transform - functions to manipulate CONLL data

This package constains several functions to manipulate conll data:

- `read_files`: Read one or several conll files and return a dictionary of documents.
- `read_file`: Read a conll file and return dictionary of documents.
- `write_file`: Write a conll file.
- `compute_mentions`: Compute mentions from the raw last column of the conll file.
- `compute_chains`: Compute and return the chains from the conll data.
- `sentpos2textpos`: Transform mentions `[SENT, START, STOP]` to `[TEXT_START, TEXT_STOP]`.
- `textpos2sentpos`: Transform mentions `[TEXT_START, TEXT_STOP]` to `[SENT, START, STOP]`.
- `write_chains`: Convert a list of chains to a conll coreference column.
- `replace_coref_col`: Replace the last column of `tar_docs` by the last column of `src_docs`.
- `remove_singletons`: Remove the singletons of the conll file `infpath`, and write the version without singleton in the conll file `outfpath`.
- `filter_pos`: Filter mentions that have POS in unwanted_pos, return a new mention list.
- `check_no_duplicate_mentions`: Return True if there is no duplicate mentions.
- `merge_boundaries`: Add the mentions of `boundary_docs` to `coref_docs` if they don't already exist, as singletons.
- `remove_col`: Remove columns from all tokens in docs.
- `write_mentions`: Opposite for `compute_mentions()`.  Write the last column in `sent`.
- `compare_coref_cols`: Build a conll file that merge the corefcols of several other files.
- `to_corefcol`: Write the conll file `outfpath` with just the last column (coref) of the conll file `infpath`.
- `get_conll_2012_key_pattern`: Return a compiled pattern object to match conll2012 key format.
- `merge_amalgams`: Add amalgams in documents from where they have been removed.

To use it, just import the function from `conll_transform`, for example:

```python
from conll_transform import read_files

documents = read_files("myfile.conll", "myfile2.conll")
print(documents)
```


The source can be found at [GitHub](https://github.com/boberle/corefconversion/blob/master/conll_transform.py).

