# coding=utf-8
import numpy as np
from matplotlib import mlab
from matplotlib import pyplot
from matplotlib import cbook


def draw_specgram(x, NFFT=256, Fs=2, Fc=0, detrend=mlab.detrend_none,
                  window=mlab.window_hanning, noverlap=128, cmap=None, xextent=None,
                  pad_to=None, sides='default', scale_by_freq=None, hold=None,
                  **kwargs):
    ax = pyplot.gca()
    # allow callers to override the hold state by passing hold=True|False
    washold = ax.ishold()

    if hold is not None:
        ax.hold(hold)
    try:
        ret = specgram1(x, NFFT=NFFT, Fs=Fs, Fc=Fc, detrend=detrend,
                        window=window, noverlap=noverlap, cmap=cmap,
                        xextent=xextent, pad_to=pad_to, sides=sides,
                        scale_by_freq=scale_by_freq, **kwargs)

        pyplot.draw_if_interactive()
    finally:
        ax.hold(washold)
    pyplot.sci(ret[-1])
    return ret


def specgram1(self, x, NFFT=256, Fs=2, Fc=0, detrend=mlab.detrend_none,
              window=mlab.window_hanning, noverlap=128,
              cmap=None, xextent=None, pad_to=None, sides='default',
              scale_by_freq=None, **kwargs):
    """
        Plot a spectrogram.

        Call signature::

          specgram(x, NFFT=256, Fs=2, Fc=0, detrend=mlab.detrend_none,
                   window=mlab.window_hanning, noverlap=128,
                   cmap=None, xextent=None, pad_to=None, sides='default',
                   scale_by_freq=None, **kwargs)

        Вычисление и построение спектрограммы данных *x*.  Данные делятся на сегменты длины
        *NFFT* и для них вычисляется Плотность спектральной мощности.
        Окна Ханнинга применяются посегментно с перекрытием равным *noverlap*.
        Цветом обозначена мощность в децибелах

        %(PSD)s

          *noverlap*: integer
            Число элементов в перекрытии окон (по умолчанию 128)

          *Fc*: integer
            The center frequency of *x* (defaults to 0), which offsets
            the y extents of the plot to reflect the frequency range used
            when a signal is acquired and then filtered and downsampled to
            baseband.

          *cmap*:
            A :class:`matplotlib.colors.Colormap` instance; if *None*, use
            default determined by rc

          *xextent*:
            The image extent along the x-axis. xextent = (xmin,xmax)
            The default is (0,max(bins)), where bins is the return
            value from :func:`~matplotlib.mlab.specgram`

          *kwargs*:

            Additional kwargs are passed on to imshow which makes the
            specgram image

          Return value is (*Pxx*, *freqs*, *bins*, *im*):

          - *bins* массив временных точек
          - *freqs* массив частот
          - *Pxx* массив мощностей вида `(len(times), len(freqs))`
          - *im* is a :class:`~matplotlib.image.AxesImage` instance

        .. note::

            Если в данные только действительные, то и отображаться будет
            только положительный спектр, иначе оба.
            Изменено может быть с помощью переменной *sides*

        Also note that while the plot is in dB, the *Pxx* array returned is
        linear in power.

        **Example:**

        .. plot:: mpl_examples/pylab_examples/specgram_demo.py
        """
    if not self._hold:
        self.cla()

    Pxx, freqs, bins = specgram2(x, NFFT, Fs, detrend,
                                 window, noverlap, pad_to, sides, scale_by_freq)

    Z = 10. * np.log10(Pxx)
    Z = np.flipud(Z)

    if xextent is None:
        xextent = 0, np.amax(bins)
    xmin, xmax = xextent
    freqs += Fc
    extent = xmin, xmax, freqs[0], freqs[-1]
    im = self.imshow(Z, cmap, extent=extent, **kwargs)
    self.axis('auto')

    return Pxx, freqs, bins, im


def specgram2(x, NFFT=256, Fs=2, detrend=mlab.detrend_none, window=mlab.window_hanning,
              noverlap=128, pad_to=None, sides='default', scale_by_freq=None):
    """
    Compute a spectrogram of data in *x*.  Data are split into *NFFT*
    length segments and the PSD of each section is computed.  The
    windowing function *window* is applied to each segment, and the
    amount of overlap of each segment is specified with *noverlap*.

    If *x* is real (i.e. non-complex) only the spectrum of the positive
    frequencie is returned.  If *x* is complex then the complete
    spectrum is returned.

    %(PSD)s

      *noverlap*: integer
          The number of points of overlap between blocks.  The default value
          is 128.

    Returns a tuple (*Pxx*, *freqs*, *t*):

         - *Pxx*: 2-D array, columns are the periodograms of
           successive segments

         - *freqs*: 1-D array of frequencies corresponding to the rows
           in Pxx

         - *t*: 1-D array of times corresponding to midpoints of
           segments.

    .. seealso::

        :func:`psd`
            :func:`psd` differs in the default overlap; in returning
            the mean of the segment periodograms; and in not returning
            times.
    """
    assert (NFFT > noverlap)

    Pxx, freqs, t = _spectral_helper(x, x, NFFT, Fs, detrend, window,
                                     noverlap, pad_to, sides, scale_by_freq)
    Pxx = Pxx.real  # Needed since helper implements generically

    return Pxx, freqs, t


def _spectral_helper(x, y, NFFT=256, Fs=2, detrend=mlab.detrend_none,
                     window=mlab.window_hanning, noverlap=0, pad_to=None, sides='default',
                     scale_by_freq=None):
    # The checks for if y is x are so that we can use the same function to
    # implement the core of psd(), csd(), and spectrogram() without doing
    # extra calculations.  We return the unaveraged Pxy, freqs, and t.
    same_data = y is x

    # Make sure we're dealing with a numpy array. If y and x were the same
    # object to start with, keep them that way
    x = np.asarray(x)
    if not same_data:
        y = np.asarray(y)
    else:
        y = x

    # zero pad x and y up to NFFT if they are shorter than NFFT
    if len(x) < NFFT:
        n = len(x)
        x = np.resize(x, (NFFT,))
        x[n:] = 0

    if not same_data and len(y) < NFFT:
        n = len(y)
        y = np.resize(y, (NFFT,))
        y[n:] = 0

    if pad_to is None:
        pad_to = NFFT

    if scale_by_freq is None:
        scale_by_freq = True

    # For real x, ignore the negative frequencies unless told otherwise
    if (sides == 'default' and np.iscomplexobj(x)) or sides == 'twosided':
        numFreqs = pad_to
        scaling_factor = 1.
    elif sides in ('default', 'onesided'):
        numFreqs = pad_to // 2 + 1
        scaling_factor = 2.
    else:
        raise ValueError("sides must be one of: 'default', 'onesided', or "
                         "'twosided'")

    if cbook.iterable(window):
        assert (len(window) == NFFT)
        windowVals = window
    else:
        windowVals = window(np.ones((NFFT,), x.dtype))

    step = NFFT - noverlap
    ind = np.arange(0, len(x) - NFFT + 1, step)
    n = len(ind)
    Pxy = np.zeros((numFreqs, n), np.complex_)

    # do the ffts of the slices
    for i in range(n):
        thisX = x[ind[i]:ind[i] + NFFT]
        thisX = windowVals * detrend(thisX)
        fx = np.fft.fft(thisX, n=pad_to)

        if same_data:
            fy = fx
        else:
            thisY = y[ind[i]:ind[i] + NFFT]
            thisY = windowVals * detrend(thisY)
            fy = np.fft.fft(thisY, n=pad_to)
        Pxy[:, i] = np.conjugate(fx[:numFreqs]) * fy[:numFreqs]

    # Scale the spectrum by the norm of the window to compensate for
    # windowing loss; see Bendat & Piersol Sec 11.5.2.
    Pxy /= (np.abs(windowVals) ** 2).sum()

    # Also include scaling factors for one-sided densities and dividing by the
    # sampling frequency, if desired. Scale everything, except the DC component
    # and the NFFT/2 component:
    Pxy[1:-1] *= scaling_factor

    # MATLAB divides by the sampling frequency so that density function
    # has units of dB/Hz and can be integrated by the plotted frequency
    # values. Perform the same scaling here.
    if scale_by_freq:
        Pxy /= Fs

    t = 1. / Fs * (ind + NFFT / 2.)
    freqs = float(Fs) / pad_to * np.arange(numFreqs)

    if (np.iscomplexobj(x) and sides == 'default') or sides == 'twosided':
        # center the frequency range at zero
        freqs = np.concatenate((freqs[numFreqs // 2:] - Fs, freqs[:numFreqs // 2]))
        Pxy = np.concatenate((Pxy[numFreqs // 2:, :], Pxy[:numFreqs // 2, :]), 0)

    return Pxy, freqs, t

def window_hanning(x):
    "return x times the hanning window of len(x)"
    return np.hanning(len(x))*x

def hanning(M):
    """
    Return the Hanning window.

    The Hanning window is a taper formed by using a weighted cosine.

    Parameters
    ----------
    M : int
        Number of points in the output window. If zero or less, an
        empty array is returned.

    Returns
    -------
    out : ndarray, shape(M,)
        The window, with the maximum value normalized to one (the value
        one appears only if `M` is odd).

    See Also
    --------
    bartlett, blackman, hamming, kaiser

    Notes
    -----
    The Hanning window is defined as

    .. math::  w(n) = 0.5 - 0.5cos\\left(\\frac{2\\pi{n}}{M-1}\\right)
               \\qquad 0 \\leq n \\leq M-1

    The Hanning was named for Julius van Hann, an Austrian meteorologist.
    It is also known as the Cosine Bell. Some authors prefer that it be
    called a Hann window, to help avoid confusion with the very similar
    Hamming window.

    Most references to the Hanning window come from the signal processing
    literature, where it is used as one of many windowing functions for
    smoothing values.  It is also known as an apodization (which means
    "removing the foot", i.e. smoothing discontinuities at the beginning
    and end of the sampled signal) or tapering function.

    References
    ----------
    .. [1] Blackman, R.B. and Tukey, J.W., (1958) The measurement of power
           spectra, Dover Publications, New York.
    .. [2] E.R. Kanasewich, "Time Sequence Analysis in Geophysics",
           The University of Alberta Press, 1975, pp. 106-108.
    .. [3] Wikipedia, "Window function",
           http://en.wikipedia.org/wiki/Window_function
    .. [4] W.H. Press,  B.P. Flannery, S.A. Teukolsky, and W.T. Vetterling,
           "Numerical Recipes", Cambridge University Press, 1986, page 425.

    """
    if M < 1:
        return np.array([])
    if M == 1:
        return np.ones(1, float)
    n = np.arange(0, M)
    return 0.5-0.5*np.cos(2.0*np.pi*n/(M-1))