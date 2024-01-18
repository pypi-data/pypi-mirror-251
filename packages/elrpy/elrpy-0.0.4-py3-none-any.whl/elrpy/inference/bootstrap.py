import jax
from jax import numpy as np

def get_bootstrap_weights(rng, group_data, num_boots, estimate_on_all=False, sample_by_group_size=True):
    """Returns bootstrap weights for each group.
    
    Args:
        rng (jax.random.PRNGKey): random number generator
        group_data (tuple): tuple of group covariates, group outcomes, and group sizes
        num_boots (int): number of bootstrap samples
        estimate_on_all (bool): whether to include replicate estimated on all data, e.g. all ones
        
    Returns:
        dict: dictionary of bootstrap weights for each group
    """
    num_boots -= estimate_on_all
    num_groups = len(group_data[0])
    group_sizes, tree_def = jax.tree_flatten(jax.tree_map(lambda x: x.shape[0], group_data[0])) 
    group_sizes = np.array(group_sizes)
    if sample_by_group_size:
        group_idx = jax.random.choice(rng, num_groups, shape=(num_groups, num_boots), p=group_sizes / np.sum(group_sizes))
    else:
        group_idx = jax.random.choice(rng, num_groups, shape=(num_groups, num_boots))
    weights = np.zeros((num_groups, num_boots))
    weights = jax.vmap(lambda w, idx: w.at[idx].add(1), in_axes=(1, 1))(weights, group_idx).T
    if estimate_on_all:
        weights = np.hstack([np.ones((num_groups, 1)), weights])
    group_weights = {g: w[:, None] for g, w in zip(group_data[0], weights)}
    return group_weights

def bootstrap_marginal_confidence_interval(bootstrap_params, alpha=0.05):
    """Returns the confidence interval for the given bootstrap parameters.
    
    Args:
        bootstrap_params (np.ndarray): bootstrap parameters
        alpha (float): confidence level
        
    Returns:
        tuple: lower and upper confidence bounds
    """
    lower = np.quantile(bootstrap_params, 100 * (alpha / 2), axis=0)
    upper = np.quantile(bootstrap_params, 100 * (1 - alpha / 2), axis=0)
    return lower, upper

def bootstrap_prediction_confidence_interval(model_fn, bootstrap_params, X, G=None, alpha=0.05):
    """Returns the confidence interval for the given bootstrap parameters.
    
    Args:
        model_fn (function): model function
        bootstrap_params (np.ndarray): bootstrap parameters
        X (np.ndarray): data matrix
        G (np.ndarray): group matrix
        alpha (float): confidence level
        
    Returns:
        tuple: lower and upper confidence bounds
    """
    bootstrap_y = model_fn(bootstrap_params, X)
    if G is not None:
        bootstrap_y = (G @ bootstrap_y.T).T

    lower = np.quantile(bootstrap_y, 100 * (alpha / 2), axis=0)
    upper = np.quantile(bootstrap_y, 100 * (1 - alpha / 2), axis=0)
    return lower, upper