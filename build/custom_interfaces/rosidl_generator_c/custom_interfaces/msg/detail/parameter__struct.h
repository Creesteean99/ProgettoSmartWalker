// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from custom_interfaces:msg/Parameter.idl
// generated code does not contain a copyright notice

#ifndef CUSTOM_INTERFACES__MSG__DETAIL__PARAMETER__STRUCT_H_
#define CUSTOM_INTERFACES__MSG__DETAIL__PARAMETER__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'start_point'
// Member 'end_point'
#include "geometry_msgs/msg/detail/point__struct.h"

/// Struct defined in msg/Parameter in the package custom_interfaces.
typedef struct custom_interfaces__msg__Parameter
{
  int32_t guide_type;
  geometry_msgs__msg__Point start_point;
  geometry_msgs__msg__Point end_point;
  float thickness;
  float amplitude;
  bool record;
} custom_interfaces__msg__Parameter;

// Struct for a sequence of custom_interfaces__msg__Parameter.
typedef struct custom_interfaces__msg__Parameter__Sequence
{
  custom_interfaces__msg__Parameter * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} custom_interfaces__msg__Parameter__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // CUSTOM_INTERFACES__MSG__DETAIL__PARAMETER__STRUCT_H_
