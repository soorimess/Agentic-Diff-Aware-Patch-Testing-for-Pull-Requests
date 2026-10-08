"""Test for regression of CountVectorizer get_feature_names behavior.

This test ensures that CountVectorizer.get_feature_names() works properly
when vocabulary is provided at initialization but the vectorizer hasn't been
fitted yet.
"""

import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.utils.testing import assert_raises


def test_countvectorizer_get_feature_names_with_vocabulary():
    """Test that get_feature_names works with vocabulary parameter without fitting."""
    # Create vocabulary as described in the bug report
    vocabulary = ['and', 'document', 'first', 'is', 'one', 'second', 'the', 'third', 'this']
    
    # Initialize vectorizer with vocabulary but no fitting
    vectorizer = CountVectorizer(vocabulary=vocabulary)
    
    # Before the fix, this would raise NotFittedError
    # After the fix, this should return the vocabulary as feature names
    feature_names = vectorizer.get_feature_names()
    
    # Should return the vocabulary in sorted order (as per the implementation)
    expected = sorted(vocabulary)
    assert feature_names == expected
    
    # Also verify that transform still works
    corpus = [
        'This is the first document.',
        'This is the second second document.',
        'And the third one.',
        'Is this the first document?',
    ]
    
    # Transform should work without prior fitting
    X = vectorizer.transform(corpus)
    assert X.shape == (4, 9)
    
    # Verify that vocabulary_ is now set after transform
    assert hasattr(vectorizer, 'vocabulary_')
    assert len(vectorizer.vocabulary_) == 9


def test_countvectorizer_get_feature_names_without_vocabulary():
    """Test that get_feature_names still raises NotFittedError without vocabulary."""
    # Initialize vectorizer without vocabulary
    vectorizer = CountVectorizer()
    
    # This should still raise NotFittedError or similar fitting-related error
    assert_raises(Exception, vectorizer.get_feature_names)
    
    # The error should be a fitting-related error
    try:
        vectorizer.get_feature_names()
    except Exception as e:
        # Should be a fitting-related error, not a ValueError or similar
        error_msg = str(e).lower()
        assert "fitted" in error_msg or "vocabulary" in error_msg or "not fitted" in error_msg