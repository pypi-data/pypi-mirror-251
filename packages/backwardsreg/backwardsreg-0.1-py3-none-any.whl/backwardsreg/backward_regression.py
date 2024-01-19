import pandas as pd
import statsmodels.api as sm
import logging
import warnings

warnings.simplefilter("ignore")  # Ignore specific warnings during fitting
logging.basicConfig(level=logging.INFO)

def fit_regression(X, y, columns, regression_type='linear'):
    try:
        if regression_type == 'linear':
            model = sm.OLS(y, sm.add_constant(pd.DataFrame(X[columns]))).fit()
        elif regression_type == 'logistic':
            model = sm.Logit(y, sm.add_constant(pd.DataFrame(X[columns]))).fit(method='bfgs')
        else:
            logging.error("Invalid regression type. Choose 'linear' or 'logistic'.")
            return None

        return model
    except Exception as e:
        logging.error(f"Error fitting regression model: {e}")
        return None

def drop_worst_feature(X, y, included_features, threshold_out, dropped_variables, regression_type='linear'):
    model = fit_regression(X, y, included_features, regression_type)
    if model:
        pvalues = model.pvalues.iloc[1:]
        worst_pval = pvalues.max()
        if worst_pval > threshold_out:
            worst_feature = pvalues.idxmax()
            included_features.remove(worst_feature)
            dropped_variables.append(worst_feature)
            logging.info(f'Drop feature {worst_feature} with p-value {worst_pval}')
            return True
    return False

def backward_regression(X, y, threshold_in=0.01, threshold_out=0.05, include_interactions=False, verbose=True):
    if set(y.unique()) == {0, 1}:
        regression_type = 'logistic'
    elif y.nunique() > 2:
        regression_type = 'linear'
    else:
        logging.error("Target variable type not recognized. Use binary or continuous target.")
        return None

    included_features = list(X.columns)
    dropped_variables = []
    
    iteration = 1
    while True:
        changed = drop_worst_feature(X, y, included_features, threshold_out, dropped_variables, regression_type)
        
        if not changed:
            break
        
        iteration += 1
    
    if include_interactions:
        # Include interactions between variables
        included_with_interactions = included_features.copy()
        for i in range(len(included_features)):
            for j in range(i + 1, len(included_features)):
                interaction_term = f"{included_features[i]} * {included_features[j]}"
                X_interaction = X.copy()  # Create a copy of X to avoid modifying the original dataframe
                X_interaction[interaction_term] = X[included_features[i]] * X[included_features[j]]

                model = fit_regression(X_interaction, y, included_with_interactions + [interaction_term], regression_type)
                if model:
                    pval_interaction = model.pvalues[interaction_term]

                    if pval_interaction < threshold_in:
                        included_with_interactions.append(interaction_term)
                        logging.info(f'Include interaction term {interaction_term} with p-value {pval_interaction}')
                    else:
                        dropped_variables.append(interaction_term)
                        logging.info(f'Drop interaction term {interaction_term} with p-value {pval_interaction}')

        return included_with_interactions, dropped_variables
    else:
        return included_features, dropped_variables

# Example usage:
# result, dropped_vars = backward_regression(X, y, threshold_in=0.01, threshold_out=0.05, include_interactions=False, verbose=True)
# print("Final included features:", result)
# print("Dropped variables:", dropped_vars)
