"""Test for regression of CountVectorizer get_feature_names behavior.

This test ensures that CountVectorizer.get_feature_names() does not raise
NotFittedError when vocabulary parameter is provided but vectorizer has not been
trained.
"""

import pytest
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.utils.estimator_checks import check_estimator


def test_countvectorizer_get_feature_names_with_vocabulary():
    """Test that get_feature_names works with provided vocabulary without fitting."""
    # Create vocabulary as described in the bug report
    vocabulary = ['and', 'document', 'first', 'is', 'one', 'second', 'the', 'third', 'this']
    
    # Initialize CountVectorizer with vocabulary but without fitting
    vectorizer = CountVectorizer(vocabulary=vocabulary)
    
    # Verify that vocabulary_ is not set yet (not fitted)
    assert not hasattr(vectorizer, 'vocabulary_')
    
    # This should NOT raise NotFittedError after the fix
    # Before the fix, this would raise: NotFittedError: CountVectorizer - Vocabulary wasn't fitted.
    feature_names = vectorizer.get_feature_names()
    
    # Verify we get the expected feature names
    expected_names = ['and', 'document', 'first', 'is', 'one', 'second', 'the', 'third', 'this']
    assert feature_names == expected_names
    
    # Verify that transform still works
    corpus = [
        'This is the first document.',
        'This is the second second document.',
        'And the third one.',
        'Is this the first document?',
    ]
    
    # Transform should work without fitting
    X = vectorizer.transform(corpus)
    assert X.shape == (4, 9)
    
    # After transform, vocabulary_ should be set
    assert hasattr(vectorizer, 'vocabulary_')


def test_countvectorizer_get_feature_names_without_vocabulary():
    """Test that get_feature_names still raises NotFittedError without vocabulary."""
    # Initialize CountVectorizer without vocabulary
    vectorizer = CountVectorizer()
    
    # This should still raise NotFittedError
    with pytest.raises(Exception) as exc_info:
        vectorizer.get_feature_names()
    
    # The error message should contain "Vocabulary wasn't fitted"
    assert "Vocabulary wasn't fitted" in str(exc_info.value)


def test_countvectorizer_get_feature_names_after_fitting():
    """Test that get_feature_names works after normal fitting."""
    # Create vocabulary as described in the bug report
    vocabulary = ['and', 'document', 'first', 'is', 'one', 'second', 'the', 'third', 'this']
    
    # Initialize CountVectorizer with vocabulary
    vectorizer = CountVectorizer(vocabulary=vocabulary)
    
    # Fit the vectorizer with some data
    corpus = [
        'This is the first document.',
        'This is the second second document.',
        'And the third one.',
        'Is this the first document?',
    ]
    
    # Fit the vectorizer
    vectorizer.fit(corpus)
    
    # This should work after fitting
    feature_names = vectorizer.get_feature_names()
    
    # Verify we get the expected feature names
    expected_names = ['and', 'document', 'first', 'is', 'one', 'second', 'the', 'third', 'this']
    assert feature_names == expected_names