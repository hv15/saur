from context import aur

import unittest
import os.path

class TestAurMethods (unittest.TestCase):
    def test_init_fake_path (self):
        fake_path = '/tmp/nothing/here/aur'
        self.assertRaises (FileNotFoundError, aur.Aur, config=None, aur_path=fake_path)
    def test_init_a_path (self):
        path = '/usr/bin/env'
        self.assertRaises (RuntimeError, aur.Aur, config=None, aur_path=path)
    @unittest.skipUnless (os.path.exists ('/usr/bin/aur'), "aurutils not available")
    def test_init_aur_path (self):
        path = '/usr/bin/aur'
        try:
            cls = aur.Aur (config=None, aur_path=path)
        except:
            self.assertTrue(False)
    @unittest.skipUnless (os.path.exists ('/usr/bin/aur'), "aurutils not available")
    def test_init_def (self):
        try:
            cls = aur.Aur (config=None)
        except:
            self.assertTrue(False)

if __name__ == '__main__':
    unittest.main ()
