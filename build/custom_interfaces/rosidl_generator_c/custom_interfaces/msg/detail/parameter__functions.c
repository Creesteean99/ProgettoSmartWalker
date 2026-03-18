// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from custom_interfaces:msg/Parameter.idl
// generated code does not contain a copyright notice
#include "custom_interfaces/msg/detail/parameter__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `start_point`
// Member `end_point`
#include "geometry_msgs/msg/detail/point__functions.h"

bool
custom_interfaces__msg__Parameter__init(custom_interfaces__msg__Parameter * msg)
{
  if (!msg) {
    return false;
  }
  // guide_type
  // start_point
  if (!geometry_msgs__msg__Point__init(&msg->start_point)) {
    custom_interfaces__msg__Parameter__fini(msg);
    return false;
  }
  // end_point
  if (!geometry_msgs__msg__Point__init(&msg->end_point)) {
    custom_interfaces__msg__Parameter__fini(msg);
    return false;
  }
  // thickness
  // amplitude
  // record
  return true;
}

void
custom_interfaces__msg__Parameter__fini(custom_interfaces__msg__Parameter * msg)
{
  if (!msg) {
    return;
  }
  // guide_type
  // start_point
  geometry_msgs__msg__Point__fini(&msg->start_point);
  // end_point
  geometry_msgs__msg__Point__fini(&msg->end_point);
  // thickness
  // amplitude
  // record
}

bool
custom_interfaces__msg__Parameter__are_equal(const custom_interfaces__msg__Parameter * lhs, const custom_interfaces__msg__Parameter * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // guide_type
  if (lhs->guide_type != rhs->guide_type) {
    return false;
  }
  // start_point
  if (!geometry_msgs__msg__Point__are_equal(
      &(lhs->start_point), &(rhs->start_point)))
  {
    return false;
  }
  // end_point
  if (!geometry_msgs__msg__Point__are_equal(
      &(lhs->end_point), &(rhs->end_point)))
  {
    return false;
  }
  // thickness
  if (lhs->thickness != rhs->thickness) {
    return false;
  }
  // amplitude
  if (lhs->amplitude != rhs->amplitude) {
    return false;
  }
  // record
  if (lhs->record != rhs->record) {
    return false;
  }
  return true;
}

bool
custom_interfaces__msg__Parameter__copy(
  const custom_interfaces__msg__Parameter * input,
  custom_interfaces__msg__Parameter * output)
{
  if (!input || !output) {
    return false;
  }
  // guide_type
  output->guide_type = input->guide_type;
  // start_point
  if (!geometry_msgs__msg__Point__copy(
      &(input->start_point), &(output->start_point)))
  {
    return false;
  }
  // end_point
  if (!geometry_msgs__msg__Point__copy(
      &(input->end_point), &(output->end_point)))
  {
    return false;
  }
  // thickness
  output->thickness = input->thickness;
  // amplitude
  output->amplitude = input->amplitude;
  // record
  output->record = input->record;
  return true;
}

custom_interfaces__msg__Parameter *
custom_interfaces__msg__Parameter__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  custom_interfaces__msg__Parameter * msg = (custom_interfaces__msg__Parameter *)allocator.allocate(sizeof(custom_interfaces__msg__Parameter), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(custom_interfaces__msg__Parameter));
  bool success = custom_interfaces__msg__Parameter__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
custom_interfaces__msg__Parameter__destroy(custom_interfaces__msg__Parameter * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    custom_interfaces__msg__Parameter__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
custom_interfaces__msg__Parameter__Sequence__init(custom_interfaces__msg__Parameter__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  custom_interfaces__msg__Parameter * data = NULL;

  if (size) {
    data = (custom_interfaces__msg__Parameter *)allocator.zero_allocate(size, sizeof(custom_interfaces__msg__Parameter), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = custom_interfaces__msg__Parameter__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        custom_interfaces__msg__Parameter__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
custom_interfaces__msg__Parameter__Sequence__fini(custom_interfaces__msg__Parameter__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      custom_interfaces__msg__Parameter__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

custom_interfaces__msg__Parameter__Sequence *
custom_interfaces__msg__Parameter__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  custom_interfaces__msg__Parameter__Sequence * array = (custom_interfaces__msg__Parameter__Sequence *)allocator.allocate(sizeof(custom_interfaces__msg__Parameter__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = custom_interfaces__msg__Parameter__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
custom_interfaces__msg__Parameter__Sequence__destroy(custom_interfaces__msg__Parameter__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    custom_interfaces__msg__Parameter__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
custom_interfaces__msg__Parameter__Sequence__are_equal(const custom_interfaces__msg__Parameter__Sequence * lhs, const custom_interfaces__msg__Parameter__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!custom_interfaces__msg__Parameter__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
custom_interfaces__msg__Parameter__Sequence__copy(
  const custom_interfaces__msg__Parameter__Sequence * input,
  custom_interfaces__msg__Parameter__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(custom_interfaces__msg__Parameter);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    custom_interfaces__msg__Parameter * data =
      (custom_interfaces__msg__Parameter *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!custom_interfaces__msg__Parameter__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          custom_interfaces__msg__Parameter__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!custom_interfaces__msg__Parameter__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
