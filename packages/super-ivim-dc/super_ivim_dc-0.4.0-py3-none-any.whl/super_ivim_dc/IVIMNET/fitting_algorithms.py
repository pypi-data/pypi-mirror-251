"""
September 2020 by Oliver Gurney-Champion
oliver.gurney.champion@gmail.com / o.j.gurney-champion@amsterdamumc.nl
https://www.github.com/ochampion

Built on code by Sebastiano Barbieri: https://github.com/sebbarb/deep_ivim

Code is uploaded as part of our publication in MRM (Kaandorp et al. Improved physics-informed deep learning of the intravoxel-incoherent motion model: accurate, unique and consistent. MRM 2021)
If this code was useful, please cite:
http://arxiv.org/abs/1903.00095
"""

import warnings

from joblib import Parallel, delayed
import numpy as np
from scipy import stats
from scipy.optimize import curve_fit, minimize
import tqdm


def fit_dats(bvalues, dw_data, arg, savename=None):
    """
    Wrapper function that selects the right fit depending on what fit is selected in arg.method.
    input:
    :param arg: an object with fit options, with attributes:
    arg.method --> string with the fit method; allowed: lsq (least squares fit), seg (segmented fit) and bayes (bayesian fit)
    arg.do_fit --> Boolean; False for skipping the regular fit
    arg.load_lsq --> Boolean; True will load the fit results saved under input parameter "savename"
    arg.fitS0 --> Boolean; False fixes S0 to 1, True fits S0
    arg.jobs --> Integer specifying the number of parallel processes used in fitting. If <2, regular fitting is used instead
    arg.bounds --> 2D Array of fit bounds ([Dtmin, Fpmin, Dpmin, S0min],[Dtmax, Fpmax, Dpmax, S0max])
    :param bvalues: 1D Array of b-values used
    :param dw_data: 2D Array containing the dw_data used with dimensions voxels x b-values
    optional:
    :param savename: String with the save name

    :return paramslsq: 2D array containing the fit parameters D, f (Fp), D* (Dp) and, optionally, S0, for each voxel
    """
    # Checking completeness of arg and adding missing values as defaults
    arg = checkarg_lsq(arg)
    if arg.do_fit:
        if not arg.load_lsq:
            # select fit to be run
            if arg.method == 'seg':
                print('running segmented fit\n')
                paramslsq = fit_segmented_array(bvalues, dw_data, njobs=arg.jobs, bounds=arg.bounds)
                # save results if parameter savename is given
                if savename is not None:
                    np.savez(savename, paramslsq=paramslsq)
            elif (arg.method == 'lsq'):
                print('running conventional fit\n')
                paramslsq = fit_least_squares_array(bvalues, dw_data, S0_output=True, fitS0=arg.fitS0, njobs=arg.jobs,
                                                    bounds=arg.bounds)
                # save results if parameter savename is given
                if savename is not None:
                    np.savez(savename, paramslsq=paramslsq)
            elif arg.method == 'bayes':
                print('running conventional fit to determine Bayesian prior\n')
                # for this Bayesian fit approach, a data-driven prior needs to be defined. Hence, intially we do a regular lsq fit
                paramslsq = fit_least_squares_array(bvalues, dw_data, S0_output=True, fitS0=arg.fitS0, njobs=arg.jobs,
                                                    bounds=arg.bounds)
                print('running Bayesian fit\n')
                Dt_pred, Fp_pred, Dp_pred, S0_pred = fit_bayesian_array(bvalues, dw_data, paramslsq, arg)
                Dt0, Fp0, Dp0, S00 = paramslsq
                # For Bayesian fit, we also give the lsq results as we had to obtain them anyway.
                if arg.fitS0:
                    paramslsq = Dt_pred, Fp_pred, Dp_pred, S0_pred, Dt0, Fp0, Dp0, S00
                else:
                    paramslsq = Dt_pred, Fp_pred, Dp_pred, Dt0, Fp0, Dp0
                if savename is not None:
                    # save results if parameter savename is given
                    np.savez(savename, paramslsq=paramslsq)
            else:
                raise Exception('the choise lsq-fit is not implemented. Try ''lsq'', ''seg'' or ''bayes''')
        else:
            # if we chose to load the fit
            print('loading fit\n')
            loads = np.load(savename)
            paramslsq = loads['paramslsq']
            del loads
        return paramslsq
    # if fit is skipped, we return nothing
    return None


def goodness_of_fit(bvalues, Dt, Fp, Dp, S0, dw_data):
    """
    Calculates the R-squared as a measure for goodness of fit.
    input parameters are
    :param b: 1D Array b-values
    :param Dt: 1D Array with fitted D
    :param Fp: 1D Array with fitted f
    :param Dp: 1D Array with fitted D*
    :param S0: 1D Array with fitted S0 (or ones)
    :param dw_data: 2D array containing data, as voxels x b-values

    :return R2: 1D Array with the R-squared for each voxel
    """
    # simulate the IVIM signal given the D, f, D* and S0
    datasim = ivim(np.tile(np.expand_dims(bvalues, axis=0), (len(Dt), 1)),
                   np.tile(np.expand_dims(Dt, axis=1), (1, len(bvalues))),
                   np.tile(np.expand_dims(Fp, axis=1), (1, len(bvalues))),
                   np.tile(np.expand_dims(Dp, axis=1), (1, len(bvalues))),
                   np.tile(np.expand_dims(S0, axis=1), (1, len(bvalues)))).astype('f')

    # calculate R-squared given the estimated IVIM signal and the data
    norm = np.mean(dw_data, axis=1)
    ss_tot = np.sum(np.square(dw_data - norm[:, None]), axis=1)
    ss_res = np.sum(np.square(dw_data - datasim), axis=1)
    R2 = 1 - (ss_res / ss_tot)  # R-squared
    return R2


def MSE(bvalues, Dt, Fp, Dp, S0, dw_data):
    """
    Calculates the MSE as a measure for goodness of fit.
    input parameters are
    :param b: 1D Array b-values
    :param Dt: 1D Array with fitted D
    :param Fp: 1D Array with fitted f
    :param Dp: 1D Array with fitted D*
    :param S0: 1D Array with fitted S0 (or ones)
    :param dw_data: 2D array containing data, as voxels x b-values

    :return MSError: 1D Array with the R-squared for each voxel
    """
    # simulate the IVIM signal given the D, f, D* and S0
    datasim = ivim(np.tile(np.expand_dims(bvalues, axis=0), (len(Dt), 1)),
                   np.tile(np.expand_dims(Dt, axis=1), (1, len(bvalues))),
                   np.tile(np.expand_dims(Fp, axis=1), (1, len(bvalues))),
                   np.tile(np.expand_dims(Dp, axis=1), (1, len(bvalues))),
                   np.tile(np.expand_dims(S0, axis=1), (1, len(bvalues)))).astype('f')

    # calculate R-squared given the estimated IVIM signal and the data
    MSError = np.mean(np.square(dw_data-datasim),axis=1)  # R-squared
    return MSError


def ivimN(bvalues, Dt, Fp, Dp, S0):
    # IVIM function in which we try to have equal variance in the different IVIM parameters; equal variance helps with certain fitting algorithms
    return S0 * (Fp / 10 * np.exp(-bvalues * Dp / 10) + (1 - Fp / 10) * np.exp(-bvalues * Dt / 1000))


def ivimN_noS0(bvalues, Dt, Fp, Dp):
    # IVIM function in which we try to have equal variance in the different IVIM parameters and S0=1
    return (Fp / 10 * np.exp(-bvalues * Dp / 10) + (1 - Fp / 10) * np.exp(-bvalues * Dt / 1000))


def ivim(bvalues, Dt, Fp, Dp, S0):
    # regular IVIM function
    return (S0 * (Fp * np.exp(-bvalues * Dp) + (1 - Fp) * np.exp(-bvalues * Dt)))


def order(Dt, Fp, Dp, S0=None):
    # function to reorder D* and D in case they were swapped during unconstraint fitting. Forces D* > D (Dp>Dt)
    if Dp < Dt:
        Dp, Dt = Dt, Dp
        Fp = 1 - Fp
    if S0 is None:
        return Dt, Fp, Dp
    else:
        return Dt, Fp, Dp, S0


def fit_segmented_array(bvalues, dw_data, njobs=4, bounds=([0, 0, 0.005],[0.005, 0.7, 0.3]), cutoff=75):
    """
    This is an implementation of the segmented fit, in which we first estimate D using a curve fit to b-values>cutoff;
    then estimate f from the fitted S0 and the measured S0 and finally estimate D* while fixing D and f. This fit
    is done on an array.
    :param bvalues: 1D Array with the b-values
    :param dw_data: 2D Array with diffusion-weighted signal in different voxels at different b-values
    :param njobs: Integer determining the number of parallel processes; default = 4
    :param bounds: 2D Array with fit bounds ([Dtmin, Fpmin, Dpmin, S0min],[Dtmax, Fpmax, Dpmax, S0max]). Default: ([0.005, 0, 0, 0.8], [0.3, 0.7, 0.005, 1.2])
    :param cutoff: cutoff value for determining which data is taken along in fitting D
    :return Dt: 1D Array with D in each voxel
    :return Fp: 1D Array with f in each voxel
    :return Dp: 1D Array with Dp in each voxel
    :return S0: 1D Array with S0 in each voxel
    """
    # first we normalise the signal to S0
    S0 = np.mean(dw_data[:, bvalues == 0], axis=1)
    dw_data = dw_data / S0[:, None]
    # here we try parallel computing, but if fails, go back to computing one single core.
    single = False
    if njobs > 2:
        try:
            # define the parallel function
            def parfun(i):
                return fit_segmented(bvalues, dw_data[i, :], bounds=bounds, cutoff=cutoff)

            output = Parallel(n_jobs=njobs)(delayed(parfun)(i) for i in tqdm.tqdm(range(len(dw_data)), position=0, leave=True))
            Dt, Fp, Dp = np.transpose(output)
        except:
            # if fails, retry using single core
            single = True
    else:
        # or, if specified, immediately go to single core
        single = True
    if single:
        # initialize empty arrays
        Dp = np.zeros(len(dw_data))
        Dt = np.zeros(len(dw_data))
        Fp = np.zeros(len(dw_data))
        for i in tqdm.tqdm(range(len(dw_data)), position=0, leave=True):
            # fill arrays with fit results on a per voxel base:
            Dt[i], Fp[i], Dp[i] = fit_segmented(bvalues, dw_data[i, :], bounds=bounds, cutoff=cutoff)
    return [Dt, Fp, Dp, S0]


def fit_segmented(bvalues, dw_data, bounds=([0, 0, 0.005],[0.005, 0.7, 0.3]), cutoff=75):
    """
    This is an implementation of the segmented fit, in which we first estimate D using a curve fit to b-values>cutoff;
    then estimate f from the fitted S0 and the measured S0 and finally estimate D* while fixing D and f.
    :param bvalues: Array with the b-values
    :param dw_data: Array with diffusion-weighted signal at different b-values
    :param bounds: Array with fit bounds ([Dtmin, Fpmin, Dpmin, S0min],[Dtmax, Fpmax, Dpmax, S0max]). Default: ([0.005, 0, 0, 0.8], [0.3, 0.7, 0.005, 1.2])
    :param cutoff: cutoff value for determining which data is taken along in fitting D
    :return Dt: Fitted D
    :return Fp: Fitted f
    :return Dp: Fitted Dp
    :return S0: Fitted S0
    """
    try:
        # determine high b-values and data for D
        high_b = bvalues[bvalues >= cutoff]
        high_dw_data = dw_data[bvalues >= cutoff]
        # correct the bounds. Note that S0 bounds determine the max and min of f
        bounds1 = ([bounds[0][0] * 1000., 1 - bounds[1][1]], [bounds[1][0] * 1000., 1. - bounds[0][
            1]])  # By bounding S0 like this, we effectively insert the boundaries of f
        # fit for S0' and D
        params, _ = curve_fit(lambda b, Dt, int: int * np.exp(-b * Dt / 1000), high_b, high_dw_data,
                              p0=(1, 1),
                              bounds=bounds1)
        Dt, Fp = params[0] / 1000, 1 - params[1]
        # remove the diffusion part to only keep the pseudo-diffusion
        dw_data_remaining = dw_data - (1 - Fp) * np.exp(-bvalues * Dt)
        bounds2 = (bounds[0][2], bounds[1][2])
        # fit for D*
        params, _ = curve_fit(lambda b, Dp: Fp * np.exp(-b * Dp), bvalues, dw_data_remaining, p0=(0.1), bounds=bounds2)
        Dp = params[0]
        return Dt, Fp, Dp
    except:
        # if fit fails, return zeros
        # print('segnetned fit failed')
        return 0., 0., 0.


def fit_least_squares_array(bvalues, dw_data, S0_output=True, fitS0=True, njobs=4,
                            bounds=([0, 0, 0.005, 0.7],[0.005, 0.7, 0.3, 1.3])):
    """
    This is an implementation of the conventional IVIM fit. It is fitted in array form.
    :param bvalues: 1D Array with the b-values
    :param dw_data: 2D Array with diffusion-weighted signal in different voxels at different b-values
    :param S0_output: Boolean determining whether to output (often a dummy) variable S0; default = True
    :param fix_S0: Boolean determining whether to fix S0 to 1; default = False
    :param njobs: Integer determining the number of parallel processes; default = 4
    :param bounds: Array with fit bounds ([Dtmin, Fpmin, Dpmin, S0min],[Dtmax, Fpmax, Dpmax, S0max]). Default: ([0.005, 0, 0, 0.8], [0.3, 0.7, 0.005, 1.2])
    :return Dt: 1D Array with D in each voxel
    :return Fp: 1D Array with f in each voxel
    :return Dp: 1D Array with Dp in each voxel
    :return S0: 1D Array with S0 in each voxel
    """
    # normalise the data to S(value=0)
    S0 = np.mean(dw_data[:, bvalues == 0], axis=1)
    dw_data = dw_data / S0[:, None]
    single = False
    # split up on whether we want S0 as output
    if S0_output:
        # check if parallel is desired
        if njobs > 1:
            try:
                # defining parallel function
                def parfun(i):
                    return fit_least_squares(bvalues, dw_data[i, :], S0_output=S0_output, fitS0=fitS0, bounds=bounds)

                output = Parallel(n_jobs=njobs)(delayed(parfun)(i) for i in tqdm.tqdm(range(len(dw_data)), position=0, leave=True))
                Dt, Fp, Dp, S0 = np.transpose(output)
            except:
                single = True
        else:
            single = True
        if single:
            # run on single core, instead. Defining empty arrays
            Dp = np.zeros(len(dw_data))
            Dt = np.zeros(len(dw_data))
            Fp = np.zeros(len(dw_data))
            S0 = np.zeros(len(dw_data))
            # running in a single loop and filling arrays
            for i in tqdm.tqdm(range(len(dw_data)), position=0, leave=True):
                Dt[i], Fp[i], Dp[i], S0[i] = fit_least_squares(bvalues, dw_data[i, :], S0_output=S0_output, fitS0=fitS0,
                                                               bounds=bounds)
        return [Dt, Fp, Dp, S0]
    else:
        # if S0 is not exported
        if njobs > 1:
            try:
                def parfun(i):
                    return fit_least_squares(bvalues, dw_data[i, :], fitS0=fitS0, bounds=bounds)

                output = Parallel(n_jobs=njobs)(delayed(parfun)(i) for i in tqdm.tqdm(range(len(dw_data)), position=0, leave=True))
                Dt, Fp, Dp = np.transpose(output)
            except:
                single = True
        else:
            single = True
        if single:
            Dp = np.zeros(len(dw_data))
            Dt = np.zeros(len(dw_data))
            Fp = np.zeros(len(dw_data))
            for i in range(len(dw_data)):
                Dt[i], Fp[i], Dp[i] = fit_least_squares(bvalues, dw_data[i, :], S0_output=S0_output, fitS0=fitS0,
                                                        bounds=bounds)
        return [Dt, Fp, Dp]


def fit_least_squares(bvalues, dw_data, S0_output=False, fitS0=True,
                      bounds=([0, 0, 0.005, 0.7],[0.005, 0.7, 0.3, 1.3])):
    """
    This is an implementation of the conventional IVIM fit. It fits a single curve
    :param bvalues: Array with the b-values
    :param dw_data: Array with diffusion-weighted signal at different b-values
    :param S0_output: Boolean determining whether to output (often a dummy) variable S0; default = True
    :param fix_S0: Boolean determining whether to fix S0 to 1; default = False
    :param bounds: Array with fit bounds ([Dtmin, Fpmin, Dpmin, S0min],[Dtmax, Fpmax, Dpmax, S0max]). Default: ([0.005, 0, 0, 0.8], [0.3, 0.7, 0.005, 1.2])
    :return Dt: Array with D in each voxel
    :return Fp: Array with f in each voxel
    :return Dp: Array with Dp in each voxel
    :return S0: Array with S0 in each voxel
    """
    try:
        if not fitS0:
            # bounds are rescaled such that each parameter changes at roughly the same rate to help fitting.
            bounds = ([bounds[0][0] * 1000, bounds[0][1] * 10, bounds[0][2] * 10],
                      [bounds[1][0] * 1000, bounds[1][1] * 10, bounds[1][2] * 10])
            params, _ = curve_fit(ivimN_noS0, bvalues, dw_data, p0=[1, 1, 0.1], bounds=bounds)
            S0 = 1
        else:
            # bounds are rescaled such that each parameter changes at roughly the same rate to help fitting.
            bounds = ([bounds[0][0] * 1000, bounds[0][1] * 10, bounds[0][2] * 10, bounds[0][3]],
                      [bounds[1][0] * 1000, bounds[1][1] * 10, bounds[1][2] * 10, bounds[1][3]])
            params, _ = curve_fit(ivimN, bvalues, dw_data, p0=[1, 1, 0.1, 1], bounds=bounds)
            S0 = params[3]
        # correct for the rescaling of parameters
        Dt, Fp, Dp = params[0] / 1000, params[1] / 10, params[2] / 10
        # reorder output in case Dp<Dt
        if S0_output:
            return order(Dt, Fp, Dp, S0)
        else:
            return order(Dt, Fp, Dp)
    except:
        # if fit fails, then do a segmented fit instead
        # print('lsq fit failed, trying segmented')
        if S0_output:
            Dt, Fp, Dp = fit_segmented(bvalues, dw_data, bounds=bounds)
            return Dt, Fp, Dp, 1
        else:
            return fit_segmented(bvalues, dw_data)


def empirical_neg_log_prior(Dt0, Fp0, Dp0, S00=None):
    """
    This function determines the negative of the log of the empirical prior probability of the IVIM parameters
    :param Dt0: 1D Array with the initial D estimates
    :param Dt0: 1D Array with the initial f estimates
    :param Dt0: 1D Array with the initial D* estimates
    :param Dt0: 1D Array with the initial S0 estimates (optional)
    """
    # Dp0, Dt0, Fp0 are flattened arrays
    # only take valid voxels along, in which the initial estimates were sensible and successful
    Dp_valid = (1e-8 < np.nan_to_num(Dp0)) & (np.nan_to_num(Dp0) < 1 - 1e-8)
    Dt_valid = (1e-8 < np.nan_to_num(Dt0)) & (np.nan_to_num(Dt0) < 1 - 1e-8)
    Fp_valid = (1e-8 < np.nan_to_num(Fp0)) & (np.nan_to_num(Fp0) < 1 - 1e-8)
    # determine whether we fit S0
    if S00 is not None:
        S0_valid = (1e-8 < np.nan_to_num(S00)) & (np.nan_to_num(S00) < 2 - 1e-8)
        valid = Dp_valid & Dt_valid & Fp_valid & S0_valid
        Dp0, Dt0, Fp0, S00 = Dp0[valid], Dt0[valid], Fp0[valid], S00[valid]
    else:
        valid = Dp_valid & Dt_valid & Fp_valid
        Dp0, Dt0, Fp0 = Dp0[valid], Dt0[valid], Fp0[valid]
    # determine prior's shape. Note that D, D* and S0 are shaped as lognorm distributions whereas f is a beta distribution
    Dp_shape, _, Dp_scale = stats.lognorm.fit(Dp0, floc=0)
    Dt_shape, _, Dt_scale = stats.lognorm.fit(Dt0, floc=0)
    Fp_a, Fp_b, _, _ = stats.beta.fit(Fp0, floc=0, fscale=1)
    if S00 is not None:
        S0_a, S0_b, _, _ = stats.beta.fit(S00, floc=0, fscale=2)

    # define the prior
    def neg_log_prior(p):
        # depends on whether S0 is fitted or not
        if len(p) == 4:
            Dt, Fp, Dp, S0 = p[0], p[1], p[2], p[3]
        else:
            Dt, Fp, Dp = p[0], p[1], p[2]
        # make D*<D very unlikely
        if (Dp < Dt):
            return 1e8
        else:
            eps = 1e-8
            Dp_prior = stats.lognorm.pdf(Dp, Dp_shape, scale=Dp_scale)
            Dt_prior = stats.lognorm.pdf(Dt, Dt_shape, scale=Dt_scale)
            Fp_prior = stats.beta.pdf(Fp, Fp_a, Fp_b)
            # determine and return the prior for D, f and D* (and S0)
            if len(p) == 4:
                S0_prior = stats.beta.pdf(S0 / 2, S0_a, S0_b)
                return -np.log(Dp_prior + eps) - np.log(Dt_prior + eps) - np.log(Fp_prior + eps) - np.log(
                    S0_prior + eps)
            else:
                return -np.log(Dp_prior + eps) - np.log(Dt_prior + eps) - np.log(Fp_prior + eps)

    return neg_log_prior


def neg_log_likelihood(p, bvalues, dw_data):
    """
    This function determines the negative of the log of the likelihood of parameters p, given the data dw_data for the Bayesian fit
    :param p: 1D Array with the estimates of D, f, D* and (optionally) S0
    :param bvalues: 1D array with b-values
    :param dw_data: 1D Array diffusion-weighted data
    :returns: the log-likelihood of the parameters given the data
    """
    if len(p) == 4:
        return 0.5 * (len(bvalues) + 1) * np.log(
            np.sum((ivim(bvalues, p[0], p[1], p[2], p[3]) - dw_data) ** 2))  # 0.5*sum simplified
    else:
        return 0.5 * (len(bvalues) + 1) * np.log(
            np.sum((ivim(bvalues, p[0], p[1], p[2], 1) - dw_data) ** 2))  # 0.5*sum simplified


def neg_log_posterior(p, bvalues, dw_data, neg_log_prior):
    """
    This function determines the negative of the log of the likelihood of parameters p, given the prior likelihood and the data
    :param p: 1D Array with the estimates of D, f, D* and (optionally) S0
    :param bvalues: 1D array with b-values
    :param dw_data: 1D Array diffusion-weighted data
    :param neg_log_prior: prior likelihood function (created with empirical_neg_log_prior)
    :returns: the posterior probability given the data and the prior
    """
    return neg_log_likelihood(p, bvalues, dw_data) + neg_log_prior(p)


def fit_bayesian_array(bvalues, dw_data, paramslsq, arg):
    """
    This is an implementation of the Bayesian IVIM fit for arrays. The fit is taken from Barbieri et al. which was
    initially introduced in http://arxiv.org/10.1002/mrm.25765 and later further improved in
    http://arxiv.org/abs/1903.00095. If found useful, please cite those papers.

    :param bvalues: Array with the b-values
    :param dw_data: 2D Array with diffusion-weighted signal in different voxels at different b-values
    :param paramslsq: 2D Array with initial estimates for the parameters. These form the base for the Bayesian prior
    distribution and are typically obtained by least squares fitting of the data
    :param arg: an object with fit options, with attributes:
    arg.fitS0 --> Boolean; False fixes S0 to 1, True fits S0
    arg.jobs --> Integer specifying the number of parallel processes used in fitting. If <2, regular fitting is used instead
    arg.bounds --> 2D Array of fit bounds ([Dtmin, Fpmin, Dpmin, S0min],[Dtmax, Fpmax, Dpmax, S0max])
    :return Dt: Array with D in each voxel
    :return Fp: Array with f in each voxel
    :return Dp: Array with Dp in each voxel
    :return S0: Array with S0 in each voxel
    """
    arg = checkarg_lsq(arg)
    # fill out missing args
    Dt0, Fp0, Dp0, S00 = paramslsq
    # determine prior
    if arg.fitS0:
        neg_log_prior = empirical_neg_log_prior(Dt0, Fp0, Dp0, S00)
    else:
        neg_log_prior = empirical_neg_log_prior(Dt0, Fp0, Dp0)
    single = False
    # determine whether we fit parallel or not
    if arg.jobs > 1:
        try:
            # do parallel bayesian fit
            def parfun(i):
                # starting point
                x0 = [Dt0[i], Fp0[i], Dp0[i], S00[i]]
                return fit_bayesian(bvalues, dw_data[i, :], neg_log_prior, x0, fitS0=arg.fitS0)

            output = Parallel(n_jobs=arg.jobs)(delayed(parfun)(i) for i in tqdm.tqdm(range(len(dw_data)), position=0,
                                                                                     leave=True))
            Dt_pred, Fp_pred, Dp_pred, S0_pred = np.transpose(output)
        except:
            single = True
    else:
        single = True
    if single:
        # do serial; intialising arrays
        Dp_pred = np.zeros(len(dw_data))
        Dt_pred = np.zeros(len(dw_data))
        Fp_pred = np.zeros(len(dw_data))
        S0_pred = np.zeros(len(dw_data))
        # fill in array while looping over voxels
        for i in tqdm.tqdm(range(len(dw_data)), position=0, leave=True):
            # starting point
            x0 = [Dt0[i], Fp0[i], Dp0[i], S00[i]]
            Dt, Fp, Dp, S0 = fit_bayesian(bvalues, dw_data[i, :], neg_log_prior, x0, fitS0=arg.fitS0)
            Dp_pred[i] = Dp
            Dt_pred[i] = Dt
            Fp_pred[i] = Fp
            S0_pred[i] = S0
    return Dt_pred, Fp_pred, Dp_pred, S0_pred


def fit_bayesian(bvalues, dw_data, neg_log_prior, x0=[0.001, 0.2, 0.05], fitS0=True):
    '''
    This is an implementation of the Bayesian IVIM fit. It returns the Maximum a posterior probability.
    The fit is taken from Barbieri et al. which was initially introduced in http://arxiv.org/10.1002/mrm.25765 and
    later further improved in http://arxiv.org/abs/1903.00095. If found useful, please cite those papers.

    :param bvalues: Array with the b-values
    :param dw_data: 1D Array with diffusion-weighted signal at different b-values
    :param neg_log_prior: the prior
    :param x0: 1D array with initial parameter guess
    :param fitS0: boolean, if set to False, S0 is not fitted
    :return Dt: estimated D
    :return Fp: estimated f
    :return Dp: estimated D*
    :return S0: estimated S0 (optional)
    '''
    try:
        # define fit bounds
        bounds = [(0, 0.006), (0, 1), (0.006, 0.3), (0, 2)]
        # Find the Maximum a posterior probability (MAP) by minimising the negative log of the posterior
        if fitS0:
            params = minimize(neg_log_posterior, x0=x0, args=(bvalues, dw_data, neg_log_prior), bounds=bounds)
        else:
            params = minimize(neg_log_posterior, x0=x0[:3], args=(bvalues, dw_data, neg_log_prior), bounds=bounds[:3])
        if not params.success:
            raise (params.message)
        if fitS0:
            Dt, Fp, Dp, S0 = params.x[0], params.x[1], params.x[2], params.x[3]
        else:
            Dt, Fp, Dp = params.x[0], params.x[1], params.x[2]
            S0 = 1
        return order(Dt, Fp, Dp, S0)
    except:
        # if fit fails, return regular lsq-fit result
        # print('a bayes fit fialed')
        return fit_least_squares(bvalues, dw_data, S0_output=True)


def checkarg_lsq(arg):
    if not hasattr(arg, 'method'):
        warnings.warn('arg.fit.method not defined. Using default of ''lsq''')
        arg.method='lsq'
    if not hasattr(arg, 'do_fit'):
        warnings.warn('arg.fit.do_fit not defined. Using default of True')
        arg.do_fit=True
    if not hasattr(arg, 'load_lsq'):
        warnings.warn('arg.fit.load_lsq not defined. Using default of False')
        arg.load_lsq=False
    if not hasattr(arg, 'fitS0'):
        warnings.warn('arg.fit.fitS0 not defined. Using default of False')
        arg.fitS0=False
    if not hasattr(arg, 'jobs'):
        warnings.warn('arg.fit.jobs not defined. Using default of 4')
        arg.jobs = 4
    if not hasattr(arg, 'bounds'):
        warnings.warn('arg.fit.bounds not defined. Using default of ([0, 0, 0.005, 0.7],[0.005, 0.7, 0.3, 1.3])')
        arg.bounds = ([0, 0, 0.005, 0.7],[0.005, 0.7, 0.3, 1.3]) #Dt, Fp, Ds, S0
    return arg
