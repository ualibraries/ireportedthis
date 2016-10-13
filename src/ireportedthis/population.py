import csv
import re
import requests

class Population( object ):
    
    def __init__( self ):

        self.entry_rx_short = re.compile( '^\s*#(?P<tag>\w+)\s+(?P<effort>\d+|\d+\.\d+|\.\d+)h\s*$' )
        self.entry_rx_long = re.compile( '^\s*(?P<description>.*?)\s+#(?P<tag>\w+)\s+(?P<effort>\d+|\d+\.\d+|\.\d+)h\s*$' )

        self.entries = []
        self.entries_rejected = []

        self.tag_counts = {}

    def _sum_tags( self ):
        
        for e in self.entries:
            if e['tag'] not in self.tag_counts:
                self.tag_counts[e['tag']] = 0
            self.tag_counts[e['tag']] += e['effort']
    
class CSVPopulation( Population ):

    def __init__( self, path_to_file ):
        super().__init__()
        
        self.path_to_file = path_to_file
        
        with open( self.path_to_file, newline='' ) as f:
            rdr = csv.reader( f )
            rdr.__next__()
            for r in rdr:

                # 0 user_email_address
                # 1 status
                # 2 body
                # 3 occurred_on
                # 4 completed_on
                # 5 created_at
                # 6 archived_at
                
                m = self.entry_rx_short.match( r[2] )
                if m:
                    self.entries.append( {
                        'email': r[0],
                        'created_at': r[5],
                        'description': '(none)',
                        'tag': m.group( 'tag' ),
                        'effort': float( m.group( 'effort' ) )
                    } )
                    continue
            
                m = self.entry_rx_long.match( r[2] )
                if m:
                    self.entries.append( {
                        'email': r[0],
                        'created_at': r[5],
                        'description': m.group( 'description' ),
                        'tag': m.group( 'tag' ),
                        'effort': float( m.group( 'effort' ) )
                    } )
                    continue
            
                self.entries_rejected.append( {
                    'email': r[0],
                    'created_at': r[5],
                    'body': r[2]
                } )
                
        self._sum_tags()
        
    @property
    def source( self ):
        return 'csv | %s' % ( self.path_to_file )

class RESTPopulation( Population ):

    def __init__( self, idt_token, idt_team_id, start_date, end_date ):
        super().__init__()

        self.idt_url = 'https://beta.idonethis.com/api/v2'

        self.idt_token = idt_token        
        self.idt_team_id = idt_team_id
        self.start_date = start_date
        self.end_date = end_date
        
        self.query_url = '%s/teams/%s/entries' % ( self.idt_url, self.idt_team_id )
        self.query_headers = { 'Authorization': 'Token %s' % ( self.idt_token ) }
        self.data = requests.get( self.query_url, self.query_headers ).json()

        for d in self.data:
            
            m = self.entry_rx_short.match( d['body'] )
            if m:
                self.entries.append( {
                    'email': d['user']['email_address'],
                    'created_at': d['created_at'],
                    'description': '(none)',
                    'tag': m.group( 'tag' ),
                    'effort': m.group( 'effort' )
                } )
                continue
            
            m = self.entry_rx_long.match( d['body' ] )
            if m:
                self.entries.append( {
                    'email': d['user']['email_address'],
                    'created_at': d['created_at'],
                    'description': m.group( 'description' ),
                    'tag': m.group( 'tag' ),
                    'effort': m.group( 'effort' )
                } )
                continue
            
            self.entries_rejected.append( {
                'email': d['user']['email_address'],
                'created_at': d['created_at'],
                'body': d['body']
            } )
            
            self._sum_tags()

    @property
    def source( self ):
        return 'rest | %s' % ( self.query_url )

