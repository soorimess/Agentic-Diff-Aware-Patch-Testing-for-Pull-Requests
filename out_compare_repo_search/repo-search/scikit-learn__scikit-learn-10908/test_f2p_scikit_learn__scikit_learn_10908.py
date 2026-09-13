from __future__ import unicode_literals

from sklearn.feature_extraction.text import CountVectorizer


def test_get_feature_names_with_provided_vocabulary():
    """CountVectorizer.get_feature_names should work when vocabulary is
    provided at construction time (no prior fit/transform required).

    Regression test for scikit-learn#10908: get_feature_names previously
    raised NotFittedError when ``vocabulary`` parameter was given.
    """
    vocab = ['and', 'document', 'first', 'is', 'one', 'second', 'the', 'third', 'this']

    vect = CountVectorizer(vocabulary=vocab)

    # Before calling get_feature_names the fitted attribute shouldn't exist
    assert not hasattr(vect, 'vocabulary_')

    # This should not raise and should return the feature names in the
    # order corresponding to the provided vocabulary.
    feature_names = vect.get_feature_names()
    assert feature_names == vocab

    # After the call the fitted attribute must be set
    assert hasattr(vect, 'vocabulary_')
    # And the mapping should be consistent with the original vocabulary
    assert vect.vocabulary_['first'] == vocab.index('first')
