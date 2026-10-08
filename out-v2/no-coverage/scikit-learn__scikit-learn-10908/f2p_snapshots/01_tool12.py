"""
Test for regression of CountVectorizer.get_feature_names() behavior
when vocabulary is provided at initialization.
"""
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.utils.testing import assert_raises


def test_countvectorizer_get_feature_names_with_vocabulary():
    """Test that get_feature_names() works when vocabulary is provided at init."""
    # Create vocabulary
    vocabulary = ['and', 'document', 'first', 'is', 'one', 'second', 'the', 'third', 'this']
    
    # Initialize vectorizer with vocabulary (no training needed)
    vectorizer = CountVectorizer(vocabulary=vocabulary)
    
    # Before the fix, this would raise NotFittedError
    # After the fix, this should work and return the vocabulary
    feature_names = vectorizer.get_feature_names()
    
    # Verify we get the expected feature names
    expected = vocabulary
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
    
    # Should produce a sparse matrix
    assert X.shape == (4, 9)
    assert X.nnz > 0


def test_countvectorizer_get_feature_names_without_vocabulary_raises():
    """Test that get_feature_names() still raises NotFittedError when no vocabulary."""
    # Initialize vectorizer without vocabulary
    vectorizer = CountVectorizer()
    
    # This should still raise NotFittedError
    assert_raises(Exception, vectorizer.get_feature_names)


if __name__ == '__main__':
    test_countvectorizer_get_feature_names_with_vocabulary()
    test_countvectorizer_get_feature_names_without_vocabulary_raises()
    print("All tests passed!")