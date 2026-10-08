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


def test_countvectorizer_get_feature_names_with_none_vocabulary():
    """Test that get_feature_names() still raises NotFittedError with None vocabulary."""
    # Initialize vectorizer with None vocabulary
    vectorizer = CountVectorizer(vocabulary=None)
    
    # This should still raise NotFittedError
    assert_raises(Exception, vectorizer.get_feature_names)


def test_countvectorizer_get_feature_names_attribute_setup():
    """Test that get_feature_names() properly sets up vocabulary_ attribute."""
    # Create vocabulary
    vocabulary = ['and', 'document', 'first', 'is', 'one', 'second', 'the', 'third', 'this']
    
    # Initialize vectorizer with vocabulary
    vectorizer = CountVectorizer(vocabulary=vocabulary)
    
    # Before fix: calling get_feature_names() would raise NotFittedError
    # After fix: calling get_feature_names() should set up vocabulary_ and work
    feature_names = vectorizer.get_feature_names()
    
    # Verify it returns correct feature names
    assert feature_names == vocabulary
    
    # Verify that vocabulary_ attribute is now set (this is the core fix)
    assert hasattr(vectorizer, 'vocabulary_')
    assert vectorizer.vocabulary_ is not None
    assert len(vectorizer.vocabulary_) == len(vocabulary)
    assert vectorizer.vocabulary_['and'] == 0
    assert vectorizer.vocabulary_['document'] == 1


if __name__ == '__main__':
    test_countvectorizer_get_feature_names_with_vocabulary()
    test_countvectorizer_get_feature_names_without_vocabulary_raises()
    test_countvectorizer_get_feature_names_with_none_vocabulary()
    test_countvectorizer_get_feature_names_attribute_setup()
    print("All tests passed!")