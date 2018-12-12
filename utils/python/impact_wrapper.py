import numpy as np
import pandas as pd
from custom_tools import get_table

# work in progress...
class Impact_Wrapper():
    """
    This class is a wrapper of the IMPACT dataset to make sure to have a reproducible and flexible way to process the dataset
    → Members:
      - impact               : raw impact dataset
      - label                : name of the label to predict
      - categorical_features : name of the categorical features to process
      - impact_processed     : impact dataset after features selection and processing
      - positive_class_number: number of positive sample
      - negative_class_number: number of negative sample
      - impact_selected      : impact dataset after sample selection
      - selected_indexes     : index selected during the sample selection
      - second_permutation   : the permutation applied to the samples selected
    """

    original_categorical_features = ['Hugo_Symbol', 'Chromosome', 'Consequence', 'Variant_Type', 'Reference_Allele', 'Tumor_Seq_Allele2',
                                     'Tumor_Sample_Barcode', 'cDNA_change', 'HGVSp_Short', 'confidence_class', 'mut_key',
                                     'VAG_VT', 'VAG_GENE', 'VAG_cDNA_CHANGE', 'VAG_PROTEIN_CHANGE', 'VAG_EFFECT',
                                     'VEP_Consequence', 'VEP_SYMBOL', 'VEP_HGVSc', 'VEP_HGVSp', 'VEP_Amino_acids', 'VEP_VARIANT_CLASS',
                                     'VEP_EXON', 'VEP_INTRON', 'VEP_IMPACT', 'VEP_CLIN_SIG',
                                     'sample_mut_key', 'patient_key', 'VEP_SIFT_class', 'VEP_PolyPhen_class', 'VEP_in_dbSNP',
                                     'is_a_hotspot', 'is_a_3d_hotspot', 'oncogenic', 'gene_type']


    def __init__(self, path, label, shuffle=True):
        """
        Create the Impact_Wrapper object
        → Arguments:
            - path   : path to impact dataset
            - label  : name of the label to predict
            - shuffle: if True shuffle the raw dataset
        """

        self.impact = pd.read_csv(path, sep='\t', low_memory=False)
        self.label = label

        # shuffle data
        if shuffle:
            # apply a permutation to self.impact
            rng = np.random.RandomState(42)
            self.first_permutation = rng.permutation(len(self.impact))
            self.impact = self.impact.iloc[self.first_permutation]
            # reset the index to [0, 1, ...]
            self.impact.reset_index(drop=True, inplace=True)

        # create the 'is_artefact' feature
        self.impact['is_artefact'] = (self.impact['confidence_class'] == "UNLIKELY")

        # create the 'is_driver' feature
        self.impact['is_driver'] = (self.impact['oncogenic'].isin(['Likely Oncogenic', 'Oncogenic', 'Predicted Oncogenic']))

        if label == 'is_driver':
            self.impact = self.impact[~self.impact['is_artefact']]
            self.impact.reset_index(drop=True, inplace=True)

        # default categorical features
        self.categorical_features = Impact_Wrapper.original_categorical_features


    def add_features(self, feature_name, feature_values, is_categorical):
        """
        Add a feature to self.impact
        → Arguments:
            - feature_name  : name of the feature
            - feature_values: features value, as a Serie or np.array or list
            - is_categorical: if True the feature will be processed as categorical
        """
        self.impact[feature_name] = feature_values
        if is_categorical:
            self.categorical_features.append(feature_name)


    def process(self, features):
        """
        Select and process the features
        → Arguments:
            - features: list of selected features
        """
        # copy self.impact and keep only selected features
        self.impact_processed = self.impact.copy()[features + [self.label]]

        # transform categorical features to dummy features
        categorical_features = [f for f in self.categorical_features if f in features]
        self.impact_processed = pd.get_dummies(self.impact_processed, columns=categorical_features, sparse=True)

        # compute some metrics
        self.positive_class_number = self.impact_processed[ self.impact_processed[self.label]].shape[0]
        self.negative_class_number = self.impact_processed[~self.impact_processed[self.label]].shape[0]

        return self


    def get_X_and_y(self, positive_class_index, negative_class_index, shuffle=True):
        """
        Return the ready-for-classification features matrix X and target array y
        → Arguments:
            - positive_class_index: index to select in the positive class, if 'all' the whole positive class is selected
            - negative_class_index: index to select in the negative class, if 'all' the whole negative class is selected
            - shuffle: if True shuffle the dataset between positive and negative after selection
        """
        # get selected dataset
        if positive_class_index == 'all':
            positive_class_index = range(self.positive_class_number)
        if negative_class_index == 'all':
            negative_class_index = range(self.negative_class_number)
        self.impact_selected = pd.concat([self.impact_processed[ self.impact_processed[self.label]].iloc[positive_class_index],
                                          self.impact_processed[~self.impact_processed[self.label]].iloc[negative_class_index]],
                                          ignore_index=False)
        self.selected_indexes = self.impact_selected.index

        # shuffle
        if shuffle:
            # apply a permutation to self.impact_selected
            rng = np.random.RandomState(42)
            permutation = rng.permutation(len(self.impact_selected))
            self.impact_selected = self.impact_selected.iloc[permutation]
            self.second_permutation = permutation

        # get features matrix X (n_samples x n_features) and target array y (n_samples)
        X = self.impact_selected.drop(self.label, axis=1)
        X = X.astype(float)
        y = self.impact_selected[self.label]

        return X, y


    def get_original_impact(self):
        """
        Return the impact rows corresponding to the rows selected by get_X_and_y() in the same order
        """
        return self.impact.loc[self.selected_indexes[self.second_permutation]]


    def print_info(X, y):
        """
        Display shape and proportion information on X and y
        → Arguments:
            - X
            - y
        """
        print('X: {} | y: {}'.format(X.shape, y.shape))
        display(get_table(y))
