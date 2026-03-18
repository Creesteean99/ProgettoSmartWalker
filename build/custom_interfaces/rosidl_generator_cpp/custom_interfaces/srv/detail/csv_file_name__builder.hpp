// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from custom_interfaces:srv/CSVFileName.idl
// generated code does not contain a copyright notice

#ifndef CUSTOM_INTERFACES__SRV__DETAIL__CSV_FILE_NAME__BUILDER_HPP_
#define CUSTOM_INTERFACES__SRV__DETAIL__CSV_FILE_NAME__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "custom_interfaces/srv/detail/csv_file_name__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace custom_interfaces
{

namespace srv
{

namespace builder
{

class Init_CSVFileName_Request_directory
{
public:
  explicit Init_CSVFileName_Request_directory(::custom_interfaces::srv::CSVFileName_Request & msg)
  : msg_(msg)
  {}
  ::custom_interfaces::srv::CSVFileName_Request directory(::custom_interfaces::srv::CSVFileName_Request::_directory_type arg)
  {
    msg_.directory = std::move(arg);
    return std::move(msg_);
  }

private:
  ::custom_interfaces::srv::CSVFileName_Request msg_;
};

class Init_CSVFileName_Request_filename
{
public:
  Init_CSVFileName_Request_filename()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_CSVFileName_Request_directory filename(::custom_interfaces::srv::CSVFileName_Request::_filename_type arg)
  {
    msg_.filename = std::move(arg);
    return Init_CSVFileName_Request_directory(msg_);
  }

private:
  ::custom_interfaces::srv::CSVFileName_Request msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::custom_interfaces::srv::CSVFileName_Request>()
{
  return custom_interfaces::srv::builder::Init_CSVFileName_Request_filename();
}

}  // namespace custom_interfaces


namespace custom_interfaces
{

namespace srv
{

namespace builder
{

class Init_CSVFileName_Response_message
{
public:
  Init_CSVFileName_Response_message()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::custom_interfaces::srv::CSVFileName_Response message(::custom_interfaces::srv::CSVFileName_Response::_message_type arg)
  {
    msg_.message = std::move(arg);
    return std::move(msg_);
  }

private:
  ::custom_interfaces::srv::CSVFileName_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::custom_interfaces::srv::CSVFileName_Response>()
{
  return custom_interfaces::srv::builder::Init_CSVFileName_Response_message();
}

}  // namespace custom_interfaces

#endif  // CUSTOM_INTERFACES__SRV__DETAIL__CSV_FILE_NAME__BUILDER_HPP_
