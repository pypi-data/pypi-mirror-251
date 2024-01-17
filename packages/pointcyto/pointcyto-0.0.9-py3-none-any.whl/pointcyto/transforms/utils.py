def standard_repr(self: object):
    self_dict_str = []
    for key, value in self.__dict__.items():
        if isinstance(value, str):
            self_dict_str.append(key + "='" + value + "'")
        else:
            self_dict_str.append(key + "=" + str(value))
    joined_self_dict = ", ".join(self_dict_str)
    return self.__class__.__name__ + "(" + joined_self_dict + ")"
