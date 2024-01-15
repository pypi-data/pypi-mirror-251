#
# This file is part of pyspex
#
# https://github.com/rmvanhees/pyspex.git
#
# Copyright (c) 2019-2023 SRON - Netherlands Institute for Space Research
#    All Rights Reserved
#
# License:  BSD-3-Clause
"""Defines the Helios spectrum, used at SRON."""
from __future__ import annotations

__all__ = ["helios_spectrum"]

import numpy as np
import xarray as xr

# - global parameters ------------------------------
HELIOS_ATTRS = {
    "source": "Helios",
    "setup.Port": "A",
    "setup.Lamp": "HES-150",
    "setup.Output": "100%",
    "setup.Date": "03-Sept-2019",
    "lamp.Port": "A",
    "lamp.Output": "100%",
    "lamp.Voltage": "19.6177 V",
    "lamp.Current": "6.056 A",
    "lamp.CCT": "2998 K",
    "lamp.Luminance": "14070 Cd/m^2",
    "lamp.Illuminance": "44200 lux",
    "lamp.Luminance_uncertainty": "156700 Cd/m^2",
    "lamp.Luminance_relative_uncertainty": "1.114%",
    "detector.Port": "Z",
    "detector.Open": "3.711E-4 A",
    "detector.Pinhole": "3.662E-6 A",
    "detector.Filter": "2.899E-5 A",
    "calib.Port": "Z",
    "calib.Open": "3.793E+7 Cd/(m^2 A)",
    "calib.Filter": "4.855E+8 Cd/(m^2 A)",
    "calib.Pinhole": "3.843E+9 Cd/(m^2 A)",
}

HELIOS_SPECTRUM = [
    4.92e00,
    5.12e00,
    5.33e00,
    5.55e00,
    5.76e00,
    5.98e00,
    6.20e00,
    6.42e00,
    6.64e00,
    6.88e00,
    7.14e00,
    7.39e00,
    7.64e00,
    7.89e00,
    8.14e00,
    8.39e00,
    8.64e00,
    8.90e00,
    9.16e00,
    9.44e00,
    9.72e00,
    1.00e01,
    1.03e01,
    1.05e01,
    1.08e01,
    1.11e01,
    1.14e01,
    1.17e01,
    1.20e01,
    1.24e01,
    1.27e01,
    1.31e01,
    1.36e01,
    1.40e01,
    1.45e01,
    1.50e01,
    1.55e01,
    1.60e01,
    1.65e01,
    1.70e01,
    1.75e01,
    1.80e01,
    1.84e01,
    1.89e01,
    1.94e01,
    1.99e01,
    2.03e01,
    2.09e01,
    2.14e01,
    2.20e01,
    2.26e01,
    2.32e01,
    2.39e01,
    2.46e01,
    2.55e01,
    2.63e01,
    2.71e01,
    2.78e01,
    2.86e01,
    2.94e01,
    3.03e01,
    3.12e01,
    3.21e01,
    3.30e01,
    3.39e01,
    3.47e01,
    3.56e01,
    3.64e01,
    3.73e01,
    3.81e01,
    3.88e01,
    3.96e01,
    4.04e01,
    4.11e01,
    4.18e01,
    4.25e01,
    4.32e01,
    4.40e01,
    4.47e01,
    4.54e01,
    4.62e01,
    4.71e01,
    4.80e01,
    4.88e01,
    4.95e01,
    5.02e01,
    5.09e01,
    5.16e01,
    5.25e01,
    5.34e01,
    5.43e01,
    5.51e01,
    5.60e01,
    5.69e01,
    5.77e01,
    5.86e01,
    5.95e01,
    6.05e01,
    6.14e01,
    6.24e01,
    6.34e01,
    6.44e01,
    6.54e01,
    6.65e01,
    6.76e01,
    6.87e01,
    6.97e01,
    7.08e01,
    7.20e01,
    7.31e01,
    7.43e01,
    7.55e01,
    7.66e01,
    7.77e01,
    7.88e01,
    7.99e01,
    8.10e01,
    8.21e01,
    8.32e01,
    8.44e01,
    8.55e01,
    8.66e01,
    8.77e01,
    8.89e01,
    9.00e01,
    9.11e01,
    9.23e01,
    9.35e01,
    9.47e01,
    9.59e01,
    9.71e01,
    9.83e01,
    9.95e01,
    1.01e02,
    1.02e02,
    1.03e02,
    1.04e02,
    1.06e02,
    1.07e02,
    1.08e02,
    1.09e02,
    1.10e02,
    1.12e02,
    1.13e02,
    1.14e02,
    1.15e02,
    1.16e02,
    1.18e02,
    1.19e02,
    1.20e02,
    1.21e02,
    1.22e02,
    1.24e02,
    1.25e02,
    1.26e02,
    1.27e02,
    1.29e02,
    1.30e02,
    1.31e02,
    1.32e02,
    1.34e02,
    1.35e02,
    1.36e02,
    1.37e02,
    1.38e02,
    1.39e02,
    1.41e02,
    1.42e02,
    1.43e02,
    1.44e02,
    1.45e02,
    1.47e02,
    1.48e02,
    1.49e02,
    1.50e02,
    1.51e02,
    1.53e02,
    1.54e02,
    1.55e02,
    1.56e02,
    1.58e02,
    1.59e02,
    1.60e02,
    1.61e02,
    1.62e02,
    1.64e02,
    1.65e02,
    1.66e02,
    1.67e02,
    1.68e02,
    1.70e02,
    1.71e02,
    1.72e02,
    1.73e02,
    1.75e02,
    1.76e02,
    1.77e02,
    1.78e02,
    1.80e02,
    1.81e02,
    1.82e02,
    1.83e02,
    1.84e02,
    1.86e02,
    1.87e02,
    1.88e02,
    1.90e02,
    1.91e02,
    1.92e02,
    1.93e02,
    1.95e02,
    1.96e02,
    1.97e02,
    1.98e02,
    1.99e02,
    2.00e02,
    2.01e02,
    2.03e02,
    2.04e02,
    2.05e02,
    2.06e02,
    2.07e02,
    2.08e02,
    2.09e02,
    2.11e02,
    2.12e02,
    2.13e02,
    2.14e02,
    2.15e02,
    2.16e02,
    2.17e02,
    2.19e02,
    2.20e02,
    2.21e02,
    2.22e02,
    2.23e02,
    2.24e02,
    2.26e02,
    2.27e02,
    2.28e02,
    2.29e02,
    2.30e02,
    2.31e02,
    2.32e02,
    2.34e02,
    2.35e02,
    2.36e02,
    2.37e02,
    2.38e02,
    2.39e02,
    2.40e02,
    2.42e02,
    2.43e02,
    2.44e02,
    2.45e02,
    2.46e02,
    2.47e02,
    2.48e02,
    2.49e02,
    2.50e02,
    2.51e02,
    2.52e02,
    2.53e02,
    2.54e02,
    2.55e02,
    2.56e02,
    2.57e02,
    2.58e02,
    2.58e02,
    2.59e02,
    2.60e02,
    2.61e02,
    2.62e02,
    2.63e02,
    2.64e02,
    2.65e02,
    2.66e02,
    2.67e02,
    2.69e02,
    2.70e02,
    2.71e02,
    2.72e02,
    2.73e02,
    2.74e02,
    2.75e02,
    2.76e02,
    2.76e02,
    2.77e02,
    2.78e02,
    2.79e02,
    2.80e02,
    2.81e02,
    2.81e02,
    2.82e02,
    2.83e02,
    2.84e02,
    2.85e02,
    2.86e02,
    2.87e02,
    2.88e02,
    2.88e02,
    2.89e02,
    2.90e02,
    2.91e02,
    2.92e02,
    2.93e02,
    2.94e02,
    2.94e02,
    2.95e02,
    2.96e02,
    2.97e02,
    2.98e02,
    2.98e02,
    2.99e02,
    3.00e02,
    3.00e02,
    3.01e02,
    3.02e02,
    3.02e02,
    3.03e02,
    3.04e02,
    3.05e02,
    3.06e02,
    3.06e02,
    3.07e02,
    3.08e02,
    3.09e02,
    3.10e02,
    3.10e02,
    3.11e02,
    3.12e02,
    3.12e02,
    3.13e02,
    3.13e02,
    3.14e02,
    3.15e02,
    3.15e02,
    3.16e02,
    3.17e02,
    3.17e02,
    3.18e02,
    3.19e02,
    3.19e02,
    3.20e02,
    3.20e02,
    3.21e02,
    3.22e02,
    3.22e02,
    3.23e02,
    3.23e02,
    3.24e02,
    3.24e02,
    3.25e02,
    3.26e02,
    3.26e02,
    3.27e02,
    3.27e02,
    3.28e02,
    3.28e02,
    3.28e02,
    3.29e02,
    3.29e02,
    3.30e02,
    3.30e02,
    3.30e02,
    3.31e02,
    3.31e02,
    3.31e02,
    3.32e02,
    3.32e02,
    3.32e02,
    3.32e02,
    3.33e02,
    3.33e02,
    3.33e02,
    3.33e02,
    3.33e02,
    3.34e02,
    3.34e02,
    3.34e02,
    3.34e02,
    3.34e02,
    3.34e02,
    3.34e02,
    3.35e02,
    3.35e02,
    3.35e02,
    3.35e02,
    3.35e02,
    3.35e02,
    3.35e02,
    3.35e02,
    3.35e02,
    3.35e02,
    3.34e02,
    3.34e02,
    3.34e02,
    3.34e02,
    3.34e02,
    3.34e02,
    3.34e02,
    3.34e02,
    3.34e02,
    3.33e02,
    3.33e02,
    3.33e02,
    3.33e02,
    3.32e02,
    3.32e02,
    3.32e02,
    3.31e02,
    3.31e02,
    3.30e02,
    3.30e02,
    3.29e02,
    3.29e02,
    3.28e02,
    3.28e02,
    3.27e02,
    3.27e02,
    3.26e02,
    3.26e02,
    3.25e02,
    3.24e02,
    3.24e02,
    3.23e02,
    3.22e02,
    3.22e02,
    3.21e02,
    3.20e02,
    3.19e02,
    3.19e02,
    3.18e02,
    3.17e02,
    3.16e02,
    3.16e02,
    3.15e02,
    3.14e02,
    3.13e02,
    3.12e02,
    3.11e02,
    3.11e02,
    3.10e02,
    3.09e02,
    3.08e02,
    3.07e02,
    3.06e02,
    3.05e02,
    3.04e02,
    3.03e02,
    3.02e02,
    3.01e02,
    3.01e02,
    3.00e02,
    2.99e02,
    2.98e02,
    2.97e02,
    2.96e02,
    2.95e02,
    2.94e02,
    2.94e02,
    2.93e02,
    2.92e02,
    2.91e02,
    2.90e02,
    2.89e02,
    2.89e02,
    2.88e02,
    2.87e02,
    2.86e02,
    2.86e02,
    2.85e02,
    2.85e02,
    2.84e02,
    2.84e02,
    2.83e02,
    2.82e02,
    2.82e02,
    2.82e02,
    2.81e02,
    2.81e02,
    2.80e02,
    2.80e02,
    2.79e02,
    2.79e02,
    2.79e02,
    2.78e02,
    2.78e02,
    2.78e02,
    2.77e02,
    2.77e02,
    2.77e02,
    2.77e02,
    2.77e02,
    2.77e02,
    2.77e02,
    2.77e02,
    2.77e02,
    2.77e02,
    2.77e02,
    2.77e02,
    2.77e02,
    2.77e02,
    2.77e02,
    2.77e02,
    2.77e02,
    2.77e02,
    2.77e02,
    2.78e02,
    2.78e02,
    2.78e02,
    2.79e02,
    2.79e02,
    2.80e02,
    2.80e02,
    2.81e02,
    2.82e02,
    2.82e02,
    2.83e02,
    2.84e02,
    2.84e02,
    2.85e02,
    2.85e02,
    2.86e02,
    2.86e02,
    2.87e02,
    2.87e02,
    2.88e02,
    2.89e02,
    2.89e02,
    2.90e02,
    2.91e02,
    2.92e02,
    2.92e02,
    2.93e02,
    2.94e02,
    2.95e02,
    2.96e02,
    2.96e02,
    2.97e02,
    2.98e02,
    2.99e02,
    3.00e02,
    3.00e02,
    3.01e02,
    3.02e02,
    3.03e02,
    3.04e02,
    3.05e02,
    3.06e02,
    3.07e02,
    3.08e02,
    3.09e02,
    3.10e02,
    3.11e02,
    3.11e02,
    3.12e02,
    3.13e02,
    3.14e02,
    3.15e02,
    3.16e02,
    3.17e02,
    3.18e02,
    3.19e02,
    3.20e02,
    3.21e02,
    3.22e02,
    3.23e02,
    3.24e02,
    3.25e02,
    3.26e02,
    3.27e02,
    3.28e02,
    3.29e02,
    3.30e02,
    3.30e02,
    3.31e02,
    3.32e02,
    3.33e02,
    3.34e02,
    3.34e02,
    3.35e02,
    3.36e02,
    3.36e02,
    3.37e02,
    3.38e02,
    3.38e02,
    3.39e02,
    3.40e02,
    3.41e02,
    3.41e02,
    3.42e02,
    3.43e02,
    3.43e02,
    3.44e02,
    3.45e02,
    3.46e02,
    3.47e02,
    3.47e02,
    3.48e02,
    3.49e02,
    3.49e02,
    3.50e02,
    3.50e02,
    3.51e02,
    3.52e02,
    3.52e02,
    3.53e02,
    3.53e02,
    3.54e02,
    3.54e02,
    3.55e02,
    3.55e02,
    3.56e02,
    3.56e02,
    3.57e02,
    3.57e02,
    3.58e02,
    3.58e02,
    3.59e02,
    3.59e02,
    3.59e02,
    3.60e02,
    3.60e02,
    3.61e02,
    3.61e02,
    3.62e02,
    3.62e02,
    3.62e02,
    3.63e02,
    3.63e02,
    3.64e02,
    3.63e02,
    3.64e02,
    3.64e02,
    3.64e02,
    3.64e02,
    3.64e02,
    3.63e02,
    3.64e02,
    3.64e02,
    3.64e02,
    3.64e02,
    3.64e02,
    3.64e02,
    3.65e02,
    3.65e02,
    3.66e02,
    3.66e02,
    3.67e02,
    3.67e02,
    3.67e02,
    3.68e02,
    3.68e02,
    3.68e02,
    3.69e02,
    3.69e02,
    3.69e02,
    3.70e02,
    3.70e02,
    3.70e02,
    3.71e02,
    3.71e02,
    3.71e02,
    3.72e02,
    3.72e02,
    3.72e02,
    3.73e02,
    3.73e02,
    3.73e02,
    3.74e02,
    3.74e02,
    3.74e02,
    3.74e02,
    3.74e02,
    3.74e02,
    3.75e02,
    3.75e02,
    3.75e02,
    3.75e02,
    3.75e02,
    3.75e02,
    3.76e02,
    3.76e02,
    3.76e02,
    3.76e02,
    3.76e02,
    3.76e02,
    3.77e02,
    3.77e02,
    3.77e02,
    3.77e02,
    3.77e02,
    3.77e02,
    3.77e02,
    3.77e02,
    3.77e02,
    3.77e02,
    3.77e02,
    3.77e02,
    3.77e02,
    3.76e02,
    3.76e02,
    3.75e02,
    3.74e02,
    3.73e02,
    3.72e02,
    3.71e02,
    3.70e02,
    3.70e02,
    3.69e02,
    3.69e02,
    3.69e02,
    3.69e02,
    3.69e02,
    3.69e02,
    3.70e02,
    3.70e02,
    3.70e02,
    3.70e02,
    3.70e02,
    3.70e02,
    3.70e02,
    3.70e02,
    3.70e02,
    3.70e02,
    3.70e02,
    3.70e02,
    3.69e02,
    3.69e02,
    3.69e02,
    3.69e02,
    3.69e02,
    3.69e02,
    3.69e02,
    3.69e02,
    3.69e02,
    3.69e02,
    3.69e02,
    3.69e02,
    3.69e02,
    3.69e02,
    3.69e02,
    3.69e02,
    3.68e02,
    3.68e02,
    3.68e02,
    3.67e02,
    3.67e02,
    3.66e02,
    3.66e02,
    3.66e02,
    3.65e02,
    3.65e02,
    3.65e02,
    3.65e02,
    3.64e02,
    3.64e02,
    3.63e02,
    3.63e02,
    3.63e02,
    3.62e02,
    3.61e02,
    3.61e02,
    3.60e02,
    3.59e02,
    3.58e02,
    3.57e02,
    3.56e02,
    3.56e02,
    3.55e02,
    3.55e02,
    3.54e02,
    3.54e02,
    3.54e02,
    3.53e02,
    3.53e02,
    3.53e02,
    3.52e02,
    3.52e02,
    3.52e02,
    3.51e02,
    3.50e02,
    3.49e02,
    3.49e02,
    3.48e02,
    3.47e02,
    3.46e02,
    3.45e02,
    3.44e02,
    3.43e02,
    3.42e02,
    3.41e02,
    3.40e02,
    3.39e02,
    3.38e02,
    3.37e02,
    3.36e02,
    3.35e02,
    3.34e02,
    3.34e02,
    3.33e02,
    3.32e02,
    3.32e02,
    3.31e02,
    3.31e02,
    3.31e02,
    3.30e02,
    3.30e02,
    3.29e02,
    3.29e02,
    3.28e02,
    3.27e02,
    3.27e02,
    3.26e02,
    3.25e02,
    3.24e02,
    3.24e02,
    3.23e02,
    3.22e02,
    3.22e02,
    3.21e02,
    3.21e02,
    3.20e02,
    3.20e02,
    3.19e02,
    3.19e02,
    3.18e02,
    3.18e02,
    3.17e02,
    3.16e02,
    3.15e02,
    3.15e02,
    3.14e02,
    3.13e02,
    3.12e02,
    3.11e02,
    3.10e02,
    3.09e02,
    3.08e02,
    3.07e02,
    3.06e02,
    3.05e02,
    3.04e02,
    3.04e02,
    3.03e02,
    3.03e02,
    3.02e02,
    3.02e02,
    3.01e02,
    3.01e02,
    3.01e02,
    3.00e02,
    3.00e02,
    3.00e02,
    3.00e02,
    2.99e02,
    2.99e02,
    2.99e02,
    2.99e02,
    2.99e02,
    2.99e02,
    2.98e02,
    2.98e02,
    2.98e02,
    2.97e02,
    2.97e02,
    2.96e02,
    2.96e02,
    2.96e02,
    2.95e02,
    2.95e02,
    2.95e02,
    2.95e02,
    2.95e02,
    2.95e02,
    2.96e02,
    2.96e02,
    2.96e02,
    2.96e02,
    2.96e02,
    2.96e02,
    2.96e02,
    2.96e02,
    2.96e02,
    2.96e02,
    2.95e02,
    2.95e02,
    2.95e02,
    2.95e02,
    2.95e02,
    2.94e02,
    2.94e02,
    2.94e02,
    2.93e02,
    2.93e02,
    2.92e02,
    2.92e02,
    2.92e02,
    2.91e02,
    2.91e02,
    2.91e02,
    2.91e02,
    2.90e02,
    2.90e02,
    2.90e02,
    2.90e02,
    2.90e02,
    2.90e02,
    2.89e02,
    2.89e02,
    2.89e02,
    2.89e02,
    2.89e02,
    2.88e02,
    2.88e02,
    2.88e02,
    2.88e02,
    2.87e02,
    2.87e02,
    2.87e02,
    2.86e02,
    2.86e02,
    2.85e02,
    2.85e02,
    2.84e02,
    2.84e02,
    2.83e02,
    2.83e02,
    2.83e02,
    2.82e02,
    2.82e02,
    2.82e02,
    2.82e02,
    2.82e02,
    2.82e02,
    2.82e02,
    2.82e02,
    2.82e02,
    2.82e02,
    2.81e02,
    2.81e02,
    2.81e02,
    2.80e02,
    2.79e02,
    2.79e02,
    2.78e02,
    2.77e02,
    2.77e02,
    2.76e02,
    2.75e02,
    2.75e02,
    2.75e02,
    2.74e02,
    2.74e02,
    2.74e02,
    2.74e02,
    2.73e02,
    2.73e02,
    2.73e02,
    2.72e02,
    2.72e02,
    2.71e02,
    2.71e02,
    2.70e02,
    2.69e02,
    2.69e02,
    2.68e02,
    2.67e02,
    2.67e02,
    2.66e02,
    2.65e02,
    2.64e02,
    2.63e02,
    2.63e02,
    2.62e02,
    2.61e02,
    2.60e02,
    2.59e02,
    2.58e02,
    2.57e02,
    2.57e02,
    2.56e02,
    2.55e02,
    2.55e02,
    2.54e02,
    2.53e02,
    2.53e02,
    2.52e02,
    2.51e02,
    2.50e02,
    2.49e02,
    2.48e02,
    2.47e02,
    2.46e02,
    2.45e02,
    2.43e02,
    2.42e02,
    2.40e02,
    2.39e02,
    2.37e02,
    2.35e02,
    2.34e02,
    2.31e02,
    2.29e02,
    2.27e02,
    2.25e02,
    2.23e02,
    2.21e02,
    2.20e02,
    2.19e02,
    2.18e02,
    2.17e02,
    2.16e02,
    2.16e02,
    2.16e02,
    2.16e02,
    2.16e02,
    2.16e02,
    2.15e02,
    2.15e02,
    2.14e02,
    2.13e02,
    2.13e02,
    2.12e02,
    2.11e02,
    2.09e02,
    2.08e02,
    2.07e02,
    2.06e02,
    2.05e02,
    2.03e02,
    2.02e02,
    2.01e02,
    2.00e02,
    1.98e02,
    1.97e02,
    1.95e02,
    1.94e02,
    1.92e02,
    1.90e02,
    1.89e02,
    1.87e02,
    1.85e02,
    1.83e02,
    1.82e02,
    1.80e02,
    1.78e02,
    1.76e02,
    1.75e02,
    1.73e02,
    1.71e02,
    1.69e02,
    1.67e02,
    1.66e02,
    1.64e02,
    1.62e02,
    1.60e02,
    1.59e02,
    1.57e02,
    1.55e02,
    1.54e02,
    1.53e02,
    1.52e02,
    1.51e02,
    1.50e02,
    1.49e02,
    1.48e02,
    1.47e02,
    1.46e02,
    1.45e02,
    1.44e02,
    1.43e02,
    1.42e02,
    1.41e02,
    1.40e02,
    1.39e02,
    1.39e02,
    1.38e02,
    1.37e02,
    1.36e02,
    1.36e02,
    1.35e02,
    1.35e02,
    1.34e02,
    1.34e02,
    1.33e02,
    1.33e02,
    1.33e02,
    1.32e02,
    1.32e02,
    1.31e02,
    1.31e02,
    1.31e02,
    1.30e02,
    1.30e02,
    1.30e02,
    1.30e02,
    1.29e02,
    1.29e02,
    1.29e02,
    1.29e02,
    1.29e02,
    1.29e02,
    1.29e02,
    1.28e02,
    1.28e02,
    1.28e02,
    1.28e02,
    1.28e02,
    1.28e02,
    1.28e02,
    1.28e02,
    1.28e02,
    1.28e02,
    1.28e02,
    1.28e02,
    1.28e02,
    1.28e02,
    1.28e02,
    1.28e02,
    1.28e02,
    1.27e02,
    1.27e02,
    1.27e02,
    1.27e02,
    1.27e02,
    1.27e02,
    1.27e02,
    1.27e02,
    1.27e02,
    1.27e02,
    1.27e02,
    1.27e02,
    1.28e02,
    1.28e02,
    1.29e02,
    1.29e02,
    1.29e02,
    1.30e02,
    1.30e02,
    1.30e02,
    1.30e02,
    1.30e02,
    1.30e02,
    1.30e02,
    1.30e02,
    1.30e02,
    1.30e02,
    1.30e02,
    1.30e02,
    1.30e02,
    1.30e02,
    1.30e02,
    1.30e02,
    1.30e02,
    1.31e02,
    1.31e02,
    1.31e02,
    1.31e02,
    1.31e02,
    1.31e02,
    1.31e02,
    1.31e02,
    1.32e02,
    1.32e02,
    1.32e02,
    1.32e02,
    1.33e02,
    1.33e02,
    1.33e02,
    1.33e02,
    1.33e02,
    1.33e02,
    1.33e02,
    1.33e02,
    1.33e02,
    1.33e02,
    1.33e02,
    1.33e02,
    1.33e02,
    1.34e02,
    1.34e02,
    1.34e02,
    1.34e02,
    1.34e02,
    1.34e02,
    1.34e02,
    1.34e02,
    1.35e02,
    1.35e02,
    1.35e02,
    1.35e02,
    1.35e02,
    1.35e02,
    1.35e02,
    1.35e02,
    1.35e02,
    1.35e02,
    1.35e02,
    1.35e02,
    1.35e02,
    1.34e02,
    1.34e02,
    1.34e02,
    1.34e02,
    1.34e02,
    1.34e02,
    1.34e02,
    1.34e02,
    1.34e02,
    1.34e02,
    1.34e02,
    1.34e02,
    1.34e02,
    1.34e02,
    1.34e02,
    1.33e02,
    1.33e02,
    1.33e02,
    1.33e02,
    1.33e02,
    1.32e02,
    1.32e02,
    1.32e02,
    1.32e02,
    1.31e02,
    1.31e02,
    1.31e02,
    1.30e02,
    1.30e02,
    1.30e02,
    1.30e02,
    1.30e02,
    1.30e02,
    1.30e02,
    1.30e02,
    1.30e02,
    1.30e02,
    1.30e02,
    1.30e02,
    1.30e02,
    1.30e02,
    1.29e02,
    1.29e02,
    1.29e02,
    1.29e02,
    1.28e02,
    1.28e02,
    1.28e02,
    1.27e02,
    1.27e02,
    1.27e02,
    1.26e02,
    1.26e02,
    1.26e02,
    1.25e02,
    1.25e02,
    1.25e02,
    1.25e02,
    1.25e02,
    1.24e02,
    1.24e02,
    1.24e02,
    1.24e02,
    1.24e02,
    1.25e02,
    1.25e02,
    1.25e02,
    1.25e02,
    1.25e02,
    1.25e02,
    1.26e02,
    1.26e02,
    1.26e02,
    1.27e02,
    1.27e02,
    1.27e02,
    1.28e02,
    1.28e02,
    1.28e02,
    1.28e02,
    1.28e02,
    1.28e02,
    1.28e02,
    1.27e02,
    1.27e02,
    1.27e02,
    1.27e02,
    1.27e02,
    1.26e02,
    1.26e02,
    1.26e02,
    1.26e02,
    1.26e02,
    1.26e02,
    1.26e02,
    1.26e02,
    1.26e02,
    1.26e02,
    1.26e02,
    1.26e02,
    1.26e02,
    1.26e02,
    1.26e02,
    1.26e02,
    1.25e02,
    1.25e02,
    1.25e02,
    1.25e02,
    1.25e02,
    1.24e02,
    1.24e02,
    1.24e02,
    1.23e02,
    1.23e02,
    1.22e02,
    1.22e02,
    1.21e02,
    1.21e02,
    1.20e02,
    1.20e02,
    1.19e02,
    1.18e02,
    1.18e02,
    1.17e02,
    1.17e02,
    1.16e02,
    1.16e02,
    1.15e02,
    1.15e02,
    1.14e02,
    1.14e02,
    1.13e02,
    1.13e02,
    1.12e02,
    1.12e02,
    1.12e02,
    1.11e02,
    1.11e02,
    1.10e02,
    1.10e02,
    1.09e02,
    1.09e02,
    1.08e02,
    1.08e02,
    1.07e02,
    1.07e02,
    1.06e02,
    1.05e02,
    1.05e02,
    1.04e02,
    1.03e02,
    1.03e02,
    1.02e02,
    1.01e02,
    1.01e02,
    9.99e01,
    9.93e01,
    9.87e01,
    9.81e01,
    9.76e01,
    9.71e01,
    9.67e01,
    9.64e01,
    9.61e01,
    9.59e01,
    9.57e01,
    9.57e01,
    9.56e01,
    9.57e01,
    9.57e01,
    9.57e01,
    9.58e01,
    9.58e01,
    9.58e01,
    9.58e01,
    9.58e01,
    9.58e01,
    9.58e01,
    9.58e01,
    9.58e01,
    9.59e01,
    9.59e01,
    9.59e01,
    9.60e01,
    9.60e01,
    9.60e01,
    9.60e01,
    9.60e01,
    9.59e01,
    9.58e01,
    9.57e01,
    9.56e01,
    9.55e01,
    9.54e01,
    9.53e01,
    9.52e01,
    9.50e01,
    9.48e01,
    9.46e01,
    9.43e01,
    9.40e01,
    9.37e01,
    9.34e01,
    9.30e01,
    9.27e01,
    9.25e01,
    9.22e01,
    9.21e01,
    9.19e01,
    9.18e01,
    9.17e01,
    9.17e01,
    9.16e01,
    9.16e01,
    9.16e01,
    9.16e01,
    9.16e01,
    9.16e01,
    9.16e01,
    9.15e01,
    9.15e01,
    9.15e01,
    9.14e01,
    9.14e01,
    9.14e01,
    9.13e01,
    9.13e01,
    9.13e01,
    9.13e01,
    9.13e01,
    9.13e01,
    9.13e01,
    9.14e01,
    9.15e01,
    9.15e01,
    9.16e01,
    9.16e01,
    9.16e01,
    9.16e01,
    9.15e01,
    9.14e01,
    9.12e01,
    9.11e01,
    9.09e01,
    9.07e01,
    9.05e01,
    9.03e01,
    9.02e01,
    9.00e01,
    8.99e01,
    8.98e01,
    8.97e01,
    8.96e01,
    8.96e01,
    8.95e01,
    8.94e01,
    8.93e01,
    8.91e01,
    8.89e01,
    8.87e01,
    8.85e01,
    8.82e01,
    8.80e01,
    8.77e01,
    8.74e01,
    8.71e01,
    8.67e01,
    8.64e01,
    8.61e01,
    8.58e01,
    8.55e01,
    8.52e01,
    8.49e01,
    8.46e01,
    8.43e01,
    8.41e01,
    8.38e01,
    8.36e01,
    8.34e01,
    8.31e01,
    8.29e01,
    8.27e01,
    8.25e01,
    8.23e01,
    8.21e01,
    8.19e01,
    8.18e01,
    8.16e01,
    8.15e01,
    8.13e01,
    8.12e01,
    8.10e01,
    8.09e01,
    8.07e01,
    8.05e01,
    8.03e01,
    8.01e01,
    8.00e01,
    7.98e01,
    7.96e01,
    7.94e01,
    7.93e01,
    7.91e01,
    7.89e01,
    7.88e01,
    7.86e01,
    7.83e01,
    7.81e01,
    7.78e01,
    7.73e01,
    7.68e01,
    7.61e01,
    7.53e01,
    7.44e01,
    7.35e01,
    7.26e01,
    7.17e01,
    7.07e01,
    6.98e01,
    6.90e01,
    6.81e01,
    6.73e01,
    6.65e01,
    6.57e01,
    6.49e01,
    6.41e01,
    6.33e01,
    6.25e01,
    6.14e01,
    6.02e01,
    5.90e01,
    5.77e01,
    5.64e01,
    5.51e01,
    5.38e01,
    5.24e01,
    5.11e01,
    4.97e01,
    4.84e01,
    4.71e01,
    4.61e01,
    4.52e01,
    4.42e01,
    4.33e01,
    4.24e01,
    4.16e01,
    4.08e01,
    4.01e01,
    3.94e01,
    3.88e01,
    3.82e01,
    3.77e01,
    3.71e01,
    3.67e01,
    3.62e01,
    3.59e01,
    3.55e01,
    3.51e01,
    3.48e01,
    3.44e01,
    3.39e01,
    3.35e01,
    3.31e01,
    3.27e01,
    3.23e01,
    3.20e01,
    3.17e01,
    3.14e01,
    3.12e01,
    3.11e01,
    3.09e01,
    3.08e01,
    3.07e01,
    3.07e01,
    3.07e01,
    3.07e01,
    3.07e01,
    3.07e01,
    3.07e01,
    3.06e01,
    3.06e01,
    3.05e01,
    3.04e01,
    3.02e01,
    3.01e01,
    3.01e01,
    3.00e01,
    3.01e01,
    3.02e01,
    3.02e01,
    3.02e01,
    3.02e01,
    3.01e01,
    3.01e01,
    3.01e01,
    3.01e01,
    3.01e01,
    3.02e01,
    3.02e01,
    3.03e01,
    3.04e01,
    3.05e01,
    3.06e01,
    3.06e01,
    3.07e01,
    3.08e01,
    3.09e01,
    3.10e01,
    3.11e01,
    3.12e01,
    3.14e01,
    3.16e01,
    3.18e01,
    3.20e01,
    3.22e01,
    3.25e01,
    3.27e01,
    3.29e01,
    3.30e01,
    3.31e01,
    3.32e01,
    3.32e01,
    3.33e01,
    3.33e01,
    3.33e01,
    3.34e01,
    3.34e01,
    3.34e01,
    3.35e01,
    3.36e01,
    3.37e01,
    3.38e01,
    3.40e01,
    3.41e01,
    3.43e01,
    3.44e01,
    3.46e01,
    3.48e01,
    3.50e01,
    3.51e01,
    3.53e01,
    3.54e01,
    3.56e01,
    3.58e01,
    3.60e01,
    3.61e01,
    3.63e01,
    3.65e01,
    3.66e01,
    3.67e01,
    3.67e01,
    3.68e01,
    3.69e01,
    3.69e01,
    3.69e01,
    3.70e01,
    3.70e01,
    3.71e01,
    3.71e01,
    3.70e01,
    3.68e01,
    3.66e01,
    3.66e01,
    3.66e01,
    3.66e01,
    3.67e01,
    3.67e01,
    3.67e01,
    3.66e01,
    3.66e01,
    3.67e01,
    3.68e01,
    3.69e01,
    3.68e01,
    3.68e01,
    3.68e01,
    3.68e01,
    3.67e01,
    3.67e01,
    3.67e01,
    3.67e01,
    3.67e01,
    3.66e01,
    3.66e01,
    3.67e01,
    3.68e01,
    3.69e01,
    3.70e01,
    3.70e01,
    3.69e01,
    3.69e01,
    3.68e01,
    3.66e01,
    3.65e01,
    3.63e01,
    3.61e01,
    3.60e01,
    3.59e01,
    3.59e01,
    3.57e01,
    3.56e01,
    3.54e01,
    3.53e01,
    3.52e01,
    3.51e01,
    3.53e01,
    3.54e01,
    3.54e01,
    3.53e01,
    3.51e01,
    3.50e01,
    3.48e01,
    3.46e01,
    3.44e01,
    3.42e01,
    3.41e01,
    3.39e01,
    3.37e01,
    3.36e01,
    3.36e01,
    3.35e01,
    3.34e01,
    3.33e01,
    3.32e01,
    3.31e01,
    3.31e01,
    3.31e01,
    3.31e01,
    3.31e01,
    3.31e01,
    3.31e01,
    3.31e01,
    3.31e01,
    3.31e01,
    3.32e01,
    3.32e01,
    3.32e01,
    3.33e01,
    3.33e01,
    3.33e01,
    3.34e01,
    3.34e01,
    3.34e01,
    3.33e01,
    3.33e01,
    3.33e01,
    3.33e01,
    3.33e01,
    3.32e01,
    3.32e01,
    3.33e01,
    3.33e01,
    3.33e01,
    3.34e01,
    3.34e01,
    3.34e01,
    3.34e01,
    3.34e01,
    3.33e01,
    3.33e01,
    3.32e01,
    3.31e01,
    3.31e01,
    3.30e01,
    3.30e01,
    3.30e01,
    3.30e01,
    3.31e01,
    3.30e01,
    3.29e01,
    3.29e01,
    3.28e01,
    3.27e01,
    3.26e01,
    3.25e01,
    3.24e01,
    3.23e01,
    3.23e01,
    3.23e01,
    3.24e01,
    3.25e01,
    3.26e01,
    3.27e01,
    3.28e01,
    3.28e01,
    3.29e01,
    3.30e01,
    3.31e01,
    3.31e01,
    3.31e01,
    3.31e01,
    3.30e01,
    3.31e01,
    3.31e01,
    3.30e01,
    3.29e01,
    3.29e01,
    3.30e01,
    3.31e01,
    3.33e01,
    3.34e01,
    3.36e01,
    3.38e01,
    3.39e01,
    3.41e01,
    3.42e01,
    3.43e01,
    3.43e01,
    3.44e01,
    3.44e01,
    3.43e01,
    3.43e01,
    3.43e01,
    3.42e01,
    3.42e01,
    3.41e01,
    3.41e01,
    3.40e01,
    3.40e01,
    3.39e01,
    3.37e01,
    3.35e01,
    3.34e01,
    3.33e01,
    3.31e01,
    3.30e01,
    3.29e01,
    3.29e01,
    3.29e01,
    3.29e01,
    3.30e01,
    3.30e01,
    3.31e01,
    3.32e01,
    3.33e01,
    3.34e01,
    3.35e01,
    3.36e01,
    3.36e01,
    3.37e01,
    3.38e01,
    3.38e01,
    3.39e01,
    3.40e01,
    3.42e01,
    3.42e01,
    3.43e01,
    3.44e01,
    3.44e01,
    3.43e01,
    3.42e01,
    3.41e01,
    3.39e01,
    3.37e01,
    3.35e01,
    3.33e01,
    3.32e01,
    3.30e01,
    3.30e01,
    3.29e01,
    3.29e01,
    3.29e01,
    3.29e01,
    3.30e01,
    3.30e01,
    3.30e01,
    3.30e01,
    3.30e01,
    3.30e01,
    3.30e01,
    3.30e01,
    3.29e01,
    3.29e01,
    3.30e01,
    3.30e01,
    3.30e01,
    3.30e01,
    3.29e01,
    3.28e01,
    3.27e01,
    3.27e01,
    3.26e01,
    3.26e01,
    3.27e01,
    3.28e01,
    3.28e01,
    3.29e01,
    3.29e01,
    3.28e01,
    3.27e01,
    3.25e01,
    3.23e01,
    3.21e01,
    3.19e01,
    3.17e01,
    3.15e01,
    3.13e01,
    3.12e01,
    3.11e01,
    3.10e01,
    3.09e01,
    3.08e01,
    3.07e01,
    3.07e01,
    3.06e01,
    3.05e01,
    3.05e01,
    3.04e01,
    3.03e01,
    3.01e01,
    3.00e01,
    2.98e01,
    2.97e01,
    2.95e01,
    2.94e01,
    2.92e01,
    2.90e01,
    2.89e01,
    2.88e01,
    2.87e01,
    2.86e01,
    2.85e01,
    2.84e01,
    2.84e01,
    2.83e01,
    2.82e01,
    2.80e01,
    2.78e01,
    2.76e01,
    2.74e01,
    2.71e01,
    2.67e01,
    2.64e01,
    2.61e01,
    2.57e01,
    2.53e01,
    2.50e01,
    2.46e01,
    2.43e01,
    2.40e01,
    2.37e01,
    2.33e01,
    2.30e01,
    2.27e01,
    2.24e01,
    2.21e01,
    2.19e01,
    2.16e01,
    2.13e01,
    2.11e01,
    2.09e01,
    2.07e01,
    2.05e01,
    2.03e01,
    2.01e01,
    2.00e01,
    1.99e01,
    1.97e01,
    1.96e01,
    1.95e01,
    1.94e01,
    1.94e01,
    1.93e01,
    1.92e01,
    1.91e01,
    1.91e01,
    1.91e01,
    1.90e01,
    1.90e01,
    1.90e01,
    1.91e01,
    1.91e01,
    1.91e01,
    1.92e01,
    1.93e01,
    1.93e01,
    1.94e01,
    1.94e01,
    1.94e01,
    1.94e01,
    1.94e01,
    1.93e01,
    1.93e01,
    1.92e01,
    1.91e01,
    1.91e01,
    1.90e01,
    1.90e01,
    1.90e01,
    1.89e01,
    1.90e01,
    1.90e01,
    1.91e01,
    1.91e01,
    1.92e01,
    1.93e01,
    1.93e01,
    1.93e01,
    1.93e01,
    1.92e01,
    1.92e01,
    1.91e01,
    1.90e01,
    1.89e01,
    1.88e01,
    1.87e01,
    1.86e01,
    1.85e01,
    1.84e01,
    1.83e01,
    1.82e01,
    1.81e01,
    1.81e01,
    1.80e01,
    1.79e01,
    1.78e01,
    1.77e01,
    1.76e01,
    1.76e01,
    1.75e01,
    1.74e01,
    1.74e01,
    1.73e01,
    1.73e01,
    1.72e01,
    1.72e01,
    1.71e01,
    1.71e01,
    1.71e01,
    1.71e01,
    1.71e01,
    1.71e01,
    1.72e01,
    1.72e01,
    1.72e01,
    1.73e01,
    1.73e01,
    1.73e01,
    1.73e01,
    1.73e01,
    1.72e01,
    1.72e01,
    1.72e01,
    1.71e01,
    1.71e01,
    1.70e01,
    1.69e01,
    1.69e01,
    1.68e01,
]


# - local functions ----------------------------
def helios_spectrum() -> xr.Dataset:
    """Define Helios spectrum."""
    # Maybe we should also check the light-level value as specified
    # in the name of the L0 file. The light level is coded as:
    # L1: 100%, L2: 50%, L3: 30%, L4: 15%, L5: 7%, L6: 3%
    wavelength = np.linspace(350, 2400, 2051, dtype="f4")
    xar_wv = xr.DataArray(
        wavelength,
        coords={"wavelength": wavelength},
        attrs={
            "longname": "wavelength grid",
            "units": "nm",
            "comment": "wavelength annotation",
        },
    )

    xar_sign = xr.DataArray(
        1e-3 * np.array(HELIOS_SPECTRUM, dtype="f4"),
        coords={"wavelength": wavelength},
        attrs={"longname": "Helios radiance spectrum", "units": "W/(m^2.sr.nm)"},
    )

    return xr.Dataset(
        {"wavelength": xar_wv, "spectral_radiance": xar_sign}, attrs=HELIOS_ATTRS
    )


def __test(l1a_file: str) -> None:
    """Small function to test this module."""
    # Create a netCDF4 file containing the Helios reference spectrum
    xds = helios_spectrum()
    xds.to_netcdf(
        l1a_file, mode="w", format="NETCDF4", group="/gse_data/ReferenceSpectrum"
    )


# --------------------------------------------------
if __name__ == "__main__":
    print("---------- SHOW DATASET ----------")
    print(helios_spectrum())
    print("---------- WRITE DATASET ----------")
    __test("test_netcdf.nc")
