# -*- coding: utf-8 -*-
#
# Copyright (C) 2006-2010, TUBITAK/UEKAE
# Copyright (C) 2010, INRIA
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.


import new
import inspect


from pyaspects.pointcut import PointCut

class AspectError(Exception):
    pass

##
# __weave_method, weaves the method (met_name) of an object (obj) with
# an Aspect instance.
def __weave_method(aspect, obj, met_name):

    def around_aspect(a):
        try:
            return getattr(a, "around")
        except AttributeError:
            return None

    def has_around_aspect(o):
        for a in aspect_dict.values():
            if around_aspect(a):
                return True
        return False

    # set or update the aspects list of weaved object
    try:
        aspect_dict = getattr(obj, '__aspect_dict')
    except:
        # no aspects defined before
        aspect_dict = {}


    if not aspect_dict.has_key(aspect.name):
        if around_aspect(aspect) and has_around_aspect(obj):
            raise AspectError('Already have an aspect that provide "around". Can not apply %s' % aspect.name)
        else:
            aspect_dict[aspect.name] = aspect
    setattr(obj, '__aspect_dict', aspect_dict)


    # new method's data 
    data = {}
    data['original_method_name'] = met_name
    data['method_name'] = '__' + met_name + '_weaved'
    if inspect.isclass(obj):
        data['__class__'] = obj
    else:
        data['__class__'] = obj.__class__


    def __aspect_wrapper(wobj, *args, **kwargs):

        # reset the return value for every call
        data['method_return_value'] = None

        # run aspect's before method
        for a in aspect_dict.values():
            if hasattr(a, "before"):
                a.before(wobj, data, *args, **kwargs)
        

        for a in aspect_dict.values():
            if hasattr(a, "around"):
                # around aspect can run the original method when needed
                data['original_method'] = getattr(obj, data['method_name'])
                ret = a.around(wobj, data, *args, **kwargs)
                data['method_return_value'] = ret
                break
        else:
            # run original method only if the method doesn't have an
            # around aspect.
            met_name = data['method_name']
            met = getattr(wobj, met_name)
            ret =  met.im_func(wobj, *args, **kwargs)
            data['method_return_value'] = ret

        # run aspect's after method
        for a in aspect_dict.values():
            if hasattr(a, "after"):
                a.after(wobj, data, *args, **kwargs)

        return ret

    original_method = getattr(obj, met_name)
    weaved_name = data['method_name']

    # rename the wrapper
    __aspect_wrapper.__name__ = met_name
    __aspect_wrapper.__doc__ = original_method.__doc__

    # don't rebind the weaved method
    if not hasattr(obj, weaved_name):
        setattr(obj, weaved_name, original_method)

    if inspect.isclass(obj):
        new_method = new.instancemethod(__aspect_wrapper, None, obj)
    else:
        new_method = new.instancemethod(__aspect_wrapper, obj, obj.__class__)
    setattr(obj, met_name, new_method)



##
# Weave a method of a class or object
#
# @param class_or_object: Python class or object
# @param met_name: (string) method name
def weave_method(aspect, class_or_object, met_name):
    p = PointCut()
    p.addMethod(class_or_object, met_name)
    aspect.updatePointCut(p)
    __weave_method(aspect, class_or_object, met_name)


##
# weave all methods in class_or_object with an aspect
def weave_all_methods(aspect, class_or_object):
    
    p = PointCut()
    _dict = dict(inspect.getmembers(class_or_object, inspect.ismethod))
    for met_name in _dict:
        if not met_name.startswith('__'):
            p.addMethod(class_or_object, met_name)

    aspect.updatePointCut(p)
    for met_name in _dict:
        if not met_name.startswith('__'):
            __weave_method(aspect, class_or_object, met_name)


# backward-compatibility functions
weave_class_method = weave_method
weave_object_method = weave_method
weave_all_class_methods = weave_all_methods
weave_all_object_methods = weave_all_methods
