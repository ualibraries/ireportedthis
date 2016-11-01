# README

(M. Simpson, 10/19/2016)

This is a quickish Python-based hack to pull and compile effort reporting statistics
out of properly-formatted IDoneThis entries.

The current how-to-use-this goes something like:

*   Clone the repository, and go through some variant of the setup steps outlined
    in "DEVELOPERS.md" to get yourself set up to use the tool.
    
*   Pull a CSV file of some set of IDoneThis entries via the web interface's
    "EXPORT" button, and save it to "data/something.csv".  The "data" subdirectory
    should be in the Git ignore file, to avoid accidentally checking CSV files
    into source code control.
    
*   Create (or use an existing) YAML schema file (for sorting the effort-reporting
    entries into hierarchical categories based on hashtags), putting it under
    "config/something.yaml" for posterity.  These should be checked into Git.
    You can also create (or use an existing) YAML filter file (for doing some
    basic tag transformations to clean up the population data before running the
    report).  The filter files should also be checked into Git.
    
*   Do something akin to this:

        % scripts/irt -p data/operations_201610.csv \
                      -t config/operations_filter_working.yaml \
                      -s config/operations_service_tree.yaml \
                      -d 22 -f 8 -cvr

    You can do "scripts/irt -h" to find out how all of the CLI switches work.

*   There's also an "exsch" script, which can be used to generate text and 
    Markdown format schema extracts to use as cheat sheets during data entry
    (since the scheme file YAML is a little cumbersome).  Use "scripts/exsch -h"
    to get information on CLI invocation.
    
You should also feel free to prowl the source code -- this is a very alpha utility
at this point in time.  If there's something you really want to see, but don't have
time to code, please put it in the "TODO.md" file for later reference.  If you fix
something on the TODO list, mark it done and move it down to the "TODONE" section.

I'm personally trying to use formal Git Flow source control, not because this project
requires it, but because I need the practice.  So feature branches and merge-to-develop,
release branches and merge-to-master, etc.  My general rules are: keep feature branches
local to my development environment, and rebase before merging, so what the "develop" branch
sees is one nice, clean, well-commented commit detailing what that particular feature
branch accomplished.  Once I get a few features finished and merged, the commit log
for the "develop" branch will demonstrate what I mean.
