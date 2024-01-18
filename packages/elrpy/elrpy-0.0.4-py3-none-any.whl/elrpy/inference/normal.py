
def normal_marginal_confidence_interval(grad_fn, hess_fn, params, alpha=0.05):
    """Returns the confidence interval for the given parameters.
    
    Args:
        grad_fn (function): gradient function
        hess_fn (function): Hessian function
        params (np.ndarray): parameters
        alpha (float): confidence level
        
    Returns:
        tuple: lower and upper confidence bounds
    """
    grad = grad_fn(params)
    hess = hess_fn(params)
    z = np.sqrt(params.shape[0]) * np.linalg.solve(hess, grad)
    lower = params - norm.ppf(1 - alpha / 2) * np.sqrt(np.diag(np.linalg.inv(hess)))
    upper = params + norm.ppf(1 - alpha / 2) * np.sqrt(np.diag(np.linalg.inv(hess)))
    