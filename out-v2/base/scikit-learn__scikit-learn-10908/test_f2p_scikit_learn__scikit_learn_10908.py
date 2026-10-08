"""Test for regression of CountVectorizer get_feature_names behavior.

This test ensures that get_feature_names() does not raise NotFittedError
when a vocabulary is provided at initialization but the vectorizer has not
been explicitly fitted.
"""

import pytest
from sklearn.feature_extraction.text import CountVectorizer


def test_get_feature_names_with_vocabulary_parameter():
    """Test that get_feature_names works when vocabulary is provided at init."""
    # Create vocabulary as described in the bug report
    vocabulary = ['and', 'document', 'first', 'is', 'one', 'second', 'the', 'third', 'this']
    
    # Initialize vectorizer with vocabulary but no fitting
    vectorizer = CountVectorizer(vocabulary=vocabulary)
    
    # Verify that vocabulary_ attribute is not set yet (before calling get_feature_names)
    assert not hasattr(vectorizer, 'vocabulary_')
    
    # Before the fix, this would raise NotFittedError
    # After the fix, this should work and return the vocabulary
    feature_names = vectorizer.get_feature_names()
    
    # The feature names should match the vocabulary
    assert feature_names == vocabulary
    
    # Verify that vocabulary_ attribute is now set after calling get_feature_names
    assert hasattr(vectorizer, 'vocabulary_')
    assert vectorizer.vocabulary_ is not None


def test_transform_works_with_vocabulary_parameter():
    """Test that transform works when vocabulary is provided at init."""
    vocabulary = ['and', 'document', 'first', 'is', 'one', 'second', 'the', 'third', 'this']
    corpus = [
        'This is the first document.',
        'This is the second second document.',
        'And the third one.',
        'Is this the first document?',
    ]
    
    vectorizer = CountVectorizer(vocabulary=vocabulary)
    
    # Transform should work without fitting
    result = vectorizer.transform(corpus)
    
    # Should produce a sparse matrix
    assert result.shape == (4, 9)


def test_get_feature_names_without_vocabulary_raises_error():
    """Test that get_feature_names still raises NotFittedError when no vocabulary."""
    vectorizer = CountVectorizer()
    
    # This should still raise NotFittedError
    with pytest.raises(Exception) as exc_info:
        vectorizer.get_feature_names()
    
    # The error should be about vocabulary not being fitted
    assert "Vocabulary wasn't fitted" in str(exc_info.value)


def test_vocabulary_attribute_properly_set():
    """Test that vocabulary_ attribute is properly set when get_feature_names is called."""
    vocabulary = ['and', 'document', 'first', 'is', 'one', 'second', 'the', 'third', 'this']
    
    vectorizer = CountVectorizer(vocabulary=vocabulary)
    
    # Before calling get_feature_names, vocabulary_ should not exist
    assert not hasattr(vectorizer, 'vocabulary_')
    
    # Call get_feature_names - this should set up vocabulary_
    feature_names = vectorizer.get_feature_names()
    
    # After calling get_feature_names, vocabulary_ should exist and be correct
    assert hasattr(vectorizer, 'vocabulary_')
    assert isinstance(vectorizer.vocabulary_, dict)
    assert len(vectorizer.vocabulary_) == len(vocabulary)
    
    # The vocabulary dict should contain all the vocabulary terms
    for term in vocabulary:
        assert term in vectorizer.vocabulary_


if __name__ == "__main__":
    # Run the tests
    test_get_feature_names_with_vocabulary_parameter()
    test_transform_works_with_vocabulary_parameter()
    test_get_feature_names_without_vocabulary_raises_error()
    test_vocabulary_attribute_properly_set()
    print("All tests passed!")