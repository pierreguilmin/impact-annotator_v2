import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn
from scipy.stats import normaltest, ttest_rel

from metrics import Metrics

class Summary():
    """
    This class implements an object that holds multiple metrics and makes it easy to see compare these metrics
    → Members:
      - metrics_dict      : dictionnary with key: {metrics name} and value: {Metrics object}
      - columns_score_mean: list of strings giving the columns name for the mean metrics values
      - columns_score_std : list of strings giving the columns name for the std metrics values
      - summary           : pandas DataFrame holding the metrics mean and std accross the folds
      - scoring           : single-value scores to evaluate the metrics on
    """

    def __init__(self, scoring=Metrics.default_scoring_metrics):
        """
        Create the Summary object
        → Arguments:
            - scoring
        """
        self.metrics_dict = {}

        self.columns_score_mean = ['test_{}_mean'.format(score_name) for score_name in scoring]
        self.columns_score_std  = ['test_{}_std'.format(score_name)  for score_name in scoring]

        self.summary = pd.DataFrame(columns=self.columns_score_mean + self.columns_score_std + ['color'])
        self.summary.index.name = 'metrics_name'

        self.scoring = scoring


    def display(self, highlight_max=True):
        """
        Display the self.summary DataFrame with custom highlighting
        → Arguments:
            - highlight_max: if True highlight the cell with the maximum value for each score
        """
        if highlight_max:
            display(self.summary[self.columns_score_mean].style.highlight_max(axis=0, color='salmon').set_precision(3))
        else:
            display(self.summary)


    def add(self, metrics, metrics_name, color=False):
        """
        Add a Metrics to self.summary
        → Arguments:
            - metrics     : a Metrics object
            - metrics_name: a string representative of the Metrics object meaning
            - color       : color associated with this Metrics object
        """
        self.metrics_dict[metrics_name] = metrics
        self.summary.loc[metrics_name]  = [metrics.get_metrics()['test_{}'.format(score_name)].mean() for score_name in self.scoring] +\
                                          [metrics.get_metrics()['test_{}'.format(score_name)].std()  for score_name in self.scoring] +\
                                          [color]


    def plot(self, figsize=(25, 8), fontsize=12):
        """
        Plot a comparison of the metrics accross every score
        → Arguments:
            - figsize : the size of the figure
            - fontsize: the score text label font size
        """
        summary_transpose = self.summary.copy().transpose()

        fig, ax = plt.subplots(1, 1, figsize=figsize)

        # get mean and std metrics
        mean_metrics = summary_transpose.loc[self.columns_score_mean]
        std_metrics  = summary_transpose.loc[self.columns_score_std]
        std_metrics.index = mean_metrics.index

        # get colors
        colors = seaborn.color_palette("viridis", self.summary.shape[0])

        # if some color have been specified, replace the default colors by the specified ones
        for i, c in enumerate(self.summary['color']):
            if c:
                colors[i] = c

        # plot comparison
        mean_metrics.plot.bar(ax=ax, width=0.85, color=colors,
                               yerr=std_metrics, error_kw={'ecolor': 'black', 'capsize': 2}, linewidth=0)
            
        # print text results
        for rect in ax.patches:
            ax.text(rect.get_x() + rect.get_width() / 2, rect.get_height() + 0.01 + std_metrics.max().max(),
                    '{:.3f}'.format(rect.get_height()), ha='center', va='bottom', color=rect.get_facecolor(), fontsize=fontsize, rotation=55)

        # plot reference 1.0 value
        plt.plot(ax.get_xlim(), [1.0, 1.0], '--', alpha=0.5, linewidth=1, color='navy')

        # set plot
        xmin, xmax = ax.get_xlim()
        plt.xticks(rotation=0, fontsize=fontsize)
        plt.yticks(fontsize=fontsize)
        plt.legend(loc='center left', bbox_to_anchor=(1, 0.5), prop={'size': fontsize * 1.2})
        plt.ylim(top=1.1)


    def save(self, path):
        """
        Save self.summary to a .pkl
        → Arguments:
            - path: string specifying the path to the .pkl file
        """
        self.summary.to_pickle(path)


    def load(self, path):
        """
        Load self.summary from a .pkl
        → Arguments:
            - path: string specifying the path to the .pkl file
        """
        self.summary = pd.read_pickle(path)

        # keep only the selected scoring metrics
        self.summary = self.summary[self.columns_score_mean + self.columns_score_std + ['color']]


    # to remove
    #
    # def plot_cv_curves(self, figsize=(7, 7), scoring=None):
    #     if not scoring:
    #         scoring = self.scoring[::-1]

    #     plt.figure(figsize=(figsize[0] * len(scoring), figsize[1]))

    #     for i, score_name in enumerate(scoring):
    #         plt.subplot(1, len(scoring), i + 1)
    #         plt.title(score_name)

    #         j = 0
    #         for metrics_name, metrics in self.metrics_dict.items():
    #             metrics.get_metrics()['test_{}'.format(score_name)].plot(style='-o', linewidth=0, label=metrics_name, alpha=0.7, color=self.summary.iloc[j]['color'])
    #             j += 1

    #     plt.legend()


    def plot_2_vs_2(self, metric_x_name, metric_y_name, figsize=(40, 7), scoring=None):
        """
        Work in progress...
        """
        if not scoring:
            scoring = self.scoring

        plt.figure(figsize=figsize)

        for i, score_name in enumerate(scoring):
            plt.subplot(1, len(scoring), i + 1)
            plt.title(score_name)

            metric_x = self.metrics_dict[metric_x_name].get_metrics()['test_{}'.format(score_name)]
            metric_y = self.metrics_dict[metric_y_name].get_metrics()['test_{}'.format(score_name)]

            pvalue_is_normal_x = normaltest(metric_x).pvalue
            pvalue_is_normal_y = normaltest(metric_y).pvalue
            if pvalue_is_normal_x < 0.05 or pvalue_is_normal_y < 0.05:
                is_not_normal_warning = '\nWARNING: distribution not gaussian\np_x={:.2e} | p_y={:.2e}'.format(pvalue_is_normal_x, pvalue_is_normal_y)
            else:
                is_not_normal_warning = ''

            plt.plot(metric_x, metric_y, 'o', alpha=0.6, label='rel')
            plt.xlabel(metric_x_name)
            plt.ylabel(metric_y_name)
            

            xmin, xmax = plt.gca().get_xlim()
            ymin, ymax = plt.gca().get_ylim()
            new_min = min(xmin, ymin)
            new_max = max(xmax, ymax)
            plt.plot([new_min, new_max], [new_min, new_max])


            pvalue = ttest_rel(metric_x, metric_y).pvalue
            title = plt.title(score_name + ' (p={:.2e})'.format(pvalue) + is_not_normal_warning)
            if pvalue < 0.05: # means significantly different with a 95% confidence
                plt.setp(title, color='r', fontweight='bold', fontsize=14)
