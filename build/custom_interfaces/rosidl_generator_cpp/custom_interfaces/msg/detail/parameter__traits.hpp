// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from custom_interfaces:msg/Parameter.idl
// generated code does not contain a copyright notice

#ifndef CUSTOM_INTERFACES__MSG__DETAIL__PARAMETER__TRAITS_HPP_
#define CUSTOM_INTERFACES__MSG__DETAIL__PARAMETER__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "custom_interfaces/msg/detail/parameter__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'start_point'
// Member 'end_point'
#include "geometry_msgs/msg/detail/point__traits.hpp"

namespace custom_interfaces
{

namespace msg
{

inline void to_flow_style_yaml(
  const Parameter & msg,
  std::ostream & out)
{
  out << "{";
  // member: guide_type
  {
    out << "guide_type: ";
    rosidl_generator_traits::value_to_yaml(msg.guide_type, out);
    out << ", ";
  }

  // member: start_point
  {
    out << "start_point: ";
    to_flow_style_yaml(msg.start_point, out);
    out << ", ";
  }

  // member: end_point
  {
    out << "end_point: ";
    to_flow_style_yaml(msg.end_point, out);
    out << ", ";
  }

  // member: thickness
  {
    out << "thickness: ";
    rosidl_generator_traits::value_to_yaml(msg.thickness, out);
    out << ", ";
  }

  // member: amplitude
  {
    out << "amplitude: ";
    rosidl_generator_traits::value_to_yaml(msg.amplitude, out);
    out << ", ";
  }

  // member: record
  {
    out << "record: ";
    rosidl_generator_traits::value_to_yaml(msg.record, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const Parameter & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: guide_type
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "guide_type: ";
    rosidl_generator_traits::value_to_yaml(msg.guide_type, out);
    out << "\n";
  }

  // member: start_point
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "start_point:\n";
    to_block_style_yaml(msg.start_point, out, indentation + 2);
  }

  // member: end_point
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "end_point:\n";
    to_block_style_yaml(msg.end_point, out, indentation + 2);
  }

  // member: thickness
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "thickness: ";
    rosidl_generator_traits::value_to_yaml(msg.thickness, out);
    out << "\n";
  }

  // member: amplitude
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "amplitude: ";
    rosidl_generator_traits::value_to_yaml(msg.amplitude, out);
    out << "\n";
  }

  // member: record
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "record: ";
    rosidl_generator_traits::value_to_yaml(msg.record, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const Parameter & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace msg

}  // namespace custom_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use custom_interfaces::msg::to_block_style_yaml() instead")]]
inline void to_yaml(
  const custom_interfaces::msg::Parameter & msg,
  std::ostream & out, size_t indentation = 0)
{
  custom_interfaces::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use custom_interfaces::msg::to_yaml() instead")]]
inline std::string to_yaml(const custom_interfaces::msg::Parameter & msg)
{
  return custom_interfaces::msg::to_yaml(msg);
}

template<>
inline const char * data_type<custom_interfaces::msg::Parameter>()
{
  return "custom_interfaces::msg::Parameter";
}

template<>
inline const char * name<custom_interfaces::msg::Parameter>()
{
  return "custom_interfaces/msg/Parameter";
}

template<>
struct has_fixed_size<custom_interfaces::msg::Parameter>
  : std::integral_constant<bool, has_fixed_size<geometry_msgs::msg::Point>::value> {};

template<>
struct has_bounded_size<custom_interfaces::msg::Parameter>
  : std::integral_constant<bool, has_bounded_size<geometry_msgs::msg::Point>::value> {};

template<>
struct is_message<custom_interfaces::msg::Parameter>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // CUSTOM_INTERFACES__MSG__DETAIL__PARAMETER__TRAITS_HPP_
