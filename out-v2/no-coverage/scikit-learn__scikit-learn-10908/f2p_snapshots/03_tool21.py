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
    
    # Verify that vocabulary_ attribute is now set
    assert hasattr(vectorizer, 'vocabulary_')
    assert len(vectorizer.vocabulary_) == len(vocabulary)
    assert vectorizer.vocabulary_['and'] == 0
    assert vectorizer.vocabulary_['document'] == 1


def test_countvectorizer_get_feature_names_without_vocabulary_raises():
    """Test that get_feature_names() still raises NotFittedError when no vocabulary."""
    # Initialize vectorizer without vocabulary
    vectorizer = CountVectorizer()
    
    # This should still raise NotFittedError
    assert_raises(Exception, vectorizer.get_feature_names)


def test_countvectorizer_get_feature_names_with_none_vocabulary():
    """Test that get_feature_names() still raises NotFittedError with None vocabulary."""
    # Initialize vectorizer with None vocabulary
    vectorizer = CountVectorizer(vocabulary=None)
    
    # This should still raise NotFittedError
    assert_raises(Exception, vectorizer.get_feature_names)


def test_countvectorizer_get_feature_names_idempotent():
    """Test that calling get_feature_names() multiple times works correctly."""
    # Create vocabulary
    vocabulary = ['and', 'document', 'first', 'is', 'one', 'second', 'the', 'third', 'this']
    
    # Initialize vectorizer with vocabulary
    vectorizer = CountVectorizer(vocabulary=vocabulary)
    
    # Call get_feature_names multiple times - should work consistently
    feature_names1 = vectorizer.get_feature_names()
    feature_names2 = vectorizer.get_feature_names()
    
    assert feature_names1 == feature_names2
    assert feature_names1 == vocabulary


if __name__ == '__main__':
    test_countvectorizer_get_feature_names_with_vocabulary()
    test_countvectorizer_get_feature_names_without_vocabulary_raises()
    test_countvectorizer_get_feature_names_with_none_vocabulary()
    test_countvectorizer_get_feature_names_idempotent()
    print("All tests passed!")