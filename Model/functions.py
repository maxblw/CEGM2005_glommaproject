def import_data(file_path):
    import pandas as pd
    df = pd.read_csv(file_path, parse_dates=["date"], index_col="date")
    return df

def set_parameters():
    w_hist = 12 # width histogram
    h_hist = 4  # height histogram

    w_time = 15 # width time series
    h_time = 3  # height time series

    lw = 0.8 # line width
    lc = 'black' # line color
    ms = 7 # marker size
    mc = 'red' # marker color
    mt = 'x'
    alpha = 0.5 # transparency
    return w_hist, h_hist, w_time, h_time, lw, lc, ms, mc, mt, alpha

def plot_discharge(df, savefig=False, plot_timeseries=True, plot_peaks=True, plot_hist=True):
    import matplotlib.pyplot as plt
    from scipy.signal import find_peaks
    w_hist, h_hist, w_time, h_time, lw, lc, ms, mc, mt, alpha = set_parameters()
    data = df[["Q(m3/s)"]].copy()
    data.dropna(inplace=True)

    if plot_timeseries:
        fig, ax = plt.subplots(figsize=(w_time, h_time))
        ax.plot(data.index, data.values, color=lc, linewidth=lw)
        if plot_peaks:
            peaks, _ = find_peaks(data["Q(m3/s)"].values, height=200, distance=32)
            exces = data.iloc[peaks]["Q(m3/s)"].values
            dpeak = data.index[peaks]
            ax.plot(dpeak, exces, marker=mt, color=mc, markersize=ms, linestyle='None')
            ax.set_title(f"Discharge time series with {len(peaks)} peak events")
        else:
            ax.set_title("Discharge time series")
        ax.set_xlabel("Date")
        ax.set_ylabel("Discharge [m3/s]")
        ax.grid()
        ax.set_xlim([data.index.min(), data.index.max()])
        ax.hlines(200, data.index.min(), data.index.max(), color='red', linestyle='--', label='Peak Threshold (200 m3/s)', lw=lw)
        if savefig:
            plt.savefig("..\\Figures\\discharge_analysis_timeseries.png", dpi=300)

    # histogram of peaks
    if plot_hist:
        fig, axes = plt.subplots(1, 2, figsize=(w_hist, h_hist))

        axes[0].hist(data["Q(m3/s)"], bins=20, color='blue', edgecolor='black', alpha=alpha, density=True)
        axes[0].set_title("Histogram of Discharge")
        axes[0].set_xlabel("Discharge [m3/s]")
        axes[0].set_ylabel("Frequency")
        axes[0].grid()

        if plot_peaks:
            axes[1].set_title(f"Histogram of {len(peaks)} Peak Discharge Events")
            axes[1].set_xlabel("Discharge [m3/s]")
            axes[1].hist(exces, bins=10, color='red', edgecolor='black', alpha=alpha, density=True)
            axes[1].grid()

        if savefig:
            plt.savefig("..\\Figures\\discharge_analysis_hist.png", dpi=300)

def plot_temperature(df, savefig=False, plot_timeseries=True, plot_peaks=True, plot_hist=True):
    import matplotlib.pyplot as plt
    from scipy.signal import find_peaks
    w_hist, h_hist, w_time, h_time, lw, lc, ms, mc, mt, alpha = set_parameters()
    data = df[["Tmean [C]"]].copy()
    data.dropna(inplace=True)

    if plot_timeseries:
        fig, ax = plt.subplots(figsize=(w_time, h_time))
        ax.plot(data.index, data.values, color=lc, linewidth=lw)
        if plot_peaks:
            peaks, _ = find_peaks(data["Tmean [C]"].values, height=17, distance=300)
            exces = data.iloc[peaks]["Tmean [C]"].values
            dpeak = data.index[peaks]
            ax.plot(dpeak, exces, marker=mt, color=mc, markersize=ms, linestyle='None')
            ax.set_title(f"Temperature time series with {len(peaks)} peak events")
        else:
            ax.set_title("Temperature time series")
        ax.set_xlabel("Date")
        ax.set_ylabel("Mean Temperature [C]")
        ax.grid()
        ax.set_xlim([data.index.min(), data.index.max()])
        ax.hlines(17, data.index.min(), data.index.max(), color='red', linestyle='--', label='Peak Threshold (17 C)', lw=lw)
        if savefig:
            plt.savefig("..\\Figures\\temperature_analysis_timeseries.png", dpi=300)

    # histogram of peaks
    if plot_hist:
        fig, axes = plt.subplots(1, 2, figsize=(w_hist, h_hist))

        axes[0].hist(data["Tmean [C]"], bins=20, color='blue', edgecolor='black', alpha=alpha, density=True)
        axes[0].set_title("Histogram of Mean Temperature")
        axes[0].set_xlabel("Mean Temperature [C]")
        axes[0].set_ylabel("Frequency")
        axes[0].grid()

        if plot_peaks:
            axes[1].set_title(f"Histogram of {len(peaks)} Peak Temperature Events")
            axes[1].set_xlabel("Mean Temperature [C]")
            axes[1].hist(exces, bins=10, color='red', edgecolor='black')
            axes[1].grid()

        if savefig:
            plt.savefig("..\\Figures\\temperature_analysis_hist.png", dpi=300)

def plot_precipitation(df, savefig=False, plot_timeseries=True, plot_peaks=True, plot_hist=True):
    import matplotlib.pyplot as plt
    from scipy.signal import find_peaks
    ### precipitation plottings ###
    thresh = 28
    w_hist, h_hist, w_time, h_time, lw, lc, ms, mc, mt, alpha = set_parameters()
    data = df[["precip [mm/day]"]].copy()

    # timeseries with peaks
    if plot_timeseries:
        fig, ax = plt.subplots(figsize=(w_time, h_time))
        ax.plot(data.index, data.values, color=lc, linewidth=lw)
        if plot_peaks:
            peaks, _ = find_peaks(data["precip [mm/day]"].values, height=thresh, distance=100)
            exces = data.iloc[peaks]["precip [mm/day]"].values
            dpeak = data.index[peaks]
            ax.plot(dpeak, exces, marker=mt, color=mc, markersize=ms, linestyle='None')
            ax.set_title(f"Precipitation time series with {len(peaks)} peak events")
        else:
            ax.set_title("Precipitation time series")
        ax.set_xlabel("Date")
        ax.set_ylabel("Precipitation [mm/day]")
        ax.grid()
        ax.set_xlim([data.index.min(), data.index.max()])

        ax.hlines(thresh, data.index.min(), data.index.max(), color='red', linestyle='--', label=f'Peak Threshold ({thresh} mm/day)', lw=lw)
        if savefig:
            plt.savefig("..\\Figures\\precipitation_analysis_timeseries.png", dpi=300)

    if plot_hist:
    # histogram of peaks
        fig, axes = plt.subplots(1, 2, figsize=(w_hist, h_hist))
        axes[0].hist(data["precip [mm/day]"], bins=20, color='blue', edgecolor='black', alpha=alpha, density=True)
        axes[0].set_title("Histogram of Precipitation")
        axes[0].set_xlabel("Precipitation [mm/day]")
        axes[0].set_ylabel("Frequency")
        axes[0].grid()
        if plot_peaks:
            axes[1].set_title(f"Histogram of {len(peaks)} Peak Precipitation Events")
            axes[1].set_xlabel("Precipitation [mm/day]")
            axes[1].hist(exces, bins=10, color='red', edgecolor='black', alpha=alpha, density=True)
            axes[1].grid()
        if savefig:
            plt.savefig("..\\Figures\\precipitation_analysis_hist.png", dpi=300)

def plot_snowdepth(df, savefig=False, plot_timeseries=True, plot_peaks=True, plot_hist=True, plot_monthly=True):
    import matplotlib.pyplot as plt
    from scipy.signal import find_peaks
    w_hist, h_hist, w_time, h_time, lw, lc, ms, mc, mt, alpha = set_parameters()
    data = df[["Snowpack [m]"]].copy()
    data.dropna(inplace=True)

    data_monthly = data.groupby(data.index.month).mean()

    if plot_timeseries:
        fig, axes = plt.subplots(2, figsize=(w_time, h_time * 2), layout='tight')
        axes[0].plot(data.index, data.values, color=lc, linewidth=lw)
        axes[0].set_title(f"Snow Pack time series")
        axes[0].set_xlabel("Date")
        axes[0].set_ylabel("Snow Pack [m]")
        axes[0].grid()
        axes[0].set_xlim([data[data > 0].index.min(), data[data > 0].index.max()])

        diff = data["Snowpack [m]"].diff()
        axes[1].plot(diff.index, diff.values, color=lc, linewidth=lw)

        if plot_peaks:
            distance_peak = 30
            thresh = 0.015
            neg_peaks, _ = find_peaks(-diff.values, height=thresh, distance=distance_peak)
            neg_exces = diff.iloc[neg_peaks].values
            neg_dpeak = diff.index[neg_peaks]
            peaks_snowmelt, _ = find_peaks(diff.values, height=thresh, distance=distance_peak)
            exces_snowmelt = diff.iloc[peaks_snowmelt].values
            dpeak_snowmelt = diff.index[peaks_snowmelt]
            axes[1].plot(dpeak_snowmelt, exces_snowmelt, marker=mt, color=mc, markersize=ms, linestyle='None')
            axes[1].plot(neg_dpeak, neg_exces, marker=mt, color='blue', markersize=ms, linestyle='None')
            axes[1].set_title(f"Differential in Snow Pack time series, threshold={thresh} m, distance={distance_peak} days")
            axes[1].hlines(thresh, data.index.min(), data.index.max(), color='red', linestyle='--', label=f'Peak Threshold ({thresh} m/day)', lw=lw)
            axes[1].hlines(-thresh, data.index.min(), data.index.max(), color='blue', linestyle='--', label=f'Negative Peak Threshold (-{thresh} m/day)', lw=lw)
        else:
            axes[1].set_title("Differential in Snow Pack time series")

        axes[1].set_xlabel("Date")
        axes[1].set_ylabel("Snow Pack Change [m/day]")
        axes[1].grid()
        axes[1].set_xlim([data[data > 0].index.min(), data[data > 0].index.max()])

    if plot_hist:
        fig, axes = plt.subplots(1, 3, figsize=(w_hist, h_hist))
        axes[0].hist(neg_exces, bins=20, color='red', edgecolor='black', alpha=alpha, density=True)
        axes[0].set_title(f"Histogram of left Tail of {len(neg_exces)} Events")
        axes[0].set_xlabel("Snow Pack Change [m/day]")
        axes[0].set_ylabel("Frequency")
        axes[0].grid()

        axes[1].hist(diff, bins=20, color='blue', edgecolor='black', alpha=alpha, density=True)
        axes[1].set_title("Histogram of Snow Pack Change")
        axes[1].set_xlabel("Snow Pack Change [m/day]")
        axes[1].set_ylabel("Frequency")
        axes[1].grid()
        if plot_peaks:
            axes[2].set_title(f"Histogram Right Tail of {len(peaks_snowmelt)} Events")
            axes[2].set_xlabel("Snow Pack Change [m/day]")
            axes[2].hist(exces_snowmelt, bins=10, color='red', edgecolor='black', alpha=alpha, density=True)
            axes[2].grid()
        if savefig:
            plt.savefig("..\\Figures\\snowpack_differential_analysis_hist.png", dpi=300)

    if plot_monthly:
        fig, ax = plt.subplots(figsize=(w_time, h_time))
        ax.bar(data_monthly.index, data_monthly["Snowpack [m]"].values, color='red', alpha=alpha, edgecolor='black')
        ax.grid()
        ax.set_title("Average Monthly Snow Pack [m]")
        ax.set_xlabel("Month")
        ax.set_ylabel("Snow Pack [m]")
        if savefig:
            plt.savefig("..\\Figures\\snowpack_analysis_monthly.png", dpi=300)
        plt.show()

def plot_all(df, savefig=False, dropna=True):
    import matplotlib.pyplot as plt
    if dropna:
        df = df.dropna()
    num_plots = df.shape[1]
    fig, axes = plt.subplots(num_plots, 1, figsize=(10, num_plots * 3))
    for i, column in enumerate(df.columns):
        axes[i].plot(df.index, df[column], color='black', linewidth=1)
        axes[i].set_title(f"{column} over Time")
        axes[i].set_ylabel(column)
        axes[i].grid(True)
        if not dropna:
            xmin = df[column].dropna().index.min()
            xmax = df[column].dropna().index.max()
            axes[i].set_xlim([xmin, xmax])
        else:
            axes[i].set_xlim([df.index.min(), df.index.max()])
    axes[-1].set_xlabel("Date")
    plt.tight_layout()
    if savefig:
        plt.savefig("..\\Figures\\all_variables_timeseries.png", dpi=300)