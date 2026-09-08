=======
History
=======

0.5.0 (2026-03-19)
------------------

* Added :func:`adam.util.azimuth_from_ellipse` for deriving the instrument
  pointing direction from an ellipse fitted to the lake breeze mask.
* Added unit tests covering the new azimuth utilities.
* Expanded the notebook documentation.

0.4.0 (2026-02-09)
------------------

* Added the :mod:`adam.triggering` module with adaptive scanning support for
  Halo Photonics lidars.
* Added the :mod:`adam.testing` module, including a reference test dataset and
  fake SSH/SFTP clients for exercising scan triggering without hardware.
* Added docstrings and documented references for the testing and triggering
  modules.
* Allowed the user to specify their own S3 bucket when fetching radar data, and
  changed the default bucket.
* Fixed handling of ``radar_object`` when passed as either a list or an array.

0.3.0 (2025-09-15)
------------------

* Added the Sphinx-Gallery example gallery.
* Fixed the instrument pointing feature.

0.2.0 (2025-09-08)
------------------

* Added :func:`adam.util.azimuth_point` to determine the optimal instrument
  pointing direction for adaptive scanning.
* Added unit tests for instrument pointing.
* Published the documentation to GitHub Pages.

0.1.1 (2025-07-14)
------------------

* Renamed the distribution to ``adam-atmos`` on PyPI.

0.1.0 (2025-07-14)
------------------

* First release on PyPI.
