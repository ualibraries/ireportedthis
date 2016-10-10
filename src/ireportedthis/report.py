import copy

class Report( object ):

    def __init__( self, population, schema ):
        
        self.population = population
        self.schema = schema
        self.focus = self._build_focus( self.schema.tree[0] )

    def _build_focus( self, start_branch ):

        name = start_branch['name']
        tag = start_branch['tag']
        if tag in self.population.tag_counts:
            effort = self.population.tag_counts[start_branch['tag']]
        else:
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
       
    def print_report( self, cumulative = False, verbose = False ):
        
        if verbose:
            print( 'Basis:' )
            print( '  Population: %s' % ( self.population.source ) )
            print( '    Entries: %d' % ( len( self.population.entries ) ) )
            print( '    Rejected Entries: %d' % ( len( self.population.entries_rejected ) ) )
            print( '  Schema: %s' % ( self.schema.source ) )
            print()
            print( 'Focus:' )
            self._print_focus( self.focus, cumulative, verbose, depth = 1 )
        else:
            self._print_focus( self.focus, cumulative, verbose )
        
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
        
        
        