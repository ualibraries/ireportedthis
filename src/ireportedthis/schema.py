import yaml

class Schema( object ):

    def __init__( self ):
        
        self.tree = {}
    
class YAMLSchema( Schema ):
    
    def __init__( self, path_to_schema_file ):
        super().__init__()
        
        self.path_to_schema_file = path_to_schema_file
        
        with open( self.path_to_schema_file ) as f:
            self.tree = yaml.safe_load( f )
            
    def pretty_print( self, tagsonly = False ):
        
        self._print_branch( self.tree[0], tagsonly )

    def _print_branch( self, branch, tagsonly, depth = 0 ):

        if tagsonly:
            line = '%s #%s' % ( '    ' * depth, branch['tag'] )
        else:
            line = '%s* %s (#%s)' % ( '    ' * depth,
                                      branch['name'],
                                      branch['tag'] )

        print( line )

        if branch['branches']:
            for b in branch['branches']:
                self._print_branch( b, tagsonly, depth + 1 )

    @property
    def source( self ):            
        return 'yaml | %s' % ( self.path_to_schema_file )
