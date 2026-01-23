def ecdf(data):
    """ Compute ECDF """
    import numpy as np
    x = np.sort(data)
    n = x.size
    y = np.arange(1, n+1) / n
    return(x,y)

def eval_ecdf(obs, x):
    import numpy as np
    from scipy.interpolate import interp1d
    interp_ecdf = interp1d(ecdf(obs)[0], ecdf(obs)[1], fill_value="extrapolate")
    return interp_ecdf(x)

def eval_inverse_ecdf(obs, x):
    import numpy as np
    from scipy.interpolate import interp1d
    ecdf_var = ecdf(obs)
    inverted_ecdf = interp1d(ecdf_var[1], ecdf_var[0], fill_value="extrapolate")
    return inverted_ecdf(x)

def sd_normal(data):
    from scipy import stats
    sd_data = stats.norm.ppf(data)
    return sd_data

def unity(data):
    from scipy import stats
    u_hat = data.copy()
    for col in data.columns:
        u_hat[col] = stats.rankdata(data[col]) / (len(data)+1)
    return u_hat

def conditionalize(data, model, cond_vars, cond_vals, tol=0.01, n_samples=1000, verbose=False):
    import numpy as np

    samples = np.array(model.simulate(n_samples))
    for var, val in zip(cond_vars, cond_vals):
        unity_val = eval_ecdf(data.iloc[:, var].values.T, val)
        idx = np.abs(samples[:, var] - unity_val) < tol
        # idx = idx.any(axis=1)
        samples = samples[idx]
        if verbose:
            print(f"Length samples after conditioning: {samples.shape[0]}")
    if samples.shape[0] == 0:
        if verbose:
            print("No samples found for the given conditioning values and tolerance.")
        return np.array([[0]]) 
    # to variable space
    else:
        columns = [i for i in range(len(data.columns)) if i not in cond_vars]
        sel_non_un = np.empty_like(samples)
        sel_non_un = [eval_inverse_ecdf(data.iloc[:, col], samples[:, col]) for col in columns]

    return np.array(sel_non_un)

def plot_conditionalize(data, model, cond_var, cond_val, tol=0.01, n_samples=1000):
    import numpy as np
    import matplotlib.pyplot as plt

    sel_non_un = conditionalize(data, model, cond_var, cond_val, tol, n_samples)
    sel_non_un = np.array(sel_non_un)

    n_plots = data.shape[1] - len(cond_var)
    if not n_plots == 1:
        fig, ax = plt.subplots(1, n_plots, figsize=(12,5))
        plotdata = data.drop(columns=data.columns[cond_var])
        for i in range(n_plots):
                ax[i].hist(plotdata.iloc[:,i], bins=9, alpha=0.5, density=True)
                ax[i].hist(sel_non_un[:,i], bins=9, alpha=0.5, density=True, label = 'conditioned samples')
                ax[i].set_title(plotdata.columns[i])
                ax[i].grid()
                ax[i].legend()
        plt.tight_layout()
    elif n_plots == 1:
        fig, ax = plt.subplots(1, 1, figsize=(6,5))
        plotdata = data.drop(columns=data.columns[cond_var])
        ax.hist(plotdata.iloc[:,0], bins=9, alpha=0.5, density=True)
        ax.hist(sel_non_un[:,0], bins=9, alpha=0.5, density=True)
        ax.set_title(plotdata.columns[0])
        ax.grid()
        plt.tight_layout()
    