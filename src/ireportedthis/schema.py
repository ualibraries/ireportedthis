import yaml

class Schema( object ):

    def __init__( self ):
        
        self.tree = {}
    
class YAMLSchema( Schema ):
    
    def __init__( self, path_to_file ):
        super().__init__()
        
        self.path_to_file = path_to_file
        
        with open( self.path_to_file ) as f:
            self.tree = yaml.safe_load( f )

    @property
    def source( self ):            
        return 'yaml | %s' % ( self.path_to_file )
