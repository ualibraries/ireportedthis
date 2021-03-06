import copy
import textwrap

class Report( object ):

    def __init__( self, population, schema, days, fte, hours ):
        
        self.population = population
        self.schema = schema
        self.days = days
        self.fte = fte
        self.hours = hours
        
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
            print( '    Accepted entries: %d ( %d%% )' % ( len( self.population.entries ),
                                                            round( 100 * ( len( self.population.entries )/( len( self.population.entries ) + len( self.population.entries_rejected ) ) ) ) ) )
            print( '    Rejected entries: %d ( %d%% )' % ( len( self.population.entries_rejected ),
                                                            round( 100 * ( len( self.population.entries_rejected )/( len( self.population.entries ) + len( self.population.entries_rejected ) ) ) ) ) )
            print( '    Earliest entry: %s' % ( self.population.entries_earliest.strftime( '%c' ) ) )
            print( '    Latest entry: %s' % ( self.population.entries_latest.strftime( '%c' ) ) )
            print( '  Schema: %s' % ( self.schema.source ) )
            if self.tags_in_population_not_in_schema.keys():
                print( '    Tags found in population but not in schema:' )
                print( textwrap.indent( textwrap.fill( ', '.join( sorted( self.tags_in_population_not_in_schema.keys() ) ), width = 70 ), ' ' * 6 ) )
                print( '    Unrecognized effort: %.2f hours' % ( sum( self.tags_in_population_not_in_schema.values() ) ) )
            else:
                print( '    Tags found in population but not in schema: (none)' )
                print( '    Unrecognized effort: (none)' )
            print()
            print( 'Reporting:' )
            print( '  Possible hours: %.2f days x %.2f fte x %.2f hours/day/fte = %.2f hours' % ( self.days, self.fte, self.hours, ( self.days * self.fte * self.hours ) ) )
            print( '  Reported: %d hours ( %d%% )' % ( self.focus.cumulative_effort, round( 100 * ( self.focus.cumulative_effort / ( self.days * self.fte * self.hours ) ) ) ) )
            print()
            print( 'Focus:' )
            self._print_focus( self.focus, cumulative, verbose, depth = 1 )
        else:
            self._print_focus( self.focus, cumulative, verbose )
        print()

        if rejected:
            print( 'Rejected Entries:' )
            for e in self.population.entries_rejected:
                print( '  %s | %s | %s' % ( e['email'], e['date'], e['body'] ) )
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
        
        
        