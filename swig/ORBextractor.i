%module ORBextractor

// include header files that are needed to make the generated cpp file works
%{
#define SWIG_FILE_WITH_INIT
#include "ORBextractor.h"
%}

// generate nested classes in python, if theres any
%feature("flatnested");
%feature("autodoc","0");

// handle numpy
%include numpy.i
%init %{
  import_array();   // call numpy c api to init.
%}
// handle cv::Mat
%include <opencv.i>

%cv_instantiate_all_defaults
%include "std_vector.i"
%include "std_list.i"

// now define the 'meat'
%include "ORBextractor.h"
