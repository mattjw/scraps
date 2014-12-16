# Author:   Matt J Williams
#           http://www.mattjw.net
#           mattjw@mattjw.net
# Date:     2014
# License:  MIT License


import collections


class PivotBufferedRowReader( object ):
    """Wraps around a database query and pulls out 'ancillary' rows relative
    to an advancable 'pivot' row, without the need for multiple database
    cursors or multiple passes over the result set.
    
    Ancillary rows follow a pivot row. In other words, if row i is
    the current pivot row, the first ancillary row is row i+1, the next 
    ancillary row is row i+2, and so on. 
    When the pivot is advanced, it is moved to the row following the previous
    pivot (i.e., row i+1 in this example), and the ancillary row is reset. So,
    after advancing the pivot to i+1, the first ancillary row would be i+2, the
    next ancillary row would be i+3, and so on.
    
    The database cursor (representing the database query) is advanced as
    new rows are needed. The reader does not make duplicate passes over the
    database. Database rows are buffered as needed to avoid making additional
    passes. 
    
    See `advance_pivot()` and `next_ancillary()`.
    """
    # ivars...
    #
    # pivot_index
    #   The index of the row for the MOST RECENT pivot call
    #   or is None if there has not been a call yet.
    #
    # ancil_index
    #   The index of the NEXT row for the NEXT ancil call.
    #
    # buffer
    #   Buffer for subsequent rows. Will never contain the current pivot; i.e.,
    #   only buffers rows subsequent to the current pivot.
    
    def __init__( self, cursor ):
        """The cursor is assumed to have been executed with a SELECT statement
        immediately preceding this constructor.
        """
        self.__cursor = cursor
        
        self.__pivot_row = None
        self.__pivot_index = None

        self.__ancil_index = None
        
        self.__buffer = collections.deque()
    
    def advance_pivot( self ):
        """ Advances the pivot to the row following the last pivot row and
        returns the new pivot row. The first call to this method returns the 
        first row of the result set.
        
        Calls to `next_ancillary` can not be made until `advance_pivot` has
        been called at least once. 
        
        Returns:
            A row from a result set.
            If there are no more available rows, returns None. 
        """
        # Regarding buffer advancement and retrieval...
        # We only need to handle two cases...
        #   1) The user is continuously calling advance_pivot (no intervening
        #      ancillary calls). In this case, we always fetch from the DB.
        #   2) At least one intervening next_ancil call has been made.
        #      In this case, whether we grab from the buffer depends on
        #      whether it is empty or not. 
        
        if self.__pivot_index is None:
            # First call -- simply initialise and return
            self.__pivot_index = 0
            self.__ancil_index = self.__pivot_index + 1
            
            self.__pivot_row = self.__cursor.fetchone()
            if self.__pivot_row is None:
                # ...then the cursor's run out of rows to grab
                return None
            
            return self.__pivot_row
        else:
            # Subsequent calls -- more tricky
            
            # Determine whether we get the next row from the buffer or the
            # database
            if len( self.__buffer ) >= 1:
                self.__pivot_row = self.__buffer.popleft()
            else:
                # This could be reached if, for whatever reason, the user
                # chose to continuously call advance_pivot (i.e., without
                # intervening next_ancil calls)
                self.__pivot_row = self.__cursor.fetchone()
                # note: this could return None
                
            self.__pivot_index += 1
            self.__ancil_index = self.__pivot_index + 1
            
            return self.__pivot_row
                    
    def next_ancillary( self ):
        """Get and return the next ancillary row.
        
        If the pivot has just been advanced, then this method
        will return the row following the pivot. Otherwise, this advances the
        ancillary to the row following the last ancillary row and returns
        the new ancillary row. 

        This never returns the pivot row. The earliest row it will return
        is the one immediately following the pivot. In other words, calling
        `next_ancillary()` immediately after `advance_pivot()` will return the
        row immediately following the pivot row.
        
        Returns:
            A row from a result set.
            If there are no more available rows, returns None. 
        """
        if self.__pivot_index is None:
            raise RuntimeError( "Cannot obtain an ancillary row until a pivot row has been obtained at least once" )
            
        # Need to do more sophisticated stuff with the buffer here.
        # Need to determine if the ancil index is within the range of what's
        # pre-fetched in the buffer.
        
        row_diff = self.__ancil_index - self.__pivot_index 
            # Gives the number of rows after the pivot.
            # Should always be >= 1.
        assert row_diff >= 1
        
        # Example:
        #   if row_diff=1, then we should try and use the FIRST row in the 
        #   buffer. If the buffer doesn't have enough rows (i.e., empty in the 
        #   case of row_diff=1) then we pull an extra row into the buffer.
        
        if len( self.__buffer ) < row_diff:
            buff_row = self.__cursor.fetchone()
            
            if buff_row is None:
                return None
                    # No more rows. Do not add to buffer. Do not increment
                    # the ancil_index. Do not pass go. Do not collect 200 pounds.
            
            self.__buffer.append( buff_row )
        
        assert row_diff <= len( self.__buffer )
            # because we should only ever need to pull in one more row
        
        row = self.__buffer[row_diff-1]
        
        self.__ancil_index += 1
            # recall that this is the NEXT ancil index
        
        return row 
        
        
if __name__=='__main__':
    import sqlite3
    
    #
    #
    # TEST 1
    #
    if False:
        #
        # Set up
        db_conn = sqlite3.connect( ':memory:' )
        db_conn.execute( 'CREATE TABLE TEST (letter VARCHAR(1))' )
    
        indx = ord('a')
        for i in xrange(26):
            char = chr(indx+i)
            qry = """INSERT INTO test (letter) VALUES ("%s")""" % (char)
            db_conn.execute( qry )
    
        #
        # The query
        qry = "SELECT * FROM test ORDER BY letter"

        curs = db_conn.cursor()
        curs.execute( qry )
    
        #
        # Test
        rdr = PivotBufferedRowReader( curs ) 
    
        next_piv = rdr.advance_pivot()
        while next_piv is not None:
            print "pivot:   ", next_piv
        
            for _ in xrange(30):
                next_ancil = rdr.next_ancillary()
                print "          ->  ancil: ", next_ancil
                print "  [ buff size %s ]  " % (len(rdr.__buffer))
        
            next_piv = rdr.advance_pivot()
    
    #
    # 
    # TEST 2
    #

    #
    # Set up
    db_conn = sqlite3.connect( ':memory:' )
    db_conn.execute( 'create table test (time_offset real)' )
    
    # expected pairs if 2-second max delta...
    #   1,2
    #   5,7
    #   10,11
    #   50,51
    #   50,52
    #   51,52
    #   80,81
    #   80,82
    #   81,82
    #   
    #   
    vals = [1,2,5,7,10,11,50,51,52,80,81,82]
    vals = [ [v] for v in vals ]
    qry = """INSERT INTO test (time_offset) values (?)"""
    db_conn.executemany( qry, vals )
    
    #
    # Test
    qry = "SELECT * FROM test ORDER BY time_offset ASC"

    curs = db_conn.cursor()
    curs.execute( qry )    
    
    rdr = PivotBufferedRowReader( curs ) 
    
    # assumptions:
    #   sorted into ascending order by time_offset
    
    # Start pivot iteration
    next_piv_row = rdr.advance_pivot()
    while next_piv_row is not None:
        # Process pivot row
        pivot_val = float( next_piv_row[0] )
        
        print "pivot row:   ", next_piv_row
        print "pivot val:   ", pivot_val
        
        # Start ancil iteration
        next_ancil_row = rdr.next_ancillary()
        while next_ancil_row is not None:
            # Process ancil row
            ancil_val = float( next_ancil_row[0] )
            
            print "          ancil row: ", next_ancil_row
            print "          ancil val: ", ancil_val 
            
            delta = ancil_val - pivot_val
            if delta <= 2:
                print "                   [[ diff: %s ]] [[ pair: %s | %s ]]" % (delta, pivot_val, ancil_val)
            else:
                break
            
            # Prep for next iteration
            next_ancil_row = rdr.next_ancillary()
        
        next_piv_row = rdr.advance_pivot()
    
    
    
