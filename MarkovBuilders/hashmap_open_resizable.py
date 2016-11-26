"""
description: open addressing Hash Map with resizing
file: hashtable_open.py
language: python3
author: sps@cs.rit.edu Sean Strout
author: anh@cs.rit.edu Arthur Nunes-Harwitt
author: jsb@cs.rit.edu Jeremy Brown
author: as@cs.rit.edu Amar Saric
author: jeh@cs.rit.edu James Heliotis
"""
from typing import Any, Hashable, Sequence

class HashMap:
    """
    This open-addressing HashMap data structure contains a list of values
    where each value is in an array 'storage' and located by a hashable key.
    When the storage fills up, a larger storage is allocated and all of the
    current entries are transferred to it. This is called 'rehashing'.
    """
    __slots__ = 'size', 'storage', 'capacity', 'collisions'

    def __init__(self: "HashMap", capacity: int = 100):
        self.size = 0
        self.storage = capacity * [None]
        self.capacity = 2 if capacity < 2 else capacity
        self.collisions = 0

    def __str__( self: "HashMap") -> str:
        result = ""
        for i in range(len(self.storage)):
            e = self.storage[i]
            if e is not None:
                result += str(i) + ": "
                if e is SKIP:
                    result += "SKIP"
                else:
                    result += str(e)
                result += "\n"
        return result


class Entry:
    """
    A class used to hold key/value pairs.
    """

    __slots__ = 'key', 'value'

    def __init__( self: "Entry", key: Hashable, value: Any ):
        self.key= key
        self.value = value

    def __str__( self ) -> str:
        return "(" + str( self.key ) + ", " + str( self.value ) + ")"

# Create an entry indicating that the search for a key should continue
# even though there is no valid entry in a certain spot due to a deletion.
# The entry must have a key that matches no other key in the program.

class _other( Hashable ):
    """For internal use only; do not instantiate."""
    def __hash__( self ): return 0
SKIP = Entry( _other(), None )

def keys( hmap ) -> Sequence[ Hashable ]:
    result = [ ]
    for entry in hmap.storage:
        if entry is not None and entry is not SKIP:
            result.append( entry.key )
    return result

def contains( hmap: HashMap, key: Hashable ) -> bool:
    index = hash_function( key ) % len( hmap.storage )
    startIndex = index  # Remember where we start.*
    while hmap.storage[ index ] is not None \
            and hmap.storage[ index ].key != key:
        index = (index + 1) % len( hmap.storage )
        if index == startIndex: # *We've gone all the way around!
            return False
    return hmap.storage[ index ] is not None

def put( hmap: HashMap, key: Hashable, value: Any ):
    if hmap.size == hmap.capacity: # It should really check for a lower value!
        _rehash( hmap )
    index = hash_function( key ) % len( hmap.storage )

    # bookkeeping
    if hmap.storage[ index ] is not None and \
            hmap.storage[ index ].key != key:
        hmap.collisions += 1

    startIndex = index
    while hmap.storage[ index ] is not None and \
            hmap.storage[ index ] is not SKIP and \
            hmap.storage[ index ].key != key:
        index = (index + 1) % len( hmap.storage )
        if index == startIndex:
            assert True, "Unexpected rehash failure"
    if hmap.storage[ index ] is None or hmap.storage[ index ] is SKIP:
        hmap.storage[ index ] = Entry( key, value )
        hmap.size += 1
    else:
        hmap.storage[ index ].value = value
    return True

def delete( hmap: HashMap, key: Hashable ):
    index = hash_function( key ) % len( hmap.storage )
    startIndex = index
    while hmap.storage[ index ] is not None and \
            hmap.storage[ index ].key != key:
        index = (index + 1) % len( hmap.storage )
        if index == startIndex:
            raise Exception( "Element to delete does not exist." )
    if hmap.storage[ index ] is None:
        raise Exception( "Element to delete does not exist." )
    else:
        hmap.storage[ index ] = SKIP
        hmap.size -= 1

def get( hmap: HashMap, key: Hashable ) -> Any:
    index = hash_function( key ) % len( hmap.storage )
    startIndex = index
    while hmap.storage[ index ] is not None and \
                    hmap.storage[ index ].key != key:
        index = ( index + 1 ) % len( hmap.storage )
        if index == startIndex:
            raise Exception( "Hash map does not contain key." )
    if hmap.storage[ index ] is None:
        raise Exception( "Hash map does not contain key:", key )
    else:
        return hmap.storage[ index ].value

def _rehash( hmap ):
    """
    Rebuild the map in a larger storage. The current map is not changed
    in any way that can be seen by its clients, but internally its storage is
    grown.
    :return: None
    """
    new_cap = 2 * hmap.capacity
    print( "Rehashing from", hmap.capacity, "to", new_cap )
    new_hmap = HashMap( new_cap )
    for key in keys( hmap ):
        put( new_hmap, key, get( hmap, key ) )
    hmap.capacity = new_hmap.capacity
    hmap.storage = new_hmap.storage

def hash_function( value: Any ) -> int:
    """
    hash_function: NatNum -> NatNum
    :parameter value: value to be hashed
    :return: an integer that represents somehow the original value
    """
    hashcode = hash( value )
    # hashcode = 0
    # hashcode = len( value )
    return hashcode
