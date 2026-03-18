// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from custom_interfaces:msg/Parameter.idl
// generated code does not contain a copyright notice

#ifndef CUSTOM_INTERFACES__MSG__DETAIL__PARAMETER__BUILDER_HPP_
#define CUSTOM_INTERFACES__MSG__DETAIL__PARAMETER__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "custom_interfaces/msg/detail/parameter__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace custom_interfaces
{

namespace msg
{

namespace builder
{

class Init_Parameter_record
{
public:
  explicit Init_Parameter_record(::custom_interfaces::msg::Parameter & msg)
  : msg_(msg)
  {}
  ::custom_interfaces::msg::Parameter record(::custom_interfaces::msg::Parameter::_record_type arg)
  {
    msg_.record = std::move(arg);
    return std::move(msg_);
  }

private:
  ::custom_interfaces::msg::Parameter msg_;
};

class Init_Parameter_amplitude
{
public:
  explicit Init_Parameter_amplitude(::custom_interfaces::msg::Parameter & msg)
  : msg_(msg)
  {}
  Init_Parameter_record amplitude(::custom_interfaces::msg::Parameter::_amplitude_type arg)
  {
    msg_.amplitude = std::move(arg);
    return Init_Parameter_record(msg_);
  }

private:
  ::custom_interfaces::msg::Parameter msg_;
};

class Init_Parameter_thickness
{
public:
  explicit Init_Parameter_thickness(::custom_interfaces::msg::Parameter & msg)
  : msg_(msg)
  {}
  Init_Parameter_amplitude thickness(::custom_interfaces::msg::Parameter::_thickness_type arg)
  {
    msg_.thickness = std::move(arg);
    return Init_Parameter_amplitude(msg_);
  }

private:
  ::custom_interfaces::msg::Parameter msg_;
};

class Init_Parameter_end_point
{
public:
  explicit Init_Parameter_end_point(::custom_interfaces::msg::Parameter & msg)
  : msg_(msg)
  {}
  Init_Parameter_thickness end_point(::custom_interfaces::msg::Parameter::_end_point_type arg)
  {
    msg_.end_point = std::move(arg);
    return Init_Parameter_thickness(msg_);
  }

private:
  ::custom_interfaces::msg::Parameter msg_;
};

class Init_Parameter_start_point
{
public:
  explicit Init_Parameter_start_point(::custom_interfaces::msg::Parameter & msg)
  : msg_(msg)
  {}
  Init_Parameter_end_point start_point(::custom_interfaces::msg::Parameter::_start_point_type arg)
  {
    msg_.start_point = std::move(arg);
    return Init_Parameter_end_point(msg_);
  }

private:
  ::custom_interfaces::msg::Parameter msg_;
};

class Init_Parameter_guide_type
{
public:
  Init_Parameter_guide_type()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Parameter_start_point guide_type(::custom_interfaces::msg::Parameter::_guide_type_type arg)
  {
    msg_.guide_type = std::move(arg);
    return Init_Parameter_start_point(msg_);
  }

private:
  ::custom_interfaces::msg::Parameter msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::custom_interfaces::msg::Parameter>()
{
  return custom_interfaces::msg::builder::Init_Parameter_guide_type();
}

}  // namespace custom_interfaces

#endif  // CUSTOM_INTERFACES__MSG__DETAIL__PARAMETER__BUILDER_HPP_
