# generated from rosidl_generator_py/resource/_idl.py.em
# with input from custom_interfaces:msg/Parameter.idl
# generated code does not contain a copyright notice


# Import statements for member types

import builtins  # noqa: E402, I100

import math  # noqa: E402, I100

import rosidl_parser.definition  # noqa: E402, I100


class Metaclass_Parameter(type):
    """Metaclass of message 'Parameter'."""

    _CREATE_ROS_MESSAGE = None
    _CONVERT_FROM_PY = None
    _CONVERT_TO_PY = None
    _DESTROY_ROS_MESSAGE = None
    _TYPE_SUPPORT = None

    __constants = {
    }

    @classmethod
    def __import_type_support__(cls):
        try:
            from rosidl_generator_py import import_type_support
            module = import_type_support('custom_interfaces')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'custom_interfaces.msg.Parameter')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__msg__parameter
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__msg__parameter
            cls._CONVERT_TO_PY = module.convert_to_py_msg__msg__parameter
            cls._TYPE_SUPPORT = module.type_support_msg__msg__parameter
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__msg__parameter

            from geometry_msgs.msg import Point
            if Point.__class__._TYPE_SUPPORT is None:
                Point.__class__.__import_type_support__()

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class Parameter(metaclass=Metaclass_Parameter):
    """Message class 'Parameter'."""

    __slots__ = [
        '_guide_type',
        '_start_point',
        '_end_point',
        '_thickness',
        '_amplitude',
        '_record',
    ]

    _fields_and_field_types = {
        'guide_type': 'int32',
        'start_point': 'geometry_msgs/Point',
        'end_point': 'geometry_msgs/Point',
        'thickness': 'float',
        'amplitude': 'float',
        'record': 'boolean',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.BasicType('int32'),  # noqa: E501
        rosidl_parser.definition.NamespacedType(['geometry_msgs', 'msg'], 'Point'),  # noqa: E501
        rosidl_parser.definition.NamespacedType(['geometry_msgs', 'msg'], 'Point'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('boolean'),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        self.guide_type = kwargs.get('guide_type', int())
        from geometry_msgs.msg import Point
        self.start_point = kwargs.get('start_point', Point())
        from geometry_msgs.msg import Point
        self.end_point = kwargs.get('end_point', Point())
        self.thickness = kwargs.get('thickness', float())
        self.amplitude = kwargs.get('amplitude', float())
        self.record = kwargs.get('record', bool())

    def __repr__(self):
        typename = self.__class__.__module__.split('.')
        typename.pop()
        typename.append(self.__class__.__name__)
        args = []
        for s, t in zip(self.__slots__, self.SLOT_TYPES):
            field = getattr(self, s)
            fieldstr = repr(field)
            # We use Python array type for fields that can be directly stored
            # in them, and "normal" sequences for everything else.  If it is
            # a type that we store in an array, strip off the 'array' portion.
            if (
                isinstance(t, rosidl_parser.definition.AbstractSequence) and
                isinstance(t.value_type, rosidl_parser.definition.BasicType) and
                t.value_type.typename in ['float', 'double', 'int8', 'uint8', 'int16', 'uint16', 'int32', 'uint32', 'int64', 'uint64']
            ):
                if len(field) == 0:
                    fieldstr = '[]'
                else:
                    assert fieldstr.startswith('array(')
                    prefix = "array('X', "
                    suffix = ')'
                    fieldstr = fieldstr[len(prefix):-len(suffix)]
            args.append(s[1:] + '=' + fieldstr)
        return '%s(%s)' % ('.'.join(typename), ', '.join(args))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        if self.guide_type != other.guide_type:
            return False
        if self.start_point != other.start_point:
            return False
        if self.end_point != other.end_point:
            return False
        if self.thickness != other.thickness:
            return False
        if self.amplitude != other.amplitude:
            return False
        if self.record != other.record:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def guide_type(self):
        """Message field 'guide_type'."""
        return self._guide_type

    @guide_type.setter
    def guide_type(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'guide_type' field must be of type 'int'"
            assert value >= -2147483648 and value < 2147483648, \
                "The 'guide_type' field must be an integer in [-2147483648, 2147483647]"
        self._guide_type = value

    @builtins.property
    def start_point(self):
        """Message field 'start_point'."""
        return self._start_point

    @start_point.setter
    def start_point(self, value):
        if __debug__:
            from geometry_msgs.msg import Point
            assert \
                isinstance(value, Point), \
                "The 'start_point' field must be a sub message of type 'Point'"
        self._start_point = value

    @builtins.property
    def end_point(self):
        """Message field 'end_point'."""
        return self._end_point

    @end_point.setter
    def end_point(self, value):
        if __debug__:
            from geometry_msgs.msg import Point
            assert \
                isinstance(value, Point), \
                "The 'end_point' field must be a sub message of type 'Point'"
        self._end_point = value

    @builtins.property
    def thickness(self):
        """Message field 'thickness'."""
        return self._thickness

    @thickness.setter
    def thickness(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'thickness' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'thickness' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._thickness = value

    @builtins.property
    def amplitude(self):
        """Message field 'amplitude'."""
        return self._amplitude

    @amplitude.setter
    def amplitude(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'amplitude' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'amplitude' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._amplitude = value

    @builtins.property
    def record(self):
        """Message field 'record'."""
        return self._record

    @record.setter
    def record(self, value):
        if __debug__:
            assert \
                isinstance(value, bool), \
                "The 'record' field must be of type 'bool'"
        self._record = value
