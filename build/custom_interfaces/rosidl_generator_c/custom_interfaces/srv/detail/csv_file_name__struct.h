// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from custom_interfaces:srv/CSVFileName.idl
// generated code does not contain a copyright notice

#ifndef CUSTOM_INTERFACES__SRV__DETAIL__CSV_FILE_NAME__STRUCT_H_
#define CUSTOM_INTERFACES__SRV__DETAIL__CSV_FILE_NAME__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'filename'
// Member 'directory'
#include "rosidl_runtime_c/string.h"

/// Struct defined in srv/CSVFileName in the package custom_interfaces.
typedef struct custom_interfaces__srv__CSVFileName_Request
{
  rosidl_runtime_c__String filename;
  rosidl_runtime_c__String directory;
} custom_interfaces__srv__CSVFileName_Request;

// Struct for a sequence of custom_interfaces__srv__CSVFileName_Request.
typedef struct custom_interfaces__srv__CSVFileName_Request__Sequence
{
  custom_interfaces__srv__CSVFileName_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} custom_interfaces__srv__CSVFileName_Request__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'message'
// already included above
// #include "rosidl_runtime_c/string.h"

/// Struct defined in srv/CSVFileName in the package custom_interfaces.
typedef struct custom_interfaces__srv__CSVFileName_Response
{
  rosidl_runtime_c__String message;
} custom_interfaces__srv__CSVFileName_Response;

// Struct for a sequence of custom_interfaces__srv__CSVFileName_Response.
typedef struct custom_interfaces__srv__CSVFileName_Response__Sequence
{
  custom_interfaces__srv__CSVFileName_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} custom_interfaces__srv__CSVFileName_Response__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // CUSTOM_INTERFACES__SRV__DETAIL__CSV_FILE_NAME__STRUCT_H_
