import copy

class Report( object ):

    def __init__( self, population, schema, days, fte ):
        
        self.population = population
        self.schema = schema
        self.days = days
        self.fte = fte
        
        self.tags_in_schema_not_in_population = []
        self.tags_in_population_not_in_schema = copy.deepcopy( self.population.tag_counts )
        self.focus = self._build_focus( self.schema.tree[0] )

    def _build_focus( self, start_branch ):

        name = start_branch['name']
        tag = start_branch['tag']
        if tag in self.population.tag_counts:
            effort = self.population.tag_counts[start_branch['tag']]
            self.tags_in_population_not_in_schema.pop( tag )
        else:
            self.tags_in_schema_not_in_population.append( tag )
            effort = 0.0
        
        subfoci = []
        if start_branch['branches']:
            for branch in start_branch['branches']:
                subfoci.append( self._build_focus( branch ) )
        
        f = Focus( name, tag, effort, subfoci )

        return f

    def find_focus_by_tag( self, tag ):
        
        return self._find_focus( self.focus, tag )
        
    def _find_focus( self, focus, tag ):
        
        if focus.tag == tag:
            return focus
        else:
            if len( focus.subfoci ) == 0:
                return None
            for sf in focus.subfoci:
                hit = self._find_focus( sf, tag )
                if hit:
                    return hit
       
    def print_report( self, cumulative = False, verbose = False, rejected = False ):
        
        if verbose:
            print( 'Basis:' )
            print( '  Population: %s' % ( self.population.source ) )
            print( '    Accepted Entries: %d ( %d%% )' % ( len( self.population.entries ),
                                                            round( 100 * ( len( self.population.entries )/( len( self.population.entries ) + len( self.population.entries_rejected ) ) ) ) ) )
            print( '    Rejected entries: %d ( %d%% )' % ( len( self.population.entries_rejected ),
                                                            round( 100 * ( len( self.population.entries_rejected )/( len( self.population.entries ) + len( self.population.entries_rejected ) ) ) ) ) )
            print( '  Schema: %s' % ( self.schema.source ) )
            print( '    Tags found in population but not in schema:' )
            print( '      %s' % ( ', '.join( sorted( self.tags_in_population_not_in_schema.keys() ) ) ) )
            print()
            print( 'Reporting:' )
            print( '  Possible Hours: 8 hours/day/fte x %d days x %d fte = %d hours' % ( self.days, self.fte, ( 8 * self.days * self.fte ) ) )
            print( '  Reported: %d hours ( %d%% )' % ( self.focus.cumulative_effort, round( 100 * ( self.focus.cumulative_effort / ( 8 * self.days * self.fte ) ) ) ) )
            print()
            print( 'Focus:' )
            self._print_focus( self.focus, cumulative, verbose, depth = 1 )
        else:
            self._print_focus( self.focus, cumulative, verbose )
        print()

        if rejected:
            print( 'Rejected Entries:' )
            for e in self.population.entries_rejected:
                print( '  %s | %s | %s' % ( e['email'], e['created_at'], e['body'] ) )
            print()
    
        
    def _print_focus( self, focus, cumulative, verbose, depth = 0 ):

        if verbose:
            line = '%s%s | #%s : %.2f' % ( '  ' * depth,
                                             focus.name,
                                             focus.tag,
                                             ( focus.cumulative_effort if cumulative else focus.effort ) )
        else:
            line = '%s#%s : %.2f' % ( '  ' * depth,
                                      focus.tag,
                                      ( focus.cumulative_effort if cumulative else focus.effort ) )
                    
        print( line )
        
        for sf in focus.subfoci:
            self._print_focus( sf, cumulative, verbose, depth + 1 )
        
class Focus( object ):
    
    def __init__( self, name, tag, effort, subfoci ):
        
        self.name = name
        self.tag = tag
        self.effort = effort
        self.subfoci = subfoci
    
    def __repr__( self ):
        return '<Focus|%s,%d:[%s]>' % ( self.tag, self.effort, ','.join( [ sf.tag for sf in self.subfoci ] ) ) 

    @property
    def cumulative_effort( self ):
        ce = self.effort
        for sf in self.subfoci:
            ce += sf.cumulative_effort
        return ce
        
        
        