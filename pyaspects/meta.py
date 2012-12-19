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


# Aspect is an unit encapsulating cross-cutting conserns.
#
# meta.py module defines a metaclass called MetaAspects.
#
# Every aspect class should set this as __metaclass__


import inspect
from pyaspects.pointcut import PointCut


##
# MetaAspect is a metaclass that creates an Aspect class.
class MetaAspect(type):

    ##
    # create a new class with the necessity members
    def __new__(cls, classname, bases, classdict):
        _pointcut = PointCut()

        def updatePointCut(cls, pc):
            for wobj, met_names in pc.items():
                for met_name in met_names:
                    cls._pointcut.addMethod(wobj, met_name)

        def before(cls, _wobj_, _wobj_data_, *args, **kwargs):
            if cls.hasJoinPoint(_wobj_, _wobj_data_):
                    met = getattr(cls, 'before__original')
                    return met.im_func(cls, _wobj_, _wobj_data_, *args, **kwargs)

        def after(cls, _wobj_, _wobj_data_, *args, **kwargs):
            if cls.hasJoinPoint(_wobj_, _wobj_data_):
                    met = getattr(cls, 'after__original')
                    return met.im_func(cls, _wobj_, _wobj_data_, *args, **kwargs)

        def around(cls, _wobj_, _wobj_data_, *args, **kwargs):
            if cls.hasJoinPoint(_wobj_, _wobj_data_):
                    met = getattr(cls, 'around__original')
                    return met.im_func(cls, _wobj_, _wobj_data_, *args, **kwargs)

        def hasJoinPoint(cls, _wobj_, _wobj_data_):
            met_name = _wobj_data_['original_method_name']

            if cls._pointcut.has_key(_wobj_):
                if met_name in cls._pointcut[_wobj_]:
                    return True

            ##
            # Try object's class if instance is not found
            klass = _wobj_data_['__class__']
            if cls._pointcut.has_key(klass):
                if met_name in cls._pointcut[klass]:
                    return True

            return False

        def proceed(cls, _wobj_, _wobj_data_, *args, **kwargs):
            # continue on running the original method
            if _wobj_data_.has_key('original_method'):
                return _wobj_data_['original_method'](_wobj_, *args, **kwargs)

        # bind/rebind methods/attributes
        if classdict.has_key('before'):
            classdict['before__original'] = classdict['before']
            classdict['before'] = before
        if classdict.has_key('after'):
            classdict['after__original'] = classdict['after']
            classdict['after'] = after
        if classdict.has_key('around'):
            classdict['around__original'] = classdict['around']
            classdict['around'] = around
            classdict['proceed'] = proceed
        classdict['_pointcut'] = _pointcut
        classdict['updatePointCut'] = updatePointCut
        classdict['hasJoinPoint'] = hasJoinPoint

        selfclass = super(MetaAspect, cls).__new__\
            (cls, classname, bases, classdict)
        return selfclass

