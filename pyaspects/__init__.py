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

__version__ = "0.4.1"

from pyaspects.weaver import weave_method, weave_all_methods, AspectError

##
# convenience function to weave a class/object/method
def weave(class_or_object_or_method, before_func=None, after_func=None):

    import types
    from pyaspects.meta import MetaAspect

    
    dummy_aspect_name = "DummyAspect"
    if before_func:
        dummy_aspect_name += "_before_%s" % before_func.__name__
    if after_func:
        dummy_aspect_name += "_after_%s" % after_func.__name__

    class DummyAspect:
        __metaclass__ = MetaAspect
        name = dummy_aspect_name

        def before(self, wobj, data, *args, **kwargs):
            if before_func:
                before_func(wobj, data, *args, **kwargs)

        def after(self, wobj, data, *args, **kwargs):
            if after_func:
                after_func(wobj, data, *args, **kwargs)


    x = class_or_object_or_method
    type_x = type(x)
    if type_x in (types.ClassType, types.InstanceType):
        weave_all_methods(DummyAspect(), x)

    elif type_x == types.MethodType:
        if x.im_self: # object method
            weave_method(DummyAspect(), x.im_self, x.__name__)
        else:
            weave_method(DummyAspect(), x.im_class, x.__name__)


        

        

    
