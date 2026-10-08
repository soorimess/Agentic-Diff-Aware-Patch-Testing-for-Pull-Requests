"""
Test for regression of CountVectorizer.get_feature_names behavior
when vocabulary parameter is provided.
"""

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.utils.testing import assert_raises
from sklearn.exceptions import NotFittedError


def test_count_vectorizer_get_feature_names_with_vocabulary():
    """Test that get_feature_names works when vocabulary is provided at init."""
    # Create vocabulary
    vocabulary = ['and', 'document', 'first', 'is', 'one', 'second', 'the', 'third', 'this']
    
    # Create vectorizer with vocabulary but no fitting
    vectorizer = CountVectorizer(vocabulary=vocabulary)
    
    # Verify that vocabulary_ is not set initially (this is the key condition)
    assert not hasattr(vectorizer, 'vocabulary_')
    
    # Before the fix, this would raise NotFittedError
    # After the fix, this should work and return the vocabulary
    feature_names = vectorizer.get_feature_names()
    
    # Verify we get the expected feature names (should match input vocabulary)
    expected_names = vocabulary
    assert feature_names == expected_names
    
    # Also test that transform still works
    corpus = [
        'This is the first document.',
        'This is the second second document.',
        'And the third one.',
        'Is this the first document?',
    ]
    
    # This should work in both cases
    X = vectorizer.transform(corpus)
    assert X.shape == (4, 9)


def test_count_vectorizer_get_feature_names_without_vocabulary():
    """Test that get_feature_names still raises NotFittedError when no vocabulary."""
    # Create vectorizer without vocabulary
    vectorizer = CountVectorizer()
    
    # This should still raise NotFittedError
    assert_raises(NotFittedError, vectorizer.get_feature_names)
    
    # Test that transform also raises NotFittedError
    corpus = [
        'This is the first document.',
        'This is the second second document.',
        'And the third one.',
        'Is this the first document?',
    ]
    
    assert_raises(NotFittedError, vectorizer.transform, corpus)