// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from custom_interfaces:srv/GuideSelected.idl
// generated code does not contain a copyright notice

#ifndef CUSTOM_INTERFACES__SRV__DETAIL__GUIDE_SELECTED__BUILDER_HPP_
#define CUSTOM_INTERFACES__SRV__DETAIL__GUIDE_SELECTED__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "custom_interfaces/srv/detail/guide_selected__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace custom_interfaces
{

namespace srv
{

namespace builder
{

class Init_GuideSelected_Request_choice
{
public:
  Init_GuideSelected_Request_choice()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::custom_interfaces::srv::GuideSelected_Request choice(::custom_interfaces::srv::GuideSelected_Request::_choice_type arg)
  {
    msg_.choice = std::move(arg);
    return std::move(msg_);
  }

private:
  ::custom_interfaces::srv::GuideSelected_Request msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::custom_interfaces::srv::GuideSelected_Request>()
{
  return custom_interfaces::srv::builder::Init_GuideSelected_Request_choice();
}

}  // namespace custom_interfaces


namespace custom_interfaces
{

namespace srv
{

namespace builder
{

class Init_GuideSelected_Response_message
{
public:
  Init_GuideSelected_Response_message()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::custom_interfaces::srv::GuideSelected_Response message(::custom_interfaces::srv::GuideSelected_Response::_message_type arg)
  {
    msg_.message = std::move(arg);
    return std::move(msg_);
  }

private:
  ::custom_interfaces::srv::GuideSelected_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::custom_interfaces::srv::GuideSelected_Response>()
{
  return custom_interfaces::srv::builder::Init_GuideSelected_Response_message();
}

}  // namespace custom_interfaces

#endif  // CUSTOM_INTERFACES__SRV__DETAIL__GUIDE_SELECTED__BUILDER_HPP_
