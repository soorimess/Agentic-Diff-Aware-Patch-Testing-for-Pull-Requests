from sklearn.feature_extraction.text import CountVectorizer


def test_get_feature_names_with_vocabulary_does_not_require_fit():
    """get_feature_names should work when ``vocabulary`` is provided.

    Regression test for issue #10908: calling ``get_feature_names`` on a
    CountVectorizer that was constructed with an explicit ``vocabulary``
    must not raise NotFittedError and must return the feature names in the
    correct order without requiring a prior call to fit/transform.
    """
    vocabulary = ['and', 'document', 'first', 'is', 'one', 'second',
                  'the', 'third', 'this']

    vec = CountVectorizer(vocabulary=vocabulary)
    # vocab should not be set as an attribute until validated
    assert not hasattr(vec, 'vocabulary_')

    # This must NOT raise. It should return the feature names in order.
    feature_names = vec.get_feature_names()
    assert feature_names == vocabulary

    # Calling get_feature_names should have set vocabulary_
    assert hasattr(vec, 'vocabulary_')

    # Transform should also work without explicit fit
    corpus = [
        'This is the first document.',
        'This is the second second document.',
        'And the third one.',
        'Is this the first document?',
    ]
    X = vec.transform(corpus)
    assert X.shape == (4, len(vocabulary))
    # The example in the original report had 19 stored elements
    assert getattr(X, 'nnz', None) == 19
