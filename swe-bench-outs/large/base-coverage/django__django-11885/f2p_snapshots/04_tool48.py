from django.test import TestCase
from django.db import models
from django.db.models.deletion import Collector


class FastDeleteCombinationTest(TestCase):
    def test_collector_uses_defaultdict_structures(self):
        """
        Test that Collector now uses defaultdict structures for better handling
        of data, field_updates, and dependencies.
        """
        collector = Collector(using='default')
        
        # Check that data is a defaultdict (not a regular dict)
        # This verifies the structural change in the code
        self.assertTrue(hasattr(collector.data, '__missing__'), 
                       "collector.data should be a defaultdict")
        
        # Check that field_updates is a defaultdict
        self.assertTrue(hasattr(collector.field_updates, '__missing__'),
                       "collector.field_updates should be a defaultdict")
        
        # Check that dependencies is a defaultdict
        self.assertTrue(hasattr(collector.dependencies, '__missing__'),
                       "collector.dependencies should be a defaultdict")
        
    def test_collector_initialization(self):
        """
        Test that Collector is properly initialized with the correct data structures.
        """
        collector = Collector(using='default')
        
        # Verify the data structures are the right types
        # This is the core change that enables fast delete query combination
        self.assertEqual(type(collector.data).__name__, 'defaultdict')
        self.assertEqual(type(collector.field_updates).__name__, 'defaultdict') 
        self.assertEqual(type(collector.dependencies).__name__, 'defaultdict')