# README

(M. Simpson, 10/10/2016)

This is a quickish Python-based hack to pull and compile effort reporting statistics out of
properly-formatted IDoneThis entries.  There's an "idt" CLI script that will someday turn
into something useful, but for the moment all it does is print a version number.

The current how-to-use-this goes something like:

*   Clone the repository, and go through some variant of the setup steps outlined
    in "DEVELOPERS.md".
    
*   Pull a CSV file of some set of IDoneThis entries via the web interface's
    "EXPORT" button, and save it to "data/something.csv".
    
*   Create (or use an existing) YAML schema file (for sorting the effort-reporting
    entries into hierarchical categories based on hashtags), putting it under
    "config/something.yaml" for posterity.
    
*   Do something akin to this:

        % python
        
            import ireportedthis
            p = ireportedthis.CSVPopulation( 'data/operations_sample.csv' )
            s = ireportedthis.YAMLSchema( 'config/operations_service_tree.yaml' )
            r = ireportedthis.Report( p, s )
            r.print_report( cumulative = True, verbose = True )
            
    That should give you something to get you started, prowl the source code for
    more to play with.

If there's something you really want to see, but don't have time to code, go stick it
in the "TODO.md" file so people know.

I'm personally trying to use formal Git Flow source control, not because this project
requires it, but because I need the practice.  So feature branches and merge-to-develop,
release branches and merge-to-master, etc.  My general rules are: keep feature branches
local to my development environment, and rebase before merging, so what the "develop" branch
sees is one nice, clean, well-commented commit detailing what that particular feature
branch accomplished.  Once I get a few features finished and merged, the commit log
for "develop" will show what I mean.

