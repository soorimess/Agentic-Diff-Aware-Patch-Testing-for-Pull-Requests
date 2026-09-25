"""
Regression test for Django bug #14580
"""
import sys
import os

# Add Django to path
sys.path.insert(0, '/testbed')

# Run the actual assertion
from django.db.migrations.serializer import serializer_factory
from django.db import models

# Process the bug
serializer = serializer_factory(models.Model)
result, imports = serializer.serialize()

# Test: This should not fail in the "fixed" version of Django but fails in the "buggy" version
# The bug was that the imports list was empty when models.Model was serialized
if 'from django.db import models' not in imports:
    raise AssertionError("Missing import statement: from django.db import models")