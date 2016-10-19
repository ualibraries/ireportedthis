# TODO

*   Once IDoneThis figures out why their v2 API only pulls 25 entries from a team entries call,
    get back to work on RESTPopulation.  When that happens, it's probably time to refactor the
    subclasses out into their own files, e.g. "ireportedthis/populations/rest_population.py",
    instead of just burying the subclasses in "ireportedthis/population.py". (mgs, 10/10/2016)

*   Add a CLI utility that just takes a YAML schema file and translates it into an easier-to-read
    tree structure (text or whatever), suitable to be handed out to folks doing effort reporting
    as a cheat sheet for the tags to use. (mgs, 10/14/2016)

