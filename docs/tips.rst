====
Tips
====

The Command: `git mv -f`
------

Sometimes you might want to rename files with case only, but filename are insensitive in some OSs.
You could take the following steps to achieve it:

1) Rename with *adding* prefix/suffix to the files you want to rename by Namanager.
2) Use git command to move it from **working space** to **index**.
3) Again, Rename with *remove* prefix/suffix to it.
4) Finally, add it by git command then you could see the files is renamed in **index**.
