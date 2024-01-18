# type: ignore
# @auto-fold regex /^\s*if/ /^\s*else/ /^\s*def/
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# sourcery skip

# my coding convention
# **EVAL : evaluate the performance of this method
# **RED  : redo this
# **DEB  : debugging needed in this part
# **DEL  : DELETE AT SOME POINT

import os
import logging
from copy import deepcopy
from importlib import reload

import matplotlib
import matplotlib.pyplot as pl
import matplotlib.colors as plc
import matplotlib.gridspec as gridspec
import numpy as np
import pandas as pd
from tqdm import tqdm

from .block import ReddModel
from .globals import _PLATFORM_SYSTEM, _CORES
from .model_repo import *
from .unmodel_repo import *
from .utils import *
from reddcolors import Palette

import multiprocessing
if _PLATFORM_SYSTEM == 'Darwin':
    #multiprocessing.set_start_method('spawn')
    pass

rc = Palette()

def hex2rgb(hex):
    hex_cleaned = hex.lstrip('#')
    return tuple(int(hex_cleaned[i:i+2], 16) for i in (0, 2 ,4))


def mk_cmap(target_colors, ncolors=100, mode=0):
    # mode=0 adds rc.fg as last color
    bgfg = [rc.bg, rc.fg]
    for c in bgfg:
        if c[0] == '#':
            c = hex2rgb(c)
    res = [bgfg[0]]
    for tc in target_colors:
        res.append(tc)
    if mode==0:
        res.append(bgfg[1])
    return plc.LinearSegmentedColormap.from_list('mycmap', res, N=ncolors)


def mk_bool_cmap(color):
    return plc.ListedColormap([rc.bg, color])


def plot_GM_Estimator(estimator, options=None):
    # sourcery skip: use-fstring-for-formatting
    if options is None:
        options = {}
    if True:
        saveloc = options['saveloc']
        saveplace = saveloc + '/plots/GMEstimates/'

        plot_fmt = options['format']  # 'png'
        plot_nm = options['plot_name']  # ''
        plot_title = options['plot_title']  # None
        plot_ylabel = options['plot_ylabel'] # None
        fill_cor = options['fill_cor']  # 0

        sig_factor = options['sig_factor']

        if plot_title is None:
            plot_title = 'Optimal estimate with Gaussian Mixtures\n for '

        if plot_ylabel is None:
            plot_ylabel = 'Probability Density'

    cor = ['C0', 'C1', 'C2', 'C4', 'C5', 'C7', 'C8', 'C9']
    colors = np.array([cor,cor,cor,cor,cor]).flatten()

    n_components = estimator.n_components

    mu = estimator.mixture_mean
    var = estimator.mixture_variance
    sig = estimator.mixture_sigma

    xx, yy = [], []

    xticks = [mu]

    fig, ax = pl.subplots(figsize=(8, 4))
    for i in range(sig_factor):
        xx.append(np.array([np.linspace(mu-sig*(i+1),
                                        mu+sig*(i+1),
                                        1000)]).T)

        yy.append(np.exp(estimator.score_samples(xx[i])))

        xx[i] = np.append(np.append(xx[i][0], xx[i]), xx[i][-1])
        yy[i] = np.append(np.append(0, yy[i]), 0)
        ax.fill(xx[i], yy[i], c=colors[fill_cor], alpha=1/sig_factor, zorder=2*(i+1)-1)

        vlines_kwargs = {'lw':[1.5, 1.5], 'ls':['--']}
        ax.vlines([xx[i][0], xx[i][-1]], ymin=[min(yy[i]), min(yy[i])],
                                         ymax=[yy[i][1], yy[i][-2]],
                                         colors=[rc.fg, rc.fg],
                                         zorder=2*(i+1),
                                         **vlines_kwargs)

        xticks.extend((xx[i][0], xx[i][-1]))
    ax.vlines(mu, ymin=[min(yy[0])],
                  ymax=[np.exp(estimator.score_samples([[mu]]))],
                  colors=[rc.fg],
                  lw=[2],
                  ls=['-'],
                  zorder=2*sig_factor)


    ax.plot(xx[-1], yy[-1], c=rc.fg, alpha=1, lw=2, zorder=9)

    mu_display = np.round(mu, 3)
    sig_display = np.round(sig, 3)

    # Dummy plots for labels
    ax.plot(
        np.median(xx[0]),
        np.median(yy[0]),
        alpha=0.0,
        label=f'$\mu = {mu_display}$',
    )
    ax.plot(np.median(xx[0]), np.median(yy[0]), alpha=0., label=r'$\sigma = {}$'.format(sig_display))
    if n_components > 1:
        ax.plot(np.median(xx[0]), np.median(yy[-1]), alpha=0., label=r'$N = {}$'.format(n_components))

    # Set ticks, labels, title, etc
    xticks = np.sort(xticks)

    dif = xticks[-1] - xticks[0]
    nround = 2
    for i in range(4):
        nround = i + 2
        if np.round(dif, i) // 10**-i > 0:
            break

    xticks = np.round(xticks, nround)
    yticks = np.round(np.linspace(0, max(yy[0]), 5), 2)

    ax.tick_params(axis='x', labelrotation=45)
    ax.set_xticks(xticks, minor=False)
    ax.set_yticks(yticks, minor=False)
    ax.legend(framealpha=0.)
    ax.set_title(plot_title+'{}'.format(plot_nm[2:]))
    ax.set_xlabel('{} {}'.format(plot_nm[2:], estimator.unit))
    ax.set_ylabel(plot_ylabel)


    pl.savefig(saveplace+'{}.{}'.format(plot_nm, plot_fmt),
               bbox_inches='tight')

    pl.close('all')


def plot_traces(sampler, eng_name, my_model, saveloc='', trace_modes=None, fmt='png'):
    if trace_modes is None:
        trace_modes = [0]
    # 0:trace, 1:norm_post, 2:dens_interv, 3:corner
    trace_mode_dic = {0:'Trace Plot',
                      1:'Normalised Posterior',
                      2:'Density Interval',
                      3:'Corner Plot'}
    saveplace = saveloc + '/plots/traces/'

    cor = ['C0', 'C1', 'C2', 'C4', 'C5', 'C7', 'C8', 'C9']
    colors_ = np.array([cor,cor,cor,cor,cor]).flatten()
    vn = np.array(flatten(my_model.get_attr_param('name')))[my_model.C_]
    try:
        if eng_name == 'reddemcee':
            import arviz as az
            arviz_data = az.from_emcee(sampler=sampler,
                                        var_names=vn)
            for trace_mode in trace_modes:

                # trace
                if trace_mode == 0:
                    circ_mask = np.array(flatten(my_model.get_attr_param('is_circular')))[my_model.C_]
                    circ_var_names = vn[circ_mask]
                    for b in my_model:
                        if b.ndim_ == 0:
                            break
                        vn_b = np.array(b.get_attr('name'))[b.C_]
                        az.plot_trace(arviz_data,
                                    figsize=(14, len(vn_b)*2.5),
                                    var_names=vn_b,
                                    circ_var_names=circ_var_names,
                                    plot_kwargs={'color':rc.fg},
                                    trace_kwargs={'color':rc.fg})

                        pl.subplots_adjust(hspace=0.60)
                        savefigname = saveplace + f'{trace_mode_dic[trace_mode]} {b.name_}.{fmt}'
                        pl.savefig(savefigname)
                        pl.close()

                elif trace_mode == 1:
                    for b in my_model:
                        for p in b[b.C_]:
                            fig, ax = pl.subplots(1, 1)
                            fig.suptitle(p.name)

                            az.plot_dist(arviz_data.posterior[p.name].values,
                                        color=rc.fg,
                                        rug=True,
                                        #figsize=(8, 6),
                                        )
                            #pl.ylabel('Probability Density')
                            pl.xlabel('Value')

                            savefigname = saveplace + f'{trace_mode_dic[trace_mode]} {p.name}.{fmt}'
                            pl.savefig(savefigname)
                elif trace_mode == 2:
                    for b in my_model:
                        if b.ndim_ == 0:
                            break
                        axes = az.plot_density(
                            [arviz_data],
                            var_names=np.array(b.get_attr('name'))[b.C_],
                            shade=0.2,
                            colors=colors_[b.bnumber_-1],
                            #hdi_markers='v'
                            )

                        fig = axes.flatten()[0].get_figure()
                        fig.suptitle("94% High Density Intervals")

                        savefigname = saveplace + f'{trace_mode_dic[trace_mode]} {b.name_}.{fmt}'
                        pl.savefig(savefigname)
                elif trace_mode == 3:
                    ax = az.plot_pair(arviz_data,
                            kind=["scatter", "kde"],
                            marginals=True,
                            marginal_kwargs={'color':rc.fg},
                            point_estimate="median",
                            scatter_kwargs={'color':rc.fg},
                            point_estimate_kwargs={'color':'red'},
                            point_estimate_marker_kwargs={'color':'red',
                                                        's':200,
                                                        'alpha':0.75},
                            )

                    savefigname = saveplace + f'{trace_mode_dic[trace_mode]}.{fmt}'
                    pl.savefig(savefigname)

                

        elif eng_name == 'dynesty':
            from dynesty import plotting as dyplot
            res2 = sampler
            for trace_mode in trace_modes:
                if trace_mode == 0:
                    # trace
                    for b in my_model:
                        vnb = np.array(b.get_attr('name'))[b.C_]
                        fig, axes = dyplot.traceplot(res2,
                                                    post_color=rc.fg,
                                                    trace_color=rc.fg,
                                                    labels=vnb,
                                                    dims=b.slice_true)
                        savefigname = saveplace + f'{trace_mode_dic[trace_mode]} {b.name_}.{fmt}'
                        pl.savefig(savefigname)
                elif trace_mode == 1:
                    arviz_data = az.from_emcee(sampler=sampler,
                                                var_names=vn)

                    for b in my_model:
                        for p in b[b.C_]:
                            fig, ax = pl.subplots(1, 1)
                            fig.suptitle(p.name)

                            az.plot_dist(arviz_data.posterior[p.name].values)

                            savefigname = saveplace + f'{trace_mode_dic[trace_mode]} {p.name}.{fmt}'
                            pl.savefig(savefigname)
                elif trace_mode == 2:
                    arviz_data = az.from_emcee(sampler=sampler,
                                                var_names=vn)

                    for b in my_model:
                        axes = az.plot_density(
                            [arviz_data],
                            var_names=np.array(b.get_attr('name'))[b.C_],
                            shade=0.2,
                            #hdi_markers='v'
                            )

                        fig = axes.flatten()[0].get_figure()
                        fig.suptitle("94% High Density Intervals")

                        savefigname = saveplace + f'{trace_mode_dic[trace_mode]} {b.name_}.{fmt}'
                        pl.savefig(savefigname)
                elif trace_mode == 3:
                    arviz_data = az.from_emcee(sampler=sampler,
                                                var_names=vn)

                    ax = az.plot_pair(arviz_data,
                            kind=["scatter", "kde"],
                            marginals=True,
                            marginal_kwargs={'color':rc.fg},
                            point_estimate="median",
                            scatter_kwargs={'color':rc.fg},
                            point_estimate_kwargs={'color':'red'},
                            point_estimate_marker_kwargs={'color':'red',
                                                        's':90},
                            )
                    savefigname = saveplace + f'{trace_mode_dic[trace_mode]}.{fmt}'
                    pl.savefig(savefigname)

            else:
                print(f'Method is not yet implemented for {eng_name}')
                return None

            pl.close('all')

    except Exception():
        print(f'Trace plot for {trace_mode_dic[trace_mode]} failed!')


def plot_KeplerianModel(my_data, my_model, res, options=None):
    if options is None:
        options = {}
    if True:
        saveloc = options['saveloc']
        saveplace = saveloc + '/plots/models/'
        unsaveplace = saveloc + '/plots/models/uncertainpy/'

        plot_fmt = options['format']
        switch_histogram = options['hist']
        switch_uncertain = options['uncertain']
        switch_errors = options['errors']
        switch_periodogram = options['periodogram']
        switch_celerite = options['celerite']
        logger_level = options['logger_level']
        gC = options['gC']

        axhline_kwargs = options['axhline_kwargs']
        errorbar_kwargs = options['errorbar_kwargs']

        # FULL_MODEL
        fm_figsize = (10, 8)

        if options['paper_mode']:
            fm_axhline_kwargs = {'color':'gray', 'linewidth':3}
            fm_errorbar_kwargs = {'marker':'o', 'ls':'', 'alpha':0.8,
                                'lw':2,
                                'markersize':10,
                                'markeredgewidth':1,
                                'markeredgecolor':'k',
                                }

            # LINE
            fm_model_line = {'ls':'--', 'lw':3}  # ?
            # HIST
            fm_hist = {'lw':2}  # 1
            fm_hist_tick_fs = 0
            # LEGEND
            fm_legend_fs = 14 # 10

            # FM_FRAME
            fm_frame_lw = 3
            # FM TICKS
            fm_tick_xsize = 20
            fm_tick_ysize = 20
            # LABELS
            fm_label_fs = 22
            # title
            fm_title_fs = 24

            plot_fmt = 'pdf'
            # PHASE


        posterior_method = 'GM'
        #c = ['C0', 'C1', 'C2', 'C4', 'C5', 'C7', 'C8', 'C9']
        c = ['C0', 'C1', 'C2', 'C4', 'C7', 'C8', 'C9']
        colors = np.array([c,c,c,c,c]).flatten()

        temp_file_names = []
        temp_mod_names = []
        temp_dat_names = []

        if switch_uncertain:
            import uncertainpy as un
            import chaospy as cp
            if logger_level is not None:
                logging.getLogger("chaospy").setLevel(logger_level)
                logging.getLogger("numpoly").setLevel(logger_level)


    def create_mod(data_arg, blocks_arg, tail_x, mod_number=0):
        x = ReddModel(data_arg, blocks_arg)
        x.switch_plot = True

        x.A_ = []
        x.nins__ = my_model.nins__
        #x.refresh__()  # needed to get nins

        temp_script = f'temp_mod_0{mod_number}.py'
        temp_file_names.append(temp_script)
        temp_mod_names.append(f'{saveloc}/temp/temp_model_{x.model_script_no}{tail_x}.py')
        temp_dat_names.append(f'{saveloc}/temp/temp_data{tail_x}.csv')

        with open(temp_script, 'w') as f:
            f.write(open(get_support('init.scr')).read())
            # DEPENDENCIES
            f.write('''
import kepler
''')
            if switch_celerite:
                f.write('''
import celerite2
import celerite2.terms as cterms
''')
            # CONSTANTS
            f.write(f'''
nan = np.nan
A_ = []
mod_fixed_ = []
gaussian_mixture_objects = dict()

cornums = {my_model.cornums}
''')

            f.write(open(x.write_model_(loc=saveloc, tail=tail_x)).read())

    if True:
        # find base for t
        common_t = find_common_integer_sequence(my_data['BJD'])
        if common_t:
            my_data['BJD'] -= common_t

        ## COL
        D = deepcopy(my_data)
        ajuste = res
        OGM = my_model

        # Block selection
        DB_A = [b for b in OGM if b.display_on_data_==True]  # Keplerians
        NDB_A = [b for b in OGM if b.display_on_data_==False]  # Instrumental

        pbar_tot = 1 + len(DB_A)

        pbar = tqdm(total=pbar_tot)
        # data for continuous
        x_c = np.linspace(D['BJD'].min(), D['BJD'].max(), 5000)
        DC = pd.DataFrame({'BJD':x_c, 'RV':np.zeros_like(x_c), 'eRV':np.ones_like(x_c)})
        ### MOVE DATA AROUND
        # Get models which I dont want to display with a line
        # Substract them to the data
        # NDM_A stands for No Display Model
        create_mod(D, NDB_A, '_NDM_A', 0)
        # this uses the original data
        # outputs what is modeled outside keplerians


        import temp_mod_00
        NDM_A_mod = reload(temp_mod_00).my_model


        ndm, ndferr = NDM_A_mod(ajuste)

        # data gets cleaned from no display
        D['RV'] -= ndm
        D['eRV'] = np.sqrt(ndferr)

        # get the residuals
        D['residuals'] = D['RV'].values
        if DB_A:
            create_mod(D, DB_A, '_DM_A', 1)
            # this uses the data with instrumental removed
            # outputs what is modeled with keplerians

            import temp_mod_01
            DM_A_mod = reload(temp_mod_01).my_model


            D['residuals'] -= DM_A_mod(ajuste)[0]

            # Here we are done. We have 3 different datasets
            # display, og-no_display, continuous

    # FULL MODEL
    # this requires a subgrid, for plotting the residuals

    if True:
        if True:
            fig = pl.figure(figsize=fm_figsize)
            gs = gridspec.GridSpec(3, 4)
            if switch_histogram:
                ax = fig.add_subplot(gs[:2, :-1])
                axr = fig.add_subplot(gs[2, :-1], sharex=ax)
                axh = fig.add_subplot(gs[:2, 3], sharey=ax)
                axrh = fig.add_subplot(gs[2, 3], sharey=axr)

            else:
                ax = fig.add_subplot(gs[:2, :])
                axr = fig.add_subplot(gs[2, :], sharex=ax)

            pl.subplots_adjust(hspace=0)
            ax.axhline(0, **fm_axhline_kwargs)
            axr.axhline(0, **fm_axhline_kwargs)

            pl.subplots_adjust(wspace=0.15)

        # First we plot the data
        if True:
            

            for n_ins in range(OGM.nins__):
                mask = D['Flag'] == (n_ins + 1)
                if switch_errors:
                    ax.errorbar(D[mask]['BJD'], D[mask]['RV'], D[mask]['eRV'],
                                c=colors[n_ins], label=OGM.instrument_names[n_ins],
                                **fm_errorbar_kwargs)

                    axr.errorbar(D[mask]['BJD'], D[mask]['residuals'], D[mask]['eRV'],
                                c=colors[n_ins],
                                **fm_errorbar_kwargs)
                else:
                    ax.plot(D[mask]['BJD'], D[mask]['RV'],
                            colors[n_ins]+'o', label=OGM.instrument_names[n_ins])

                    axr.plot(D[mask]['BJD'], D[mask]['residuals'], colors[n_ins]+'o')
                

        if switch_periodogram:
            plot_periodogram(D, options)


        # We set unmodels for uncertainties
        if len(DB_A):
            for b in DB_A:
                if b.parameterisation == 0:
                    #kepmod = Keplerian_Model
                    unkepmod = unKeplerian_Model
                    un_model_name = "unKeplerian_Model"
                    chaos_names = ['Period', 'Amplitude', 'Phase', 'Eccentricity', 'Longitude_Periastron']
                if b.parameterisation == 1:
                    #kepmod = Keplerian_Model_1
                    unkepmod = unKeplerian_Model_1
                    un_model_name = "unKeplerian_Model_1"
                    chaos_names = ['lPeriod', 'Amp_sin', 'Amp_cos', 'Ecc_sin', 'Ecc_cos']
                if b.parameterisation == 2:
                    #kepmod = Keplerian_Model_2
                    unkepmod = unKeplerian_Model_2
                    un_model_name = "unKeplerian_Model_2"
                    chaos_names = ['Period', 'Amplitude', 'Time_Periastron', 'Eccentricity', 'Longitude_Periastron']
                if b.parameterisation == 3:
                    #kepmod = Keplerian_Model_3
                    unkepmod = unKeplerian_Model_3
                    un_model_name = "unKeplerian_Model_3"
                    chaos_names = ['Period', 'Amplitude', 'Time_Periastron', 'Ecc_sin', 'Ecc_cos']

        # Now we plot our line
        if len(DB_A):
            DB_AC = deepcopy(DB_A)

            create_mod(DC, DB_AC, '_DM_AC', 2)

            import temp_mod_02
            DM_AC_mod = reload(temp_mod_02).my_model


            DC['RV'] = DM_AC_mod(ajuste)[0]

            ax.plot(DC['BJD'], DC['RV'], color=rc.fg,
                    ls=fm_model_line['ls'],
                    lw=fm_model_line['lw'])

        if True and switch_histogram:
            nbins = 5
            while nbins < len(D):
                counts, bins = np.histogram(D['RV'], bins=nbins)
                if (counts==0).any():
                    break
                else:
                    nbins += 1

            nbins = 5
            while nbins < len(D):
                counts, bins = np.histogram(D['residuals'], bins=nbins)
                if (counts==0).any():
                    break
                else:
                    nbins += 1

            # PLOT HISTOGRAMS
            axh.hist(D['RV'], bins=nbins-1, orientation='horizontal', ec=rc.fg, lw=fm_hist['lw'])
            axrh.hist(D['residuals'], bins=nbins-1, orientation='horizontal', ec=rc.fg, lw=fm_hist['lw'])
            # HIDE TICKS
            axh.tick_params(axis="x", labelbottom=False, labelsize=fm_tick_xsize)
            axh.tick_params(axis="y", labelleft=False)

            axrh.tick_params(axis="y", labelleft=False)
            axrh.tick_params(axis="x", labelsize=fm_tick_xsize)
            axrh.set_xlabel('Counts', fontsize=fm_label_fs)
            
        # Ticks and labels
        if True:
            ax.tick_params(axis="x", labelbottom=False)
            axr.tick_params(axis="x", labelsize=fm_tick_xsize)

            ax.tick_params(axis="y", labelsize=fm_tick_ysize)
            axr.tick_params(axis="y", labelsize=fm_tick_ysize)

            ax.set_title('Keplerian Model', fontsize=fm_title_fs)
            ax.set_ylabel(r'RVs ($\frac{m}{s}$)', fontsize=fm_label_fs)
            ax.legend(fontsize=fm_legend_fs)#, framealpha=0)

            if common_t:
                axr.set_xlabel(f'BJD (days) + {common_t}', fontsize=fm_label_fs)
            else:
                axr.set_xlabel(f'BJD (days)', fontsize=fm_label_fs)

            axr.set_ylabel(r'Residuals ($\frac{m}{s}$)', fontsize=fm_label_fs)


        # SPINES
        if True:
            for spine in ax.spines.values():
                spine.set_linewidth(fm_frame_lw)
            for spine in axr.spines.values():
                spine.set_linewidth(fm_frame_lw)

            for spine in axh.spines.values():
                spine.set_linewidth(fm_frame_lw)
            for spine in axrh.spines.values():
                spine.set_linewidth(fm_frame_lw)

        fig.savefig(saveplace+'{}.{}'.format('keplerian_model', plot_fmt),
                    bbox_inches='tight')


        pbar.update(1)


    # PHASEFOLD
    for mode in range(True+switch_uncertain):
        # add a tail to the name if uncertainties
        if mode == 0:
            name_tail = ''
        if mode == 1:
            name_tail = '_uncertainties'
            pbar_tot = len(DB_A)
            pbar = tqdm(total=pbar_tot)
        chaos_thetas = []
        nb_ = 0
        for b in DB_A:
            # make grid
            if True:
                fig = pl.figure(figsize=fm_figsize)
                gs = gridspec.GridSpec(3, 4)

                if switch_histogram:
                    ax = fig.add_subplot(gs[:2, :-1])
                    axr = fig.add_subplot(gs[2, :-1], sharex=ax)
                    axh = fig.add_subplot(gs[:2, 3], sharey=ax)
                    axrh = fig.add_subplot(gs[2, 3], sharey=axr)
                else:
                    ax = fig.add_subplot(gs[:2, :])
                    axr = fig.add_subplot(gs[2, :], sharex=ax)

                pl.subplots_adjust(hspace=0)

                ax.axhline(0, **fm_axhline_kwargs)
                axr.axhline(0, **fm_axhline_kwargs)

            pl.subplots_adjust(wspace=0.15)

            # adjust params for different parameterisations
            # now just in period for param 1
            # Get PAE? ## RED
            per = np.exp(b[0].value) if b.parameterisation == 1 else b[0].value
            D_PF = deepcopy(D)

            TB = [deepcopy(b)]

            if True:
                create_mod(D_PF, TB, '_TB', 3)
                import temp_mod_03
                TM_mod = reload(temp_mod_03).my_model

            D_PF['RV_TB'] = TM_mod(ajuste)[0]
            D_PF['RV_D'] = D_PF['residuals'].values + D_PF['RV_TB'].values
            D_PF['eRV_D'] = TM_mod(ajuste)[1]

            D_PF = fold_dataframe(D_PF, per=per)

            ## plot data per instrument
            for n_ins in range(OGM.nins__):
                mask = D_PF['Flag'] == (n_ins + 1)

                if switch_errors:
                    ax.errorbar(D_PF[mask]['BJD'], D_PF[mask]['RV_D'], yerr=D_PF[mask]['eRV'],
                                    c=colors[n_ins], label=OGM.instrument_names[n_ins],
                                    **fm_errorbar_kwargs)

                    axr.errorbar(D_PF[mask]['BJD'], D_PF[mask]['residuals'], yerr=D_PF[mask]['eRV'],
                                c=colors[n_ins],
                                **fm_errorbar_kwargs)
                else:
                    ax.plot(D_PF[mask]['BJD'], D_PF[mask]['RV_D'],
                                colors[n_ins]+'o', label=OGM.instrument_names[n_ins])

                    axr.plot(D_PF[mask]['BJD'], D_PF[mask]['residuals'],
                                colors[n_ins]+'o')

            ### create model line for the phasefold
            xpf_c = np.linspace(D_PF['BJD'].min(), D_PF['BJD'].max(), 5000)
            D_PFC = pd.DataFrame({'BJD':xpf_c, 'RV':np.zeros_like(xpf_c), 'eRV':np.ones_like(xpf_c)})

            TB_C = [deepcopy(b)]

            if True:
                create_mod(D_PFC, TB_C, '_TB_C', 4)
                import temp_mod_04
                TM_C_mod = reload(temp_mod_04).my_model

            D_PFC['RV'] = TM_C_mod(ajuste)[0]


            ## plot phasefold
            if True:
                # get uncertainties
                if mode==1:
                    un_model = un.Model(run=unkepmod,
                                        labels=['BJD (days)', r'RVs $\frac{m}{s}$'],
                                        interpolate=True,
                                        logger_level=u'error',
                                        #postprocess=func
                                        )

                    chaostheta = {}
                    for i in range(len(b)):
                        if posterior_method == 'GM':
                            if b[i].fixed is None:
                                chaostheta[chaos_names[i]] = cp.TruncNormal(lower=b[i].limits[0],
                                                                            upper=b[i].limits[1],
                                                                            mu=b[i].posterior.mixture_mean,
                                                                            sigma=b[i].posterior.mixture_sigma)
                            else:
                                chaostheta[chaos_names[i]] = b[i].value_mean

                    chaos_thetas.append(chaostheta)

                    parameters = un.Parameters(chaostheta)

                    UQ = un.UncertaintyQuantification(model=un_model,
                                                      parameters=parameters,
                                                      logger_level=u'critical',
                                                      logger_filename=unsaveplace+'uncertainpy.log')

                    with nullify_output(suppress_stdout=True, suppress_stderr=True):
                        undata = UQ.quantify(seed=10,
                                             method='pc',
                                             plot=None,
                                             #plot='all',
                                             pc_method='collocation',
                                             logger_level=u'critical',
                                             figure_folder=unsaveplace+'figures',
                                             data_folder=unsaveplace+'data',
                                             single=False)

                    keplerian_data = un.Data('{}data/{}.h5'.format(unsaveplace,
                                                                   un_model_name))

                    untime = undata[un_model_name].time
                    unmean = undata[un_model_name].mean
                    unvariance = undata[un_model_name].variance
                    unpercentile_5 = undata[un_model_name].percentile_5
                    unpercentile_95 = undata[un_model_name].percentile_95
                    unsensitivity = undata[un_model_name].sobol_first

                # Plot model line
                ax.plot(D_PFC['BJD'].values, D_PFC['RV'].values, color=rc.fg,
                        ls=fm_model_line['ls'],
                        lw=fm_model_line['lw'],)

                # plot uncertainties
                if mode == 1:
                    ax.fill_between(untime,
                                    unpercentile_5,
                                    unpercentile_95,
                                    color=rc.fg,
                                    alpha=0.5)


                    if True:
                        figs, axs = pl.subplots(figsize=(8, 6))
                        for i in range(unsensitivity.shape[0]):
                            axs.plot(untime, unsensitivity[i],
                                       linewidth=1.5,
                                       )
                        axs.set_title('First-order Sobol indices')
                        axs.set_xlabel(f'BJD (days)',
                                       fontsize=fm_label_fs)
                        axs.set_ylabel('First-order Sobol indices',
                                       fontsize=fm_label_fs)
                        axs.legend(parameters.get_from_uncertain(),
                                            loc='upper right',
                                            framealpha=0.5)

                        figs.savefig(saveplace+f'sobol_{b.name_+name_tail}.{plot_fmt}',
                                   bbox_inches='tight')
                        pl.close(figs)
                # Plot Histogram Model
                if switch_histogram:
                    nbins = 5
                    while nbins < len(D_PF):
                        counts, bins = np.histogram(D_PF['RV_D'], bins=nbins)
                        if (counts==0).any():
                            break
                        else:
                            nbins += 1

                    axh.hist(D_PF['RV_D'], bins=nbins-1, orientation='horizontal', ec=rc.fg,
                             lw=fm_hist['lw'])

                # Plot histogram residuals
                if switch_histogram:
                    nbins = 5
                    while nbins < len(D_PF):
                            counts, bins = np.histogram(D_PF['residuals'], bins=nbins)
                            if (counts==0).any():
                                break
                            else:
                                nbins += 1
                    axrh.hist(D_PF['residuals'], bins=nbins-1, orientation='horizontal', ec=rc.fg,
                              lw=fm_hist['lw'])

                # Ticks and labels

                if True:
                    ax.tick_params(axis="x", labelbottom=False)
                    axr.tick_params(axis="x", labelsize=fm_tick_xsize)

                    ax.tick_params(axis="y", labelsize=fm_tick_ysize)
                    axr.tick_params(axis="y", labelsize=fm_tick_ysize)
                    
                    if switch_histogram:
                        # HIDE TICKS
                        axh.tick_params(axis="x", labelbottom=False, labelsize=fm_tick_xsize)
                        axh.tick_params(axis="y", labelleft=False)

                        axrh.tick_params(axis="y", labelleft=False)
                        axrh.tick_params(axis="x", labelsize=fm_tick_xsize)
                        axrh.set_xlabel('Counts', fontsize=fm_label_fs)

                                         
                    ax.set_title('Keplerian Model', fontsize=fm_title_fs)
                    ax.set_ylabel(r'RVs ($\frac{m}{s}$)', fontsize=fm_label_fs)
                    ax.legend(fontsize=fm_legend_fs)#, framealpha=0)

                    axr.set_xlabel(f'BJD (days)', fontsize=fm_label_fs)
                    axr.set_ylabel(r'Residuals ($\frac{m}{s}$)', fontsize=fm_label_fs)


                # SPINES
                if True:
                    for spine in ax.spines.values():
                        spine.set_linewidth(fm_frame_lw)
                    for spine in axr.spines.values():
                        spine.set_linewidth(fm_frame_lw)

                    for spine in axh.spines.values():
                        spine.set_linewidth(fm_frame_lw)
                    for spine in axrh.spines.values():
                        spine.set_linewidth(fm_frame_lw)

            pl.savefig(saveplace+f'{b.name_+name_tail}.{plot_fmt}',
                       bbox_inches='tight')

            nb_ += 1

            pbar.update(1)


            # print('MARKER 5')
            if nb_ == len(DB_A):
                pbar.close()

    temp_file_folder = saveloc+'/temp/models/'


    with nullify_output():
        for file in list(set(temp_file_names)):
            try:
                os.system('mv {0} {1}{0}'.format(file, temp_file_folder))
            except Warning:
                print('Couldnt auto-delete temp files')

        for file in list(set(temp_mod_names)):
            try:
                os.system('mv {0} {1}{2}'.format(file, temp_file_folder, file.split('/')[-1]))
            except Warning:
                print('Couldnt auto-delete temp files')

        for file in list(set(temp_dat_names)):
            try:
                os.system('mv {0} {1}{2}'.format(file, temp_file_folder, file.split('/')[-1]))
            except Warning:
                print('Couldnt auto-delete temp files')

    return chaos_thetas


def plot_periodogram(my_data, options, tail_name=''):
    from scipy.signal import lombscargle
    if options is None:
        options = {}

    saveplace = options['saveloc'] + '/plots/'
    plot_fmt = options['format']
    x = my_data['BJD'] - min(my_data['BJD']) + 0.1
    y = my_data['residuals']
    yerr = my_data['eRV']

    # other params
    Nfreq = 20000
    periods = np.linspace(x.min(), x.max()/2, Nfreq)
    ang_freqs = 2 * np.pi / periods

    maxpoints = 5
    ide = np.arange(maxpoints)+1

    TITLE = 'Residuals Periodogram'
    xaxis_label = 'Period (days)'
    yaxis_label = 'Power'
    title_fontsize = 'large'
    label_fontsize = 'medium'
    line_style = '-'
    line_color = rc.fg
    hsize, vsize = 10, 8
    dpi = 80
    xlog = True
    ylog = False

    scatter_marker_style = 'o'
    scatter_size = 40
    scatter_color = '#FF0000'
    scatter_alpha = 1

    method = 0
    t = np.ascontiguousarray(x.values)
    mag = np.ascontiguousarray(y.values)
    #dmag = np.ascontiguousarray(yerr.values)

    if method == 0:
        power = lombscargle(t, mag - np.mean(mag), ang_freqs)
        N = len(t)
        power *= 2 / (N * np.std(mag) ** 2)

    # Plot
    fig, ax = pl.subplots(figsize=(hsize, vsize), dpi=dpi)
    pl.title(TITLE, fontsize=title_fontsize)

    idx = getExtremePoints(power, typeOfExtreme='max', maxPoints=maxpoints)

    pl.plot(periods, power, ls=line_style, c=line_color)
    # fap line

    #ax.annotate('0.1% significance level', (3, 0.13))
    #pl.plot(periods, np.ones_like(periods)*0.12, ls='--', c=line_color, alpha=0.5)

    pl.scatter(periods[idx], power[idx],
                marker=scatter_marker_style,
                s=scatter_size, c=scatter_color,
                alpha=scatter_alpha)

    for i in idx:
        ax.annotate(f' Max = {np.round(periods[i], 2)}', (periods[i]+10, power[i]))

        ax.set_title(TITLE, fontsize=title_fontsize)
        ax.set_xlabel(xaxis_label, fontsize=label_fontsize)
        ax.set_ylabel(yaxis_label, fontsize=label_fontsize)

        if xlog:
            ax.set_xscale('log')
        if ylog:
            ax.set_yscale('log')

    #tabable = np.array([periods[idx][::-1], power[idx][::-1]])
    #taball = np.vstack([ide, tabable])
    #headers = ['Rank', 'Period', 'Power']

    #ax.table(cellText=taball.T, colLabels=headers, loc='top right')

    pl.savefig(f'{saveplace}periodogram{tail_name}.{plot_fmt}')
    pl.close(fig)
# blue verde rojo purp naran cyan brown blue green

import gc

def make_block_plot(foo):
    if _PLATFORM_SYSTEM == 'Darwin':
        matplotlib.use('Agg')
        pass
    
    plot_points, plot_args, index, pltd = foo
    if True:
        '''
        print('THIS IS THE PLOT args START')
        print('index', index)
        print('plot_points', plot_points)
        print('plot_args', plot_args)
        print('THIS IS THE PLOT EXCEPTION START')
        '''
        #raise Exception('debug boi')

    if True:
        if pltd['paper_mode']:
            #matplotlib.use('png')

            pltd['fs_supt'] = 48#24
            pltd['fs_supylabel'] = 44#22

            pl_scatter_alpha = 0.7
            pl_scatter_size = 6#2

            pltd['fs_xlabel'] = 28#14
            fm_frame_lw = 6#3

            fm_tick_xsize = 40#20
            fm_tick_ysize = 40#20

            pltd['format'] = 'png'
            plt_vlines_lw = 4#2

            pl_label_fs = 44#22

            pltd['figsize_xaxis'] = 20#10
            


        ch1, lk0 = plot_points  # chains[t], likes[t]
        b, t = plot_args

        # plot_options as a dict: figsize_xaxis, fs_supt, fs_supylabel, fs_xlabel, pt_fmt
        elongatex = 0
        elongatey = 2 if b.ndim_ == 1 else 0

        fig, axes = pl.subplots(b.ndim_,
                                figsize=(pltd['figsize_xaxis'] + elongatex,
                                                    b.ndim_*6 + elongatey)
                                                    )

        fig.suptitle(f'Posteriors {b.name_}', fontsize=pltd['fs_supt'])
        fig.supylabel('Log Posterior', fontsize=pltd['fs_supylabel'])

        minl, maxl = min(lk0), max(lk0)

        for pi in range(b.ndim_):
            ch0 = ch1[:, b.cpointer[pi]]

            ax = axes if b.ndim_ == 1 else axes[pi]
            ax.scatter(ch0, lk0,
                        c=pltd['colors'][b.bnumber_-1],
                        alpha=pl_scatter_alpha,
                        s=pl_scatter_size)

            param = b[b.C_][pi]
            _param_value_max = param.value_max
            _param_value_mean = param.value_mean
            ax.vlines(_param_value_max,
                        ymin=minl,
                        ymax=maxl,
                        colors=rc.fg,
                        **{'ls':'-',
                            'label':f'max = {np.round(param.value_max, 3)}',
                            'lw':plt_vlines_lw})
            ax.vlines(_param_value_mean,
                        ymin=minl,
                        ymax=maxl,
                        colors=rc.fg,
                        **{'ls':'--',
                            'label':f'mean = {np.round(param.value_mean, 3)}',
                            'lw':plt_vlines_lw})
            ax.set_xlabel(f'{param.name} {param.unit}', fontsize=pl_label_fs)
            ax.tick_params(axis='x', labelsize=fm_tick_xsize, labelrotation=45)
            ax.tick_params(axis='y', labelsize=fm_tick_ysize)
            ax.legend(framealpha=0., fontsize=pltd['fs_xlabel'], loc=1)

            # SPINES
            if True:
                for spine in ax.spines.values():
                    spine.set_linewidth(fm_frame_lw)

        #if pltd['paper_mode']:
            #pl.subplots_adjust(hspace=0.00)

        pl.tight_layout()
        ptfmt = pltd['format']
        mdname = pltd['modes_names']
        pl.savefig(pltd['saveloc']+f'/plots/posteriors/{mdname[0]}/{t}_temp/{b.name_}.{ptfmt}',
                        bbox_inches='tight')

        pl.close()

    #del plot_points
    #del plot_args
    gc.collect()
    pass


from multiprocessing import Pool

def super_plots(chains, likes, options, my_model, temps=1, ncores=None):
    cor = ['C0', 'C1', 'C2', 'C4', 'C5', 'C7', 'C8', 'C9']
    colors = np.array([cor,cor,cor,cor,cor]).flatten()

    modes_names = ['scatter', 'hexbin', 'gaussian']

    saveplace = options['saveloc']

    options['fs_xlabel'] = 10
    options['fs_supylabel'] = 16
    options['figsize_xaxis'] = 12
    options['colors'] = colors
    options['modes_names'] = modes_names

    if ncores is None:
        ncores = _CORES

    # make folders
    for t in range(temps):
        try:
            os.makedirs(saveplace+f'/plots/posteriors/{modes_names[0]}/{t}_temp')
        except:
            pass
    
    plot_pt_list = []
    plot_list = []
    for ti in range(temps):
        for b in my_model:
            if b.ndim_ > 0:
                plot_pt_list.append([chains[ti], likes[ti]])
                plot_list.append([b, ti])

    num_plots = len(plot_list)



    ncores = 5
    tasks = []
    for i in range(num_plots):
        tasks.append([plot_pt_list[i],
                      plot_list[i],
                      i,
                      options])
        if (i+1) % ncores == 0:
            with Pool(ncores) as pool:
                for _ in tqdm(pool.imap_unordered(make_block_plot, tasks), total=len(tasks)):
                    pass

            pl.close('all')
            gc.collect()
            tasks = []
        
        if (i+1) == num_plots:
            with Pool(ncores) as pool:
                for _ in tqdm(pool.imap_unordered(make_block_plot, tasks), total=len(tasks)):
                    pass

            pl.close('all')
            gc.collect()
            tasks = []

        


    #print('THESE ARE THE TASKS')
    #for task in tasks:
    #    print(f'{task}\n')
    #print('THESE ARE THE TASKS\n\n\n\n')
    
    return


def activate_paper_mode():
    # TITLE
    matplotlib.rcParams['font.size'] = 22

    # AXIS
    matplotlib.rcParams['axes.labelsize'] = 22

    # FRAME
    matplotlib.rcParams['axes.linewidth'] = 3

    # errorbar
    matplotlib.rcParams['lines.markersize'] = 7

'''
def plot_posts_master(chains, likes, options, my_model, temps=1, dtp=None):
    from scipy.ndimage.filters import gaussian_filter

    def myplot(x, y, s, bins=500):

        xn = (x - min(x)) / (max(x)- min(x))
        yn = (y - min(y)) / (max(y)- min(y))

        heatmap, xedges, yedges = np.histogram2d(xn, yn, bins=(bins*4, bins))
        heatmap = gaussian_filter(heatmap, sigma=s)


        extent = [0.0, 4.0, 0.0, 1.0]
        #extent = [min(x), max(x), min(y), max(y)]
        return heatmap.T, extent


    cor = ['C0', 'C1', 'C2', 'C4', 'C5', 'C7', 'C8', 'C9']
    colors = np.array([cor,cor,cor,cor,cor]).flatten()

    cma = ['Blues', 'Oranges', 'Greens', 'Reds', 'Purples', 'YlOrBr','PuRd', 'Greys']
    cmas = np.array([cma,cma,cma,cma,cma]).flatten()

    modes_names = ['scatter', 'hexbin', 'gaussian']

    pt_fmt = options['format']
    draw_top_percent = dtp
    figsize_xaxis = 12
    fs_supt = options['fs_supt']
    fs_supylabel = 16
    fs_xlabel = 10
    saveplace = options['saveloc']


    for t in range(temps):
        # make folders
        for mode in options['modes']:
            try:
                os.makedirs(saveplace+f'/plots/posteriors/{modes_names[mode]}/{t}_temp')
            except:
                pass
            
            
        # select samples
        ch = chains[t]
        lk = likes[t]

        # plot the top dtp percent
        if dtp:
            # mask = np.argsort(lk) > int((100-dtp)/100 * (len(lk)-1))
            mask = lk > np.median(lk)
            lk0 = lk[mask]
            ch1 = ch[mask]
        else:
            lk0 = lk
            ch1 = ch


        pbar_tot = np.sum([1 for b in my_model if b.ndim_ != 0])
        pbar_tot *= len(options['modes'])
        pbar = tqdm(total=pbar_tot)
        for b in my_model:
            if b.ndim_ == 0:
                break
            elongatey = 0
            if b.ndim_ == 1:
                elongatey = 1
            
            for mode in options['modes']:
                elongatex = 0
                if mode == 1:
                    elongatex = 2.2

                fig, axes = pl.subplots(b.ndim_, figsize=(figsize_xaxis + elongatex,
                                                          b.ndim_*3 + elongatey))
                fig.suptitle(f'Posteriors {b.name_}', fontsize=fs_supt)
                fig.supylabel('Log Posterior', fontsize=fs_supylabel)

                for pi in range(b.ndim_):
                    ax = axes if b.ndim_ == 1 else axes[pi]

                    ch0 = ch1[:, b.cpointer[pi]]
                    param = b[b.C_][pi]
                    ymin, ymax = min(lk0), max(lk0)


                    _param_value_max = param.value_max
                    _ymin = ymin
                    _ymax = ymax
                    _param_value_mean = param.value_mean

                    if mode == 0:
                        #sup_mat = np.unique(np.column_stack((ch0, lk0)), axis=0)
                        #sup_ch, sup_lk = sup_mat[:, 0], sup_mat[:, 1]
                        ax.scatter(ch0, lk0,
                                    c=colors[b.bnumber_-1],
                                    alpha=0.8)
                    if mode == 1:
                        # MAKE COLORMAP
                        cmap = mk_cmap([colors[b.bnumber_-1]], ncolors=100)

                        hb = ax.hexbin(ch0, lk0, gridsize=(30, 6), cmap=cmap, mincnt=1)
                        cb = fig.colorbar(hb, ax=ax)
                        cb.set_label('log10(N)')

                    if mode == 2:
                        # MAKE COLORMAP
                        cmap = mk_cmap([colors[b.bnumber_-1]], ncolors=100)

                        # MAKE HEATMAP
                        gaussian_sigma = 8
                        img, extent = myplot(ch0, lk0, gaussian_sigma)

                        # PLOT
                        imsh = ax.imshow(img, extent=extent, origin='lower', cmap=cmap)

                        # ACCOMODATE TICKS
                        my_xticks = np.linspace(0.00, 1.00, 9)
                        numsx = my_xticks * (max(ch0)-min(ch0)) / 4 + min(ch0)
                        my_xlabels = np.round(numsx, 3).astype('str')
                        
                        ax.set_xticks(my_xticks)
                        ax.set_xticklabels(my_xlabels, fontsize=11)

                        my_yticks = np.array([0.00, 0.25, 0.50, 0.75, 1.00]) 
                        numsy = my_yticks * (max(lk0)-min(lk0)) + min(lk0)
                        my_ylabels = np.round(numsy, 3).astype('str')
                        ax.set_yticks(my_yticks)
                        ax.set_yticklabels(my_ylabels, fontsize=11)

                        ax.tick_params(axis='x', labelrotation=45)
                        cb = fig.colorbar(imsh, ax=ax)
                        cb.set_label(f'Counts x {len(lk0)}', fontsize=10)

                        _param_value_max = (param.value_max - min(ch0)) / (max(ch0) - min(ch0)) * 4
                        _param_value_mean = (param.value_mean - min(ch0)) / (max(ch0) - min(ch0)) * 4
                        _ymin = 0
                        _ymax = 1

                    ax.vlines(_param_value_max,
                                ymin=_ymin,
                                ymax=_ymax,
                                colors=rc.fg,
                                **{'ls':'-',
                                    'label':f'max = {np.round(param.value_max, 3)}'})
                    ax.vlines(_param_value_mean,
                                ymin=_ymin,
                                ymax=_ymax,
                                colors=rc.fg,
                                **{'ls':'--',
                                    'label':f'mean = {np.round(param.value_mean, 3)}'})

                    ax.set_xlabel(f'{param.name} {param.unit}')
                    ax.tick_params(axis='x', labelrotation=45)
                    #ax2.set_ylabel('Undamped')
                    ax.legend(framealpha=0., fontsize=fs_xlabel)
                pl.tight_layout()
                pl.savefig(saveplace+f'/plots/posteriors/{modes_names[mode]}/{t}_temp/{b.name_}.{pt_fmt}',
                        bbox_inches='tight')

                pl.close('all')
                pbar.update(1)
        pbar.close()

#plot_posts_master(ch, lk, sim.plot_posteriors, sim.model, temps=setup[0])

def plot_posts(chains, likes, saveplace, my_model, temps=1, dtp=100):
    cor = ['C0', 'C1', 'C2', 'C4', 'C5', 'C7', 'C8', 'C9']
    colors = np.array([cor,cor,cor,cor,cor]).flatten()
    pt_fmt = 'png'
    draw_top_percent = dtp
    fs_supt = 20

    for t in range(temps):
        try:
            os.makedirs(saveplace+f'/plots/posteriors/scatter/{t}_temp')
        except:
            pass

        ch = chains[t]
        lk = likes[t]

        #mask = np.argsort(lk) > int((100-dtp)/100 * (len(lk)-1))
        mask = lk > np.median(lk)
        for b in my_model:
            if b.ndim_ == 0:
                break
            fig, axes = pl.subplots(b.ndim_, figsize=(12, b.ndim_*3))
            fig.suptitle(f'Posteriors {b.name_}', fontsize=fs_supt)
            fig.supylabel('Likelihood', fontsize=16)

            lk0 = lk[mask]
            ch1 = ch[mask]
            for pi in range(b.ndim_):
                if b.ndim_ == 1:
                    ax = axes
                else:
                    ax = axes[pi]

                ch0 = ch1[:, b.cpointer[pi]]
                param = b[b.C_][pi]
                ymin, ymax = min(lk0), max(lk0)

                ax.scatter(ch0, lk0,
                            c=colors[b.bnumber_-1],
                            alpha=0.5)

                ax.vlines(param.value_max,
                            ymin=ymin,
                            ymax=ymax,
                            colors=rc.fg,
                            **{'ls':'-',
                                'label':f'max = {np.round(param.value_max, 3)}'})
                ax.vlines(param.value_mean,
                            ymin=ymin,
                            ymax=ymax,
                            colors=rc.fg,
                            **{'ls':'--',
                                'label':f'mean = {np.round(param.value_mean, 3)}'})

                ax.set_xlabel(f'{param.name} {param.unit}')
                ax.tick_params(axis='x', labelrotation=45)
                #ax2.set_ylabel('Undamped')
                ax.legend(framealpha=0., fontsize=10)
            pl.tight_layout()
            pl.savefig(saveplace+f'/plots/posteriors/scatter/{t}_temp/{b.name_}.{pt_fmt}',
                       bbox_inches='tight')

        pl.close('all')


def plot_posts_hexa(chains, likes, saveplace, my_model, temps=1, dtp=100):
    import matplotlib.cm as cm
    cma = ['Blues', 'Oranges', 'Greens', 'Reds', 'Purples', 'YlOrBr','PuRd', 'Greys']
    cmas = np.array([cma,cma,cma,cma,cma]).flatten()
    pt_fmt = 'png'
    fs_supt = 20

    for t in range(temps):
        try:
            os.makedirs(saveplace+f'/plots/posteriors/hexs/{t}_temp')
        except:
            pass

        ch = chains[t]
        lk = likes[t]

        mask = lk > np.median(lk)
        for b in my_model:
            if b.ndim_ == 0:
                break
            fig, axes = pl.subplots(b.ndim_, figsize=(12 + 2.2, b.ndim_*3))
            fig.suptitle(f'Posteriors {b.name_}', fontsize=fs_supt)
            fig.supylabel('Log Posterior', fontsize=16)

            lk0 = lk[mask]
            ch1 = ch[mask]

            for pi in range(b.ndim_):
                if b.ndim_ == 1:
                    ax = axes
                else:
                    ax = axes[pi]

                ch0 = ch1[:, b.cpointer[pi]]


                param = b[b.C_][pi]

                hb = ax.hexbin(ch0, lk0, gridsize=(30, 6), cmap='inferno', mincnt=1)

                #axs.axis([min(ch0), max(ch0), min(lk0), max(lk0)])
                #ax.set_title('Posteriors hexbin')

                cb = fig.colorbar(hb, ax=ax)
                cb.set_label('log10(N)')

                ax.set_xlabel(f'{param.name} {param.unit}')
                ax.tick_params(axis='x', labelrotation=45)
            pl.tight_layout()
            pl.savefig(saveplace+f'/plots/posteriors/hexs/{t}_temp/{b.name_}.{pt_fmt}',
                           bbox_inches='tight')

            pl.close('all')
    pass

#plot_posts_hexa(ch, lk, sim.saveplace, sim.model, temps=setup[0])

def plot_posts_joinplot(chains, likes, saveplace, my_model, temps=1):
    import seaborn as sns

    fs_supt = 20
    pt_fmt = 'png'
    for t in range(temps):
        try:
            os.makedirs(saveplace+f'/plots/hexs/{t}_temp')
        except:
            pass

        ch = chains[t]
        lk = likes[t]
        mask = lk > np.median(lk)

        for b in my_model:
            lk0 = lk[mask]
            ch1 = ch[mask]
            for pi in range(b.ndim_):
                fig, ax = pl.subplots(1, figsize=(12, b.ndim_*3))
                fig.suptitle(f'Posteriors {b.name_}', fontsize=fs_supt)
                fig.supylabel('Likelihood', fontsize=16)

                ch0 = ch1[:, b.cpointer[pi]]
                param = b[b.C_][pi]
                ymin, ymax = min(lk0), max(lk0)

                sns.jointplot(x=ch0, y=lk0, kind='hist')

                ax.set_xlabel(f'{param.name} {param.unit}')
                #ax2.set_ylabel('Undamped')
                #ax.legend(framealpha=0., fontsize=10)
                pl.savefig(saveplace+f'/plots/hexs/{t}_temp/{param.name}.{pt_fmt}',
                       bbox_inches='tight')
                pl.close('all')


def plot_posts_hexa1(chains, likes, saveplace, my_model, temps=1):
    from scipy.ndimage.filters import gaussian_filter
    import matplotlib.cm as cm
    cor = ['C0', 'C1', 'C2', 'C4', 'C5', 'C7', 'C8', 'C9']
    colors = np.array([cor,cor,cor,cor,cor]).flatten()

    pt_fmt = 'png'
    fs_supt = 20
    ndat = len(likes[0]) // 2  # median

    def hex2rgb(hex):
        hex_cleaned = hex.lstrip('#')
        return tuple(int(hex_cleaned[i:i+2], 16) for i in (0, 2 ,4))


    def myplot(x, y, s, bins=500):

        xn = (x - min(x)) / (max(x)- min(x))
        yn = (y - min(y)) / (max(y)- min(y))

        heatmap, xedges, yedges = np.histogram2d(xn, yn, bins=(bins*4, bins))
        heatmap = gaussian_filter(heatmap, sigma=s)


        extent = [0.0, 4.0, 0.0, 1.0]
        #extent = [min(x), max(x), min(y), max(y)]
        return heatmap.T, extent

    for t in range(temps):
        print(f'init temp {t}')
        try:
            os.makedirs(saveplace+f'/plots/posteriors/gaussian/{t}_temp')
        except:
            pass

        ch = chains[t]
        lk = likes[t]

        mask = lk > np.median(lk)

        for b in my_model:
            print(f'    init block {b.name_}')

            lk0 = lk[mask]
            ch1 = ch[mask]
            for pi in range(b.ndim_):

                param = b[b.C_][pi]
                print(f'        init param {param.name}')
                fig, axs = pl.subplots(4, 1, figsize=(12,12))

                ch0 = ch1[:, b.cpointer[pi]]

                sigmas = [8, 16, 32, 64]

                for ax, s in zip(axs.flatten(), sigmas):
                    if s == 0:
                        ax.plot(ch0, lk0, '.', markersize=5)
                        ax.set_title("Scatter plot")
                    else:
                        img, extent = myplot(ch0, lk0, s)
                        bgfg = [rc.bg, rc.fg]
                        for c in bgfg:
                            if c[0] == '#':
                                c = hex2rgb(c)

                        res = [bgfg[0], colors[b.bnumber_-1], bgfg[1]]
                        cmap = plc.LinearSegmentedColormap.from_list('mycmap', res, N=100)

                        imsh = ax.imshow(img, extent=extent, origin='lower', cmap=cmap)
                        ax.set_title("Smoothing with  $\sigma$ = %d" % s, fontsize=16)


                        #nums = ax.get_xticklabels() * (max(ch0)-min(ch0)) + min(ch0) / 4

                        nums = np.linspace(0.00, 1.00, 9) * (max(ch0)-min(ch0)) / 4 + min(ch0)
                        labels = np.round(nums, 3).astype('str')
                        ax.set_xticklabels(labels, fontsize=11)

                        numsy = np.array([0.00, 0.25, 0.50, 0.75, 1.00]) * (max(lk0)-min(lk0)) + min(lk0)
                        labelsy = np.round(numsy, 3).astype('str')
                        ax.set_yticklabels(labelsy, fontsize=11)

                        ax.tick_params(axis='x', labelrotation=45)
                        cb = fig.colorbar(imsh, ax=ax)
                        cb.set_label(f'Counts x {ndat}', fontsize=10)

                        #numsc = cb.ax.get_yticklabels() * ndat
                        #labelscb = np.round(numsc, 3).astype('str')
                        #cb.ax.set_yticklabels(labelscb)

                pl.tight_layout()
                pl.savefig(saveplace+f'/plots/posteriors/gaussian/{t}_temp/{param.name}.{pt_fmt}',
                           bbox_inches='tight')

                pl.close('all')

#plot_posts_hexa1(ch, lk, sim.saveplace, sim.model, temps=setup[0])

#plot_posts_joinplot(ch, lk, sim.saveplace, sim.model, temps=setup[0])
'''

'''
ch = sim.sampler.get_func('get_chain', kwargs={'flat':True, 'discard':sim.reddemcee_discard, 'thin':sim.reddemcee_thin})
lk = sim.sampler.get_func('get_blobs', kwargs={'flat':True, 'discard':sim.reddemcee_discard, 'thin':sim.reddemcee_thin})
pt = sim.sampler.get_func('get_log_prob', kwargs={'flat':True, 'discard':sim.reddemcee_discard, 'thin':sim.reddemcee_thin})

for t in range(setup[0]):
    mask = pt[t] > np.median(pt[t])

    ch[t] = ch[t][mask]
    lk[t] = lk[t][mask]
    pt[t] = pt[t][mask]

super_plots(ch, pt, sim.plot_posteriors, sim.model, temps=setup[0])

plot_posts(ch, lk, sim.saveplace, sim.model, temps=setup[0])
plot_posts_hexa(ch, lk, sim.saveplace, sim.model, temps=setup[0])
plot_posts_hexa1(ch, lk, sim.saveplace, sim.model, temps=setup[0])
'''


'''
figure FULL MODEL

figure
figsize=(10, 8)

axhline
axhline_kwargs

errorbar
errorbar_kwargs

'''


# 1:48 -> 01:33


