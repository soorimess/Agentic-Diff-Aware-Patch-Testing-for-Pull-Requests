# Test for issue scikit-learn#10908
# Ensure CountVectorizer.get_feature_names does not raise when
# vocabulary is passed at initialization.

from sklearn.feature_extraction.text import CountVectorizer


def test_get_feature_names_with_vocabulary_parameter():
    """get_feature_names should work when vocabulary parameter is set.

    Before the fix for #10908, get_feature_names raised NotFittedError
    if the CountVectorizer was constructed with the ``vocabulary``
    parameter but had not been fitted or used to transform data yet.
    """
    vocabulary = ['and', 'document', 'first', 'is', 'one', 'second',
                  'the', 'third', 'this']

    vec = CountVectorizer(vocabulary=vocabulary)

    # This used to raise NotFittedError. It should return the feature names
    # in the order corresponding to the provided vocabulary.
    feature_names = vec.get_feature_names()
    assert feature_names == vocabulary
