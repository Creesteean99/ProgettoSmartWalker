// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from custom_interfaces:msg/Parameter.idl
// generated code does not contain a copyright notice

#ifndef CUSTOM_INTERFACES__MSG__DETAIL__PARAMETER__STRUCT_HPP_
#define CUSTOM_INTERFACES__MSG__DETAIL__PARAMETER__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


// Include directives for member types
// Member 'start_point'
// Member 'end_point'
#include "geometry_msgs/msg/detail/point__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__custom_interfaces__msg__Parameter __attribute__((deprecated))
#else
# define DEPRECATED__custom_interfaces__msg__Parameter __declspec(deprecated)
#endif

namespace custom_interfaces
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct Parameter_
{
  using Type = Parameter_<ContainerAllocator>;

  explicit Parameter_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : start_point(_init),
    end_point(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->guide_type = 0l;
      this->thickness = 0.0f;
      this->amplitude = 0.0f;
      this->record = false;
    }
  }

  explicit Parameter_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : start_point(_alloc, _init),
    end_point(_alloc, _init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->guide_type = 0l;
      this->thickness = 0.0f;
      this->amplitude = 0.0f;
      this->record = false;
    }
  }

  // field types and members
  using _guide_type_type =
    int32_t;
  _guide_type_type guide_type;
  using _start_point_type =
    geometry_msgs::msg::Point_<ContainerAllocator>;
  _start_point_type start_point;
  using _end_point_type =
    geometry_msgs::msg::Point_<ContainerAllocator>;
  _end_point_type end_point;
  using _thickness_type =
    float;
  _thickness_type thickness;
  using _amplitude_type =
    float;
  _amplitude_type amplitude;
  using _record_type =
    bool;
  _record_type record;

  // setters for named parameter idiom
  Type & set__guide_type(
    const int32_t & _arg)
  {
    this->guide_type = _arg;
    return *this;
  }
  Type & set__start_point(
    const geometry_msgs::msg::Point_<ContainerAllocator> & _arg)
  {
    this->start_point = _arg;
    return *this;
  }
  Type & set__end_point(
    const geometry_msgs::msg::Point_<ContainerAllocator> & _arg)
  {
    this->end_point = _arg;
    return *this;
  }
  Type & set__thickness(
    const float & _arg)
  {
    this->thickness = _arg;
    return *this;
  }
  Type & set__amplitude(
    const float & _arg)
  {
    this->amplitude = _arg;
    return *this;
  }
  Type & set__record(
    const bool & _arg)
  {
    this->record = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    custom_interfaces::msg::Parameter_<ContainerAllocator> *;
  using ConstRawPtr =
    const custom_interfaces::msg::Parameter_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<custom_interfaces::msg::Parameter_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<custom_interfaces::msg::Parameter_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      custom_interfaces::msg::Parameter_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<custom_interfaces::msg::Parameter_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      custom_interfaces::msg::Parameter_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<custom_interfaces::msg::Parameter_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<custom_interfaces::msg::Parameter_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<custom_interfaces::msg::Parameter_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__custom_interfaces__msg__Parameter
    std::shared_ptr<custom_interfaces::msg::Parameter_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__custom_interfaces__msg__Parameter
    std::shared_ptr<custom_interfaces::msg::Parameter_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const Parameter_ & other) const
  {
    if (this->guide_type != other.guide_type) {
      return false;
    }
    if (this->start_point != other.start_point) {
      return false;
    }
    if (this->end_point != other.end_point) {
      return false;
    }
    if (this->thickness != other.thickness) {
      return false;
    }
    if (this->amplitude != other.amplitude) {
      return false;
    }
    if (this->record != other.record) {
      return false;
    }
    return true;
  }
  bool operator!=(const Parameter_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct Parameter_

// alias to use template instance with default allocator
using Parameter =
  custom_interfaces::msg::Parameter_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace custom_interfaces

#endif  // CUSTOM_INTERFACES__MSG__DETAIL__PARAMETER__STRUCT_HPP_
