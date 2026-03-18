// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from custom_interfaces:srv/VelocityRegistration.idl
// generated code does not contain a copyright notice

#ifndef CUSTOM_INTERFACES__SRV__DETAIL__VELOCITY_REGISTRATION__BUILDER_HPP_
#define CUSTOM_INTERFACES__SRV__DETAIL__VELOCITY_REGISTRATION__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "custom_interfaces/srv/detail/velocity_registration__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace custom_interfaces
{

namespace srv
{

namespace builder
{

class Init_VelocityRegistration_Request_create
{
public:
  explicit Init_VelocityRegistration_Request_create(::custom_interfaces::srv::VelocityRegistration_Request & msg)
  : msg_(msg)
  {}
  ::custom_interfaces::srv::VelocityRegistration_Request create(::custom_interfaces::srv::VelocityRegistration_Request::_create_type arg)
  {
    msg_.create = std::move(arg);
    return std::move(msg_);
  }

private:
  ::custom_interfaces::srv::VelocityRegistration_Request msg_;
};

class Init_VelocityRegistration_Request_record
{
public:
  Init_VelocityRegistration_Request_record()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_VelocityRegistration_Request_create record(::custom_interfaces::srv::VelocityRegistration_Request::_record_type arg)
  {
    msg_.record = std::move(arg);
    return Init_VelocityRegistration_Request_create(msg_);
  }

private:
  ::custom_interfaces::srv::VelocityRegistration_Request msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::custom_interfaces::srv::VelocityRegistration_Request>()
{
  return custom_interfaces::srv::builder::Init_VelocityRegistration_Request_record();
}

}  // namespace custom_interfaces


namespace custom_interfaces
{

namespace srv
{

namespace builder
{

class Init_VelocityRegistration_Response_message
{
public:
  Init_VelocityRegistration_Response_message()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::custom_interfaces::srv::VelocityRegistration_Response message(::custom_interfaces::srv::VelocityRegistration_Response::_message_type arg)
  {
    msg_.message = std::move(arg);
    return std::move(msg_);
  }

private:
  ::custom_interfaces::srv::VelocityRegistration_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::custom_interfaces::srv::VelocityRegistration_Response>()
{
  return custom_interfaces::srv::builder::Init_VelocityRegistration_Response_message();
}

}  // namespace custom_interfaces

#endif  // CUSTOM_INTERFACES__SRV__DETAIL__VELOCITY_REGISTRATION__BUILDER_HPP_
