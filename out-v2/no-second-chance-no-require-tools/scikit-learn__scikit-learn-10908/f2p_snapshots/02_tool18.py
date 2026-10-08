"""Test for regression of bug where CountVectorizer.get_feature_names raises 
NotFittedError when vocabulary parameter is provided."""

import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.exceptions import NotFittedError


def test_countvectorizer_get_feature_names_with_vocabulary():
    """Test that get_feature_names works when vocabulary is provided at init."""
    # Create vocabulary
    vocabulary = ['and', 'document', 'first', 'is', 'one', 'second', 'the', 'third', 'this']
    
    # Create vectorizer with vocabulary (but no training)
    vectorizer = CountVectorizer(vocabulary=vocabulary)
    
    # This should not raise NotFittedError after the fix
    feature_names = vectorizer.get_feature_names()
    
    # Verify we get the expected feature names
    expected_names = ['and', 'document', 'first', 'is', 'one', 'second', 'the', 'third', 'this']
    assert feature_names == expected_names


def test_countvectorizer_transform_with_vocabulary():
    """Test that transform works when vocabulary is provided at init (control test)."""
    # Create vocabulary
    vocabulary = ['and', 'document', 'first', 'is', 'one', 'second', 'the', 'third', 'this']
    
    # Create corpus
    corpus = [
        'This is the first document.',
        'This is the second second document.',
        'And the third one.',
        'Is this the first document?',
    ]
    
    # Create vectorizer with vocabulary (but no training)
    vectorizer = CountVectorizer(vocabulary=vocabulary)
    
    # Transform should work (this was already working)
    X = vectorizer.transform(corpus)
    
    # Verify we get a sparse matrix
    assert X.shape == (4, 9)
    assert X.nnz > 0


def test_countvectorizer_get_feature_names_without_vocabulary_raises():
    """Test that get_feature_names still raises NotFittedError when no vocabulary."""
    # Create vectorizer without vocabulary
    vectorizer = CountVectorizer()
    
    # This should still raise NotFittedError
    try:
        vectorizer.get_feature_names()
        assert False, "Should have raised NotFittedError"
    except NotFittedError:
        pass  # Expected


def test_countvectorizer_get_feature_names_after_fit():
    """Test that get_feature_names works after fitting."""
    # Create corpus
    corpus = [
        'This is the first document.',
        'This is the second second document.',
        'And the third one.',
        'Is this the first document?',
    ]
    
    # Create vectorizer and fit it
    vectorizer = CountVectorizer()
    vectorizer.fit(corpus)
    
    # This should work
    feature_names = vectorizer.get_feature_names()
    
    # Verify we get some feature names
    assert len(feature_names) > 0