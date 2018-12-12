import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as seaborn

from sklearn.metrics import roc_curve, precision_recall_curve, confusion_matrix
from sklearn.model_selection import cross_validate, learning_curve
import time
from custom_tools import *

class Metrics():
    """
    This class implements a cross-validation experiment and the handling/displaying of all the associated metrics
    → Members:
      - scoring        : single-value scores to compute for each fold
      - number_of_folds: number of fold of the cross-validation
      - metrics        : pandas DataFrame of size number_of_folds x number_of_metrics, holds all the relevant metrics for each fold, the columns are:
            - fit_time, score_time                 : time to fit/score in seconds
            - estimator                            : model fitted on the train test
            - train_<score_name>, test_<score_name>: train and test single-value scores
            - gs_best_parameters, gs_cv_results    : holds grid-search metrics if one was performed, NA otherwise
            - y_test                               : the y array of the test test
            - y_proba_pred, y_class_pred           : the predicted probability and class for each entry of y_test
            - test_fpr, test_tpr, roc_thresh       : metrics to plot roc curve
            - precision, recall, pr_thresh         : metrics to plot precision-recall curve
      - model          : sklearn model
      - groups         : data groups array if they exist
      - X              : features matrix of size n_samples x n_features
      - y              : target array of size n_samples
      - cv_strategy    : sklearn cross-validation strategy
      - n_jobs         : number of jobs
      - lc_train_sizes, lc_train_scores, lc_test_scores: only if get_learning_curves_metrics() is called, stores the learning curves metrics
    """

    default_scoring_metrics = ['average_precision', 'roc_auc', 'precision', 'recall', 'f1', 'accuracy']

    def __init__(self, model=None, X=None, y=None, cv_strategy=None, groups=None, scoring=default_scoring_metrics, n_jobs=1,
                 run_model=True, read_from_pkl=False, path=None):
        """
        Create the Metrics object
        → Arguments:
            - model        : can be a pipeline object
            - X
            - y
            - cv_strategy
            - groups       : can be left to None if cv_strategy doesn't implement GroupFold or similar
            - scoring
            - n_jobs
            - run_model    : if set to False, doesn't run the model
            - read_from_pkl: if set to True, read the metrics from a .pkl
            - path         : path to the .pkl if read_from_pkl is True
        """

        self.scoring = scoring

        if not read_from_pkl:
            self.number_of_folds = cv_strategy.get_n_splits()

            # create the metrics DataFrame
            self.metrics = pd.DataFrame(index=range(self.number_of_folds),
                                        columns=['fit_time', 'score_time', 'estimator'] +
                                                ['train_{}'.format(score_name) for score_name in self.scoring] +
                                                ['test_{}'.format(score_name)  for score_name in self.scoring] +
                                                ['gs_best_parameters', 'gs_cv_results'] + 
                                                ['y_test', 'y_proba_pred', 'y_class_pred',
                                                 'test_fpr', 'test_tpr', 'roc_thresh',
                                                 'precision', 'recall', 'pr_thresh'])
            self.metrics.index.name = 'fold_number'

            self.model       = model
            self.X           = X
            self.y           = y
            self.cv_strategy = cv_strategy
            self.groups      = groups
            self.n_jobs      = n_jobs

            if run_model:
                self.run_model()
        else:
            self.metrics = pd.read_pickle(path)
            self.number_of_folds = self.metrics.shape[0]


    def display(self):
        """
        Display the self.metrics DataFrame
        """
        display(self.metrics)


    def get_metrics(self):
        """
        Return the self.metrics DataFrame
        """
        return self.metrics


    def save(self, path='metrics.pkl'):
        """
        Save self.metrics to a .pkl
        → Arguments:
            - path: string specifying the path to the .pkl file
        """
        self.metrics.to_pickle(path)


    def run_model(self):
        """
        Run the model and evaluate all the metrics values to fill the self.metrics DataFrame
        """
        print('Run model...', end='')
        start = time.time()

        # get cross validation metrics
        results = cross_validate(self.model, self.X, self.y, groups=self.groups, cv=self.cv_strategy, scoring=self.scoring,
                                 return_train_score=True, return_estimator=True, n_jobs=self.n_jobs, error_score='raise')
        self.metrics.update(pd.DataFrame(results))

        # get grid search metrics if the model have performed a grid search
        if hasattr(self.metrics.iloc[0]['estimator'], 'best_params_'):
            self.metrics['gs_best_parameters'] = self.metrics['estimator'].apply(lambda x: x.best_params_)
            self.metrics['gs_cv_results']      = self.metrics['estimator'].apply(lambda x: x.cv_results_)

        # get ROC curve, PR curve and confusion matrix metrics
        # WARNING: this implies re-testing the fitted model on the test folds
        self._get_other_metrics()

        # we remove the estimators from the metrics because they can be quite memory-expensive (for random forest with a lot of trees for example)
        self.metrics.drop('estimator', axis=1, inplace=True)

        print(' done! ({:.2f}s)'.format(time.time() - start))
    

    def _get_other_metrics(self):
        """
        Compute the ROC curve, PR curve as well as the predicted probability and class arrays
        """
        # for each fold
        for i, (train_index, test_index) in enumerate(self.cv_strategy.split(self.X, self.y, groups=self.groups)):
            (X_train, X_test) = (self.X.iloc[train_index], self.X.iloc[test_index])
            (y_train, y_test) = (self.y.iloc[train_index], self.y.iloc[test_index])

            fold_metrics = self.metrics.iloc[i].copy(deep=False)
            
            # prediction metrics
            fold_metrics['y_test']       = y_test.values
            fold_metrics['y_proba_pred'] = fold_metrics['estimator'].predict_proba(X_test)[:,1]
            fold_metrics['y_class_pred'] = fold_metrics['estimator'].predict(X_test)

            # ROC metrics
            fpr, tpr, roc_thresholds = roc_curve(fold_metrics['y_test'], fold_metrics['y_proba_pred'])
            fold_metrics['test_fpr']   = fpr
            fold_metrics['test_tpr']   = tpr
            fold_metrics['roc_thresh'] = roc_thresholds

            # precision-recall metrics
            precision, recall, pr_thresholds = precision_recall_curve(fold_metrics['y_test'], fold_metrics['y_proba_pred'])
            fold_metrics['precision'] = precision
            fold_metrics['recall']    = recall
            fold_metrics['pr_thresh'] = pr_thresholds


    def print_mean(self):
        """
        Print the test set mean score and std deviation for each single-value score
        """
        for score_name in self.scoring:
            test_scores = self.metrics['test_{}'.format(score_name)]
            print('▴ Mean {:17}: {:.3f} ± {:.3f}'.format(score_name, test_scores.mean(), test_scores.std()))


    def print_fold_details(self, detailed_grid_search_metrics=False):
        """
        For each fold, print the test set score and std deviation for each single-value score, also print grid search metrics if they exist
        → Arguments:
            - detailed_grid_search_metrics: if True print detailed grid search metrics for each fold and for each set of hyperparameters
        """
        
        # the boolean grid_search is True if the self.metrics DataFrame contains grid search metrics
        grid_search = not pd.isnull(self.metrics.iloc[0]['gs_best_parameters'])

        # Print standard output format
        print('Fold #: [fit_time | score_time]')
        print('  → score_name_1: [test_score_1 | train_score_1]')
        print('  → score_name_2: [test_score_2 | train_score_2]')
        print('  → ...')

        if grid_search:
            print('  → best hyperparameters: {\'hyperparameter_name_1\': best_value, ...}')

            if detailed_grid_search_metrics:
                print('     - mean_test_score ± std_test_score for {hyperparameters_set #1}')
                print('     - mean_test_score ± std_test_score for {hyperparameters_set #2}')
                print('     - ...')

        print()

        # for each fold
        for i, fold_metrics in self.metrics.iterrows():
            print('Fold {}: [{:.2f}s | {:.2f}s]'.format(i + 1, fold_metrics.fit_time, fold_metrics.score_time))

            for score_name in self.scoring:
                print('  → {:17}: [{:.3f} | {:.3f}]'.format(score_name, fold_metrics['test_{}'.format(score_name)], fold_metrics['train_{}'.format(score_name)]))

            if grid_search:
                print('  → best hyperparameters: {}'.format(fold_metrics['gs_best_parameters']))

                if detailed_grid_search_metrics:
                    for mean, std, param in zip(fold_metrics.gs_cv_results['mean_test_score'],
                                                fold_metrics.gs_cv_results['std_test_score'],
                                                fold_metrics.gs_cv_results['params']):
                        print('     - {:.3f} ± {:.3f} for {}'.format(mean, std, param))


    def plot_threshold_decision_curves(self, figsize=(30, 10), plot_thresholds=True, show_folds_legend=True):
        """
        Plot ROC curve, PR curve and predicted probability distribution side-by-side
        → Arguments:
            - figsize          : global figure size
            - plot_thresholds  : for the ROC and PR curve, if True plot the thresholds curve for each fold
            - show_folds_legend: for the ROC and PR curve, if True show the legend for each fold curve
        """
        fig, ax = plt.subplots(1, 3, figsize=figsize)

        fontsize = figsize[0] / 3 * 1.5

        self.plot_roc(ax[0], fontsize, plot_thresholds, show_folds_legend)
        self.plot_precision_recall(ax[1], fontsize, plot_thresholds, show_folds_legend)
        self.plot_probability_distribution(ax[2], fontsize)


    def plot_roc(self, ax, fontsize, plot_thresholds=True, show_folds_legend=True):
        """
        Plot ROC curve for each fold (and the associated threshold) and a mean interpolated ROC curve
        Strongly inspired by http://scikit-learn.org/stable/auto_examples/model_selection/plot_roc_crossval.html
        → Arguments:
            - ax               : matplotlib axis object
            - fontsize        : size of the legend
            - plot_thresholds  : if True plot the thresholds curve for each fold
            - show_folds_legend: if True show the legend for each fold curve
        """
        # set plot
        ax.set_title('ROC curve for {} folds'.format(self.number_of_folds), fontsize=fontsize)
        ax.set_xlabel('false positive rate', fontsize=fontsize)
        if plot_thresholds:
            ax.set_ylabel('true positive rate  |  threshold value', fontsize=fontsize)
        else:
            ax.set_ylabel('true positive rate', fontsize=fontsize)
        ax.set_xlim(-0.05, 1.05)
        ax.set_ylim(-0.05, 1.05)
        
        mean_fpr = np.linspace(0, 1, 101) # [0, 0.01, 0.02, ..., 0.09, 1.0]
        tprs = [] # true positive rate list for each fold

        # for each fold
        for i, fold_metrics in self.metrics.iterrows():
            fpr, tpr, thresholds = fold_metrics['test_fpr'], fold_metrics['test_tpr'], fold_metrics['roc_thresh']

            # because the length of fpr and tpr vary with the fold (size of thresholds  = nunique(y_pred[:, 1]) + 1), we can't just do
            # fprs.append(fpr) and tprs.append(tpr)
            # we use a linear interpolation to find the values of fpr for a 101 chosen tpr values (mean_fpr)
            tprs.append(np.interp(mean_fpr, fpr, tpr))
            tprs[-1][0] = 0.0 # threshold > 1 for the first point (ie the last tpr value, we correct the interpolation)

            # plot ROC curve
            if show_folds_legend:
                label = 'ROC fold %d (AUC = %0.3f)' % (i + 1, fold_metrics['test_roc_auc'])
            else:
                label = None
            plt = ax.plot(fpr, tpr, linewidth=0.6, alpha=0.4, label=label)

            # plot thresholds
            if plot_thresholds:
                thresholds[0] = 1.001 # value is > 1, we set it just above one for the graphic style
                ax.plot(fpr, thresholds, linewidth=0.6, alpha=0.4, color=plt[0].get_color())
        

        # plot baseline
        ax.plot([0, 1], [0, 1], '--r', linewidth=0.5, alpha=1, label='random')

        # plot mean ROC
        mean_tpr = np.mean(tprs, axis=0)
        ax.plot(mean_fpr, mean_tpr, 'b', linewidth=2,
                label='mean ROC (AUC = {:.3f} ± {:.3f})'.format(self.metrics['test_roc_auc'].mean(), self.metrics['test_roc_auc'].std()))

        # plot mean ROC std
        std_tpr = np.std(tprs, axis=0)
        ax.fill_between(mean_fpr, mean_tpr - std_tpr, mean_tpr + std_tpr, color='blue', alpha=0.15,
                         label='mean ROC ± 1 std. dev.')

        #plt.tick_params(labelsize=20)
        ax.xaxis.set_tick_params(labelsize=fontsize)
        ax.yaxis.set_tick_params(labelsize=fontsize)

        ax.legend(loc='lower right', prop={'size': fontsize})


    def plot_precision_recall(self, ax, fontsize, plot_thresholds=True, show_folds_legend=True):
        """
        Plot Precision-Recall curve (PR) for each fold (and the associated threshold) and a mean PR curve
        Strongly inspired by self.plot_roc() method
        See https://classeval.wordpress.com/introduction/introduction-to-the-precision-recall-plot/
        WARNING: for simplicity we use linear interpolation but this is wrong (cf. previous website)
        → Arguments:
            - ax               : matplotlib axis object
            - fontsize         : size of the legend
            - plot_thresholds  : if True plot the thresholds curve for each fold
            - show_folds_legend: if True show the legend for each fold curve
        """

        # set plot
        ax.set_title('Precision-Recall curve for {} folds'.format(self.number_of_folds), fontsize=fontsize)
        ax.set_xlabel('recall', fontsize=fontsize)
        if plot_thresholds:
            ax.set_ylabel('precision  |  threshold value', fontsize=fontsize)
        else:
            ax.set_ylabel('precision', fontsize=fontsize)
        ax.set_xlim(-0.05, 1.05)
        ax.set_ylim(-0.05, 1.05)
        ax.xaxis.set_tick_params(labelsize=fontsize)
        ax.yaxis.set_tick_params(labelsize=fontsize)
        
        mean_recall = np.linspace(0, 1, 101) # [0, 0.01, 0.02, ..., 0.09, 1.0]
        precisions = [] # precision value list for each fold

        # for each fold
        for i, fold_metrics in self.metrics.iterrows():
            precision, recall, thresholds = fold_metrics['precision'], fold_metrics['recall'], fold_metrics['pr_thresh']
            
            # correct first point precision to make a horizontal line between first and second point
            # from the sklearn documentation: "The last precision and recall values are 1. and 0. respectively and do not have a corresponding
            # threshold. This ensures that the graph starts on the y axis."
            # this methodology is advised by the website quoted in the main method comment
            precision[-1] = precision[-2]

            # because the length of precision and recall vary with the fold (size of thresholds  = nunique(y_pred[:, 1]) + 1), we can't just do
            # precisions.append(precision) and recalls.append(recall)
            # we use a linear interpolation to find the values of precision for a 101 chosen recall values
            # WARNING: this is wrong, this choice has been made for simplicity
            # Also, the documentation for np.interp asks the coordinates where we want to interpolate the values to be sorted, these explains the need to do [::-1]
            # for both recall and precision
            precisions.append(np.interp(mean_recall, recall[::-1], precision[::-1]))

            # plot PR curve
            if show_folds_legend:
                label = 'PR fold %d (AP = %0.3f)' % (i + 1, fold_metrics['test_average_precision'])
            else:
                label = None
            plt = ax.plot(recall, precision, linewidth=0.6, alpha=0.4, label=label)

            # plot thresholds
            if plot_thresholds:
                # cf last comment on sklearn documentation, there's no threshold for the first point so we don't plot it
                ax.plot(recall[:-1], thresholds, linewidth=0.6, alpha=0.4, color=plt[0].get_color())
            
        # plot baseline (see website)
        positive_number = self.metrics['y_test'].apply(lambda x: sum(x)).sum()
        negative_number = self.metrics['y_test'].apply(lambda x: sum(~x)).sum()
        positive_proportion = positive_number / (positive_number + negative_number)
        ax.plot([0, 1], [positive_proportion, positive_proportion], '--r', linewidth=0.5, alpha=1, label='random')
 
        # plot mean PR
        mean_precision = np.mean(precisions, axis=0)
        ax.plot(mean_recall, mean_precision, 'b', linewidth=2,
                label='mean PR (AP = {:.3f} ± {:.3f})'.format(self.metrics['test_average_precision'].mean(), self.metrics['test_average_precision'].std()))

        # plot mean PR std
        std_precision = np.std(precisions, axis=0)
        ax.fill_between(mean_recall, mean_precision - std_precision, mean_precision + std_precision, color='blue', alpha=0.15,
                         label='mean PR ± 1 std. dev.')


        ax.legend(loc='lower left', prop={'size': fontsize})


    def plot_probability_distribution(self, ax, fontsize):
        """
        Plot predicted probability distribution for True and False class
        → Arguments:
            - ax         : matplotlib axis object
            - fontsize   : size of the legend
        """
        # concatenate all y_test and y_predicted list from each fold amd make a DataFrame
        dd = pd.DataFrame({'true_class': unlist(self.metrics['y_test']), 'predicted_probability': unlist(self.metrics['y_proba_pred'])})

        # plot predicted probability by class
        seaborn.distplot(dd[dd['true_class'] == True]['predicted_probability'], bins=100,
                         ax=ax, label='artefact', color='blue',
                         kde_kws={'bw': 0.01, 'alpha': 1},
                         hist_kws={'alpha': 0.2})
        seaborn.distplot(dd[dd['true_class'] == False]['predicted_probability'], bins=100,
                         ax=ax, label='real', color='green',
                         kde_kws={'bw': 0.01, 'alpha': 1},
                         hist_kws={'alpha': 0.2})

        # set plot
        ax.set_xlim(0, 1)
        ax.set_title('predicted probability density by class', fontsize=fontsize)
        ax.set_xlabel('predicted probability', fontsize=fontsize)
        ax.set_ylabel('density', fontsize=fontsize)
        ax.xaxis.set_tick_params(labelsize=fontsize)
        ax.yaxis.set_tick_params(labelsize=fontsize)
        ax.legend(bbox_to_anchor=(0.9, 0.9), prop={'size': fontsize});


    def get_confusion_matrix(self, threshold):
        """
        Return a list of confusion matrix for each fold
        → Arguments:
            - threshold: the probability threshold at which we want to compute the confusion matrices 
        """
        cms = []

        for i, fold_metrics in self.metrics.iterrows():
            if threshold == 0.5:
                y_pred = fold_metrics['y_class_pred']
            else:
                y_pred = (fold_metrics['y_proba_pred'] >= threshold)
            # we use [::-1][:,::-1] to invert axes and plot the usual confusion matrix (not the sklearn one)
            cms.append(confusion_matrix(fold_metrics['y_test'], y_pred)[::-1][:,::-1])

        return cms


    def plot_confusion_matrix(self, figsize=(20, 3), fontsize=12, threshold=0.5):
        """
        Plot confusion matrix for each fold
        → Arguments:
            - ax         : matplotlib axis object
            - fontsize   : size of the legend
            - threshold  : probability threshold used to choose the predicted y
        """
        # set plot
        plt.figure(figsize=figsize)

        # get the confusion matrices list
        cms = self.get_confusion_matrix(threshold)

        # for each fold
        for i, conf_mat in enumerate(cms):

            cm = pd.DataFrame(conf_mat, index=['True', 'False'], columns=['True', 'False'])
            
            # set plot
            plt.subplot(1, self.number_of_folds, i + 1)
            plt.title('fold {}'.format(i + 1))
            
            # compute some metrics
            prop = pd.DataFrame(cm.values / (cm.sum(axis = 1)[:, np.newaxis]), index=['True', 'False'], columns=['True', 'False'])
            
            # compute custom label
            labels = prop.applymap(lambda x: '{:.1f}%'.format(100 * x)) + cm.applymap(lambda x: ' ({})'.format(x))
            
            # plot confusion matrix
            seaborn.heatmap(prop, annot=labels, fmt='s', cmap=plt.cm.Blues, vmin=0, vmax=1, annot_kws={"size": fontsize})

            plt.ylabel('Real', fontsize=fontsize)
            plt.xlabel('Predicted', fontsize=fontsize)


    def plot_mean_confusion_matrix(self, figsize=(6, 5), fontsize=16, threshold=0.5):
        """
        Plot mean confusion matrix accross every fold
        → Arguments:
            - figsize    : figure size
            - fontsize   : size of the legend
            - threshold  : probability threshold used to choose the predicted y
        """
        # set plot
        plt.figure(figsize=figsize)
        plt.title('mean confusion matrix over {} folds'.format(self.number_of_folds), fontsize=fontsize)
        
        # get the confusion matrices list
        cms = self.get_confusion_matrix(threshold)

        # compute some metrics
        mean_cm = pd.DataFrame(np.mean(cms, axis = 0), index=['True', 'False'], columns=['True', 'False'])
        std_cm  = pd.DataFrame(np.std(cms , axis = 0), index=['True', 'False'], columns=['True', 'False'])
        
        prop = pd.DataFrame(mean_cm.values / (mean_cm.sum(axis = 1)[:, np.newaxis]), index=['True', 'False'], columns=['True', 'False'])
        pstd = pd.DataFrame(std_cm.values  / (mean_cm.sum(axis = 1)[:, np.newaxis]), index=['True', 'False'], columns=['True', 'False'])
        
        # compute custom label
        labels = prop.applymap(lambda x: '{:.1f}%'.format(100 * x))   + mean_cm.applymap(lambda x: ' ({:.1f})'.format(x)) + '\n' +\
                 pstd.applymap(lambda x: '± {:.1f}%'.format(100 * x)) + std_cm.applymap(lambda x: ' (± {:.1f})'.format(x))
        
        # plot confusion matrix
        seaborn.heatmap(prop, annot=labels, fmt='s', cmap=plt.cm.Blues, vmin=0, vmax=1, annot_kws={"size": fontsize})

        plt.ylabel('Real', fontsize=fontsize)
        plt.xlabel('Predicted', fontsize=fontsize)


    def plot_grid_search_results(self, plot_error_bar=True):
        """
        For each hyperparameter p, plot a subplot made of multiple scatter plots (one for each fold) with for each scatter plot:
        x: the hyperparameter p values, the other hyperparameters are fixed to their best values for the fold
        y: the grid search score for this fold and this hyperparameters set (ie moving hyperparameter p and other hyperparameters fixed)
        → Arguments:
            - plot_error_bar: if True plot an error bar for each grid-search point (std on the nested cross-validation folds)
        """
        # get hyper_parameters list
        hyper_parameters = list(self.metrics.iloc[0]['gs_best_parameters'].keys())
        
        # boiler plate code to get the number of folds in the nested cross-validation
        n_folds_nested_cross_validation = len([key for key in self.metrics.iloc[0]['gs_cv_results'].keys() if key.startswith('split') and key.endswith('_test_score')])
        print('{} hyperparameters tuned for {} different folds (over a {}-fold nested cross-validation):'.format(len(hyper_parameters), self.number_of_folds, n_folds_nested_cross_validation))
        
        # print the parameters grid
        max_param_name_length = max([len(p) for p in hyper_parameters])
        for p in hyper_parameters:
            print('  → {}: {}'.format(p.ljust(max_param_name_length), np.unique(self.metrics.iloc[0].gs_cv_results['param_{}'.format(p)])))

        # print the best parameters for each fold
        print('Best hyperparameters for each fold:')
        for i, fold_metrics in self.metrics.iterrows():
            print('fold {}: {}'.format(i, fold_metrics['gs_best_parameters']))


        # we plot one subplot of size 10x10 per hyperparameter
        plt.figure(figsize = (10 * len(hyper_parameters), 10))

        # for each hyperparameter
        for (plot_id, moving_parameter) in enumerate(hyper_parameters):
            # get fixed parameters list
            fix_parameters = [p for p in hyper_parameters if p != moving_parameter]

            plt.subplot(1, len(hyper_parameters), plot_id + 1)
            plt.title('Varying "{}" with all other hyperparameters\nfixed to its(their) best value(s) for each fold'.format(moving_parameter, fix_parameters))
            plt.ylabel('score')
            plt.xlabel(moving_parameter)

            # for each fold
            for fold_number in range(self.number_of_folds):
                # get the grid search results for this fold
                fold_metric = pd.DataFrame(self.metrics.iloc[fold_number]['gs_cv_results'])

                # only keep the best hyperparameters values for this fold
                for p in fix_parameters:
                    fold_metric = fold_metric.iloc[np.where(fold_metric['param_{}'.format(p)] == self.metrics.iloc[fold_number]['gs_best_parameters'][p])]

                x = fold_metric['param_{}'.format(moving_parameter)]
                y = fold_metric['mean_test_score']
                
                # plot score curve
                plot = plt.plot(x, y, '-o', markersize=10, alpha=0.6, label='fold {}'.format(fold_number + 1))

                # plot special marker for the highest value
                plt.plot(x[y.idxmax()], y.max(), 'o',  alpha=0.6, markersize=20, color=plot[0].get_color())

                # plot error bars
                if plot_error_bar:
                    plt.errorbar(x, y, yerr=fold_metric['std_test_score'], capsize=5, label=None, ecolor=plot[0].get_color(), fmt='none', alpha=0.5)
                
            plt.legend(loc='lower right', prop={'size': 15})


    def get_learning_curves_metrics(self, train_sizes=np.linspace(0.1, 1, 10), scoring='roc_auc', n_jobs=1):
        """
        Get learning curves metrics.
        → Arguments:
            - train_sizes: sizes of the train set
            - scoring    : scoring metric to evaluate
            - n_jobs     : number of jobs
        """
        print('Run learning curves computation...', end='')
        start = time.time()

        # get learning curves
        self.lc_train_sizes, self.lc_train_scores, self.lc_test_scores = learning_curve(self.model, self.X, self.y,
                                                                                        train_sizes=train_sizes, cv=self.cv_strategy,
                                                                                        n_jobs=n_jobs, error_score='raise')

        print(' done! ({:.2f}s)'.format(time.time() - start))


    def plot_learning_curves(self, figsize=(10, 10)):
        """
        Plot learning curves
        Strongly inspired by http://scikit-learn.org/stable/auto_examples/model_selection/plot_learning_curve.html
        → Arguments:
            - figsize: figure size
        """
        # set plot
        plt.figure(figsize=figsize)
        plt.title('Learning curves')
        plt.xlabel('Number of training examples')
        plt.ylabel('ROC AUC score')

        train_scores_mean = np.mean(self.lc_train_scores, axis=1)
        test_scores_mean  = np.mean(self.lc_test_scores , axis=1)
        test_scores_std   = np.std(self.lc_test_scores  , axis=1)
        train_scores_std  = np.std(self.lc_train_scores , axis=1)

         # plot metrics and their standard deviations
        plt.plot(self.lc_train_sizes, train_scores_mean, 'o-', color='r', markersize=10, label='mean train score')
        plt.plot(self.lc_train_sizes, test_scores_mean , 'o-', color='g', markersize=10, label='mean test score')
        plt.fill_between(self.lc_train_sizes, train_scores_mean - train_scores_std, train_scores_mean + train_scores_std,
                         alpha=0.1, color='r', label='mean train score ± 1 std. dev.')
        plt.fill_between(self.lc_train_sizes, test_scores_mean - test_scores_std, test_scores_mean + test_scores_std,
                         alpha=0.1, color='g', label='mean test score ± 1 std. dev.')
        
        plt.legend(loc='best', prop={'size': figsize[0] * 1.5})


    def plot_features_importance(self, random_forest=False, figsize=(20, 8), pipeline_step_index=None):
        """
        Plot features importance by fitting the model on the whole dataset
        This is gini importance (and not the mean decrease accuracy), see https://stackoverflow.com/questions/15810339/how-are-feature-importances-in-randomforestclassifier-determined>
        → Arguments:
            - random_forest: set to True if the model is Random Forest to get the inter tree variability error bars
            - figsize      : figure size
        """
        print('Fit model...', end='')
        start = time.time()

        self.model.fit(self.X, self.y)

        print(' done! ({:.2f}s)'.format(time.time() - start))
        
        # get features importance
        if not pipeline_step_index:
            feature_importance = pd.DataFrame({'value': self.model.feature_importances_.tolist()}, index=self.X.columns.tolist())
        else:
            feature_importance = pd.DataFrame({'value': self.model.steps[pipeline_step_index][1].feature_importances_.tolist()}, index=self.X.columns.tolist())
        feature_importance.sort_values(by='value', axis=0, inplace=True)
        
        # get inter tree variability of the feature importance score
        if random_forest:
            if not pipeline_step_index:
                feature_importance['inter_tree_variability'] = np.std([tree.feature_importances_ for tree in self.model.estimators_], axis=0)
            else:
                feature_importance['inter_tree_variability'] = np.std([tree.feature_importances_ for tree in self.model.steps[pipeline_step_index][1].estimators_], axis=0)
        else:
            feature_importance['inter_tree_variability'] = 0
        
        plt.figure(figsize=figsize)
        
        plt.subplot(1, 2, 1)
        feature_importance.tail(15).value.plot.barh(width=0.85, xerr=feature_importance.tail(15)['inter_tree_variability'], linewidth=0)
            
        plt.subplot(1, 2, 2)
        feature_importance.value.plot.barh(width=0.85, xerr=feature_importance['inter_tree_variability'], linewidth=0)
        plt.tight_layout()
