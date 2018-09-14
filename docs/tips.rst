====
Tips
====

The Command: `git mv -f`
------

Sometimes you might want to rename files in terms of only changing their case. Unfortunately, on some operating systems, filenames are case-insensitive.
You can take the following steps to achieve this goal:

1) Rename by *adding* a prefix/suffix to the files you want to rename by Namanager.
2) Use git to stage the file.
3) Rename the file *again*, except removing the prefix/suffix you added previously this time.
4) Finally, stage the file again using git and the file should be renamed as expected.
