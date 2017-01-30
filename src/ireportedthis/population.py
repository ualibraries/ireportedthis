import csv
import datetime
import re
import yaml

class Population( object ):
    
    def __init__( self ):

        self.entry_rx_short = re.compile( '^\s*#(?P<tag>\w+)\s+(?P<effort>\d+|\d+\.\d+|\.\d+)\s*(h|hr|hrs)\s*$' )
        self.entry_rx_long = re.compile( '^\s*(?P<description>.*?)\s+#(?P<tag>\w+)\s+(?P<effort>\d+|\d+\.\d+|\.\d+)\s*(h|hr|hrs)\s*$' )

        self.entries = []
        self.entries_rejected = []
        self.entries_earliest = False
        self.entries_latest = False

        self.tag_counts = {}

    def _sum_tags( self ):
        
        for e in self.entries:
            if e['tag'] not in self.tag_counts:
                self.tag_counts[e['tag']] = 0
            self.tag_counts[e['tag']] += e['effort']
            
    def _set_earliest_and_latest( self ):
        
        self.entries_earliest = min( [ e['date'] for e in self.entries ] )
        self.entries_latest = max( [e['date'] for e in self.entries ] )

class CSVPopulation( Population ):

    def __init__( self, path_to_export_file, path_to_filter_file ):
        super().__init__()
        
        self.path_to_export_file = path_to_export_file
        self.path_to_filter_file = path_to_filter_file
        
        with open( self.path_to_filter_file ) as f:
            self.filters = yaml.safe_load( f )
        
        with open( self.path_to_export_file, newline='' ) as f:
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
                
                if r[0] in self.filters['skip']:
                    continue
                
                m = self.entry_rx_short.match( r[2] )
                if m:
                    
                    if m.group( 'tag' ) in self.filters['tags'].keys():
                        filtered_tag = self.filters['tags'][m.group( 'tag' )]
                    else:
                        filtered_tag = m.group( 'tag' )
                    
                    self.entries.append( {
                        'email': r[0],
                        'date': datetime.datetime.strptime( r[4], '%Y-%m-%d' ),
                        'description': '(none)',
                        'tag': filtered_tag,
                        'effort': float( m.group( 'effort' ) )
                    } )
                    continue
            
                m = self.entry_rx_long.match( r[2] )
                if m:

                    if m.group( 'tag' ) in self.filters['tags'].keys():
                        filtered_tag = self.filters['tags'][m.group( 'tag' )]
                    else:
                        filtered_tag = m.group( 'tag' )
                    
                    self.entries.append( {
                        'email': r[0],
                        'date': datetime.datetime.strptime( r[4], '%Y-%m-%d' ),
                        'description': m.group( 'description' ),
                        'tag': filtered_tag,
                        'effort': float( m.group( 'effort' ) )
                    } )
                    continue
            
                self.entries_rejected.append( {
                    'email': r[0],
                    'date': r[4],
                    'body': r[2]
                } )
                
        self._sum_tags()
        self._set_earliest_and_latest()
        
    @property
    def source( self ):
        return 'csv | %s | %s' % ( self.path_to_export_file, self.path_to_filter_file )
