Batch processing
================
ADAM supports batch inference so that you can infer the location of the lake breeze overview
multiple radar scans with one inference step. Batch inference will save computational time
by loading the model only once and utilizing vectorization to perform the inference on multiple
radar scans at a time.



Analyzing the mask data in custom workflows
===========================================
The :py:meth:`RadarImage` class contains all of the information you need to perform
custom analyses of the lake breeze front. 