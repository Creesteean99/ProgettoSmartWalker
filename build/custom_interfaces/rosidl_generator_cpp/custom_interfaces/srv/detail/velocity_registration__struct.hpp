// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from custom_interfaces:srv/VelocityRegistration.idl
// generated code does not contain a copyright notice

#ifndef CUSTOM_INTERFACES__SRV__DETAIL__VELOCITY_REGISTRATION__STRUCT_HPP_
#define CUSTOM_INTERFACES__SRV__DETAIL__VELOCITY_REGISTRATION__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__custom_interfaces__srv__VelocityRegistration_Request __attribute__((deprecated))
#else
# define DEPRECATED__custom_interfaces__srv__VelocityRegistration_Request __declspec(deprecated)
#endif

namespace custom_interfaces
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct VelocityRegistration_Request_
{
  using Type = VelocityRegistration_Request_<ContainerAllocator>;

  explicit VelocityRegistration_Request_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->record = false;
      this->create = false;
    }
  }

  explicit VelocityRegistration_Request_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->record = false;
      this->create = false;
    }
  }

  // field types and members
  using _record_type =
    bool;
  _record_type record;
  using _create_type =
    bool;
  _create_type create;

  // setters for named parameter idiom
  Type & set__record(
    const bool & _arg)
  {
    this->record = _arg;
    return *this;
  }
  Type & set__create(
    const bool & _arg)
  {
    this->create = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    custom_interfaces::srv::VelocityRegistration_Request_<ContainerAllocator> *;
  using ConstRawPtr =
    const custom_interfaces::srv::VelocityRegistration_Request_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<custom_interfaces::srv::VelocityRegistration_Request_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<custom_interfaces::srv::VelocityRegistration_Request_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      custom_interfaces::srv::VelocityRegistration_Request_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<custom_interfaces::srv::VelocityRegistration_Request_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      custom_interfaces::srv::VelocityRegistration_Request_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<custom_interfaces::srv::VelocityRegistration_Request_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<custom_interfaces::srv::VelocityRegistration_Request_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<custom_interfaces::srv::VelocityRegistration_Request_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__custom_interfaces__srv__VelocityRegistration_Request
    std::shared_ptr<custom_interfaces::srv::VelocityRegistration_Request_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__custom_interfaces__srv__VelocityRegistration_Request
    std::shared_ptr<custom_interfaces::srv::VelocityRegistration_Request_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const VelocityRegistration_Request_ & other) const
  {
    if (this->record != other.record) {
      return false;
    }
    if (this->create != other.create) {
      return false;
    }
    return true;
  }
  bool operator!=(const VelocityRegistration_Request_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct VelocityRegistration_Request_

// alias to use template instance with default allocator
using VelocityRegistration_Request =
  custom_interfaces::srv::VelocityRegistration_Request_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace custom_interfaces


#ifndef _WIN32
# define DEPRECATED__custom_interfaces__srv__VelocityRegistration_Response __attribute__((deprecated))
#else
# define DEPRECATED__custom_interfaces__srv__VelocityRegistration_Response __declspec(deprecated)
#endif

namespace custom_interfaces
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct VelocityRegistration_Response_
{
  using Type = VelocityRegistration_Response_<ContainerAllocator>;

  explicit VelocityRegistration_Response_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->message = "";
    }
  }

  explicit VelocityRegistration_Response_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : message(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->message = "";
    }
  }

  // field types and members
  using _message_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _message_type message;

  // setters for named parameter idiom
  Type & set__message(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->message = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    custom_interfaces::srv::VelocityRegistration_Response_<ContainerAllocator> *;
  using ConstRawPtr =
    const custom_interfaces::srv::VelocityRegistration_Response_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<custom_interfaces::srv::VelocityRegistration_Response_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<custom_interfaces::srv::VelocityRegistration_Response_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      custom_interfaces::srv::VelocityRegistration_Response_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<custom_interfaces::srv::VelocityRegistration_Response_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      custom_interfaces::srv::VelocityRegistration_Response_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<custom_interfaces::srv::VelocityRegistration_Response_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<custom_interfaces::srv::VelocityRegistration_Response_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<custom_interfaces::srv::VelocityRegistration_Response_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__custom_interfaces__srv__VelocityRegistration_Response
    std::shared_ptr<custom_interfaces::srv::VelocityRegistration_Response_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__custom_interfaces__srv__VelocityRegistration_Response
    std::shared_ptr<custom_interfaces::srv::VelocityRegistration_Response_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const VelocityRegistration_Response_ & other) const
  {
    if (this->message != other.message) {
      return false;
    }
    return true;
  }
  bool operator!=(const VelocityRegistration_Response_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct VelocityRegistration_Response_

// alias to use template instance with default allocator
using VelocityRegistration_Response =
  custom_interfaces::srv::VelocityRegistration_Response_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace custom_interfaces

namespace custom_interfaces
{

namespace srv
{

struct VelocityRegistration
{
  using Request = custom_interfaces::srv::VelocityRegistration_Request;
  using Response = custom_interfaces::srv::VelocityRegistration_Response;
};

}  // namespace srv

}  // namespace custom_interfaces

#endif  // CUSTOM_INTERFACES__SRV__DETAIL__VELOCITY_REGISTRATION__STRUCT_HPP_
