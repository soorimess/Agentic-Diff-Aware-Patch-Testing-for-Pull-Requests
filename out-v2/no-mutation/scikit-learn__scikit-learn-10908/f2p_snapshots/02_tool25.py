"""Test for regression of CountVectorizer get_feature_names behavior.

This test ensures that CountVectorizer.get_feature_names() does not raise
NotFittedError when vocabulary parameter is provided but the vectorizer
has not been fitted.
"""

import pytest
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.exceptions import NotFittedError


def test_countvectorizer_get_feature_names_with_vocabulary():
    """Test that get_feature_names works when vocabulary is provided but not fitted."""
    # Create a vocabulary
    vocabulary = ['and', 'document', 'first', 'is', 'one', 'second', 'the', 'third', 'this']
    
    # Initialize CountVectorizer with vocabulary but without fitting
    vectorizer = CountVectorizer(vocabulary=vocabulary)
    
    # Check that vocabulary_ is not set yet (not fitted)
    assert not hasattr(vectorizer, 'vocabulary_')
    
    # This should NOT raise NotFittedError - the bug was that it did
    feature_names = vectorizer.get_feature_names()
    
    # Check that we get the expected feature names
    expected_names = vocabulary
    assert feature_names == expected_names
    
    # Transform should still work
    corpus = [
        'This is the first document.',
        'This is the second second document.',
        'And the third one.',
        'Is this the first document?',
    ]
    
    # This should work without fitting
    X = vectorizer.transform(corpus)
    assert X.shape == (4, 9)
    
    # Now check that vocabulary_ is set after transform
    assert hasattr(vectorizer, 'vocabulary_')


def test_countvectorizer_get_feature_names_without_vocabulary():
    """Test that get_feature_names still raises NotFittedError when no vocabulary."""
    vectorizer = CountVectorizer()
    
    # This SHOULD raise NotFittedError
    with pytest.raises(NotFittedError):
        vectorizer.get_feature_names()