import logging
import os
from unittest import TestCase

from bd2k.util.exceptions import panic

import cgcloud
from cgcloud.core.ui import main

log = logging.getLogger( __name__ )


class CoreTests( TestCase ):
    """
    Tests the typical life-cycle of instances and images
    """
    _multiprocess_can_split_ = True

    boxes = cgcloud.core.BOXES

    @classmethod
    def setUpClass( cls ):
        super( CoreTests, cls ).setUpClass( )
        # FIMXE: use a unique namespace for every run
        os.environ.setdefault( 'CGCLOUD_NAMESPACE', '/test/' )
        # FIXME: on EC2 detect zone automatically
        os.environ.setdefault( 'CGCLOUD_ZONE', 'us-west-2a' )

    def cgcloud( self, *args ):
        log.info( "Running %r" % (args,) )
        main( args )

    @classmethod
    def __box_test( cls, box ):
        def box_test( self ):
            ssh_opts = [ '-o', 'UserKnownHostsFile=/dev/null', '-o', 'StrictHostKeyChecking=no' ]
            role = box.role( )
            self.cgcloud( 'create', role )
            try:
                self.cgcloud( 'stop', role )
                self.cgcloud( 'image', role )
                try:
                    self.cgcloud( 'terminate', role )
                    self.cgcloud( 'recreate', role )
                    file_name = 'foo-' + role
                    self.cgcloud( *( [ 'ssh', role ] + ssh_opts + [ 'touch', file_name ] ) )
                    self.cgcloud( 'rsync', "--ssh-opts=" + ' '.join( ssh_opts ), role, ':' + file_name, '.' )
                    self.assertTrue( os.path.exists( file_name ) )
                    os.unlink( file_name )
                    self.cgcloud( 'terminate', role )
                finally:
                    self.cgcloud( 'delete-image', role )
            except:
                with panic( log ):
                    self.cgcloud( 'terminate', '-q', role )

        return box_test

    @classmethod
    def make_tests( cls ):
        for box in cls.boxes:
            test_method = cls.__box_test( box )
            test_method.__name__ = 'test_%s' % box.role( ).replace( '-', '_' )
            setattr( cls, test_method.__name__, test_method )

    def test_illegal_argument( self ):
        try:
            self.cgcloud( 'delete-image', self.boxes[ 0 ].role( ), '-1' )
            self.fail( )
        except SystemExit:
            pass


CoreTests.make_tests( )
