PyAspects is a project to ease aspect-oriented programming in Python language.

### Basic Usage ###

"weave" convenience function can use ordinary functions to apply
aspects to a class, object or a method.

- When used with a class, all methods of the class will be
  weaved. This will affect all instances of the class.

- When used with an object, all methods of the object will be
  weaved. But this won't affect any other instances of the same
  class.

- When used with a method, only that particular method will be
  weaved.

Example:
Using the convenience function w/o creating an aspect.


def my_before_func(wobj, data, *args, **kwargs):
    # wobj: the object that is wrapped
    # data: aspect's data where you can get information about the weaved method
    # args: arguments passed to the original method
    # kwargs: keywords passed to the original method
    do_something()

pyaspects.weave(some_object_class_or_method, before_func=my_before_func)


Using an aspect to weave a method, class, object.

pyaspects.weave_all_methods(MyAspect(), MyClass)
pyaspects.weave_all_methods(MyAspect(), MyClass.my_method)
pyaspects.weave_all_methods(MyAspect(), my_instance)
pyaspects.weave_all_methods(MyAspect(), my_instance.my_method)


### Types of Advices ###

With pyaspects you can inject some code before, after or instead
(around) of a method.

before and after advices are quite strait-forward they basically get
the object and arguments of the method and run before/after the
execution of the method. You can have as many before/after advices as
you want to.

On the other hand, a method can only have one around advise. This is
because around advice will be run in place and it's return value will
be used instead. But, around advice can invoke the original method
using the proceed method of the MetaAspect.


### What is in "data" ###

The data argument passed to aspects is a dictionary and provides
information about the weaved method.

data['original_method_name'] : The method name before weaving happens.

data['method_name'] : Weaved method name. This is basically the method
"proceed" will call in around aspect.

data['method_return_value'] : Return value of the original
method. This will be available only to after aspect and around aspect
(if it calls proceed).

data['__class__'] : Class object that the method belongs to.

### How to define a new aspect ###

Aspects can provide methods to be executed before or after the weaved
methods.

Example: 

class TestAspect:
    __metaclass__ = MetaAspect
    name = "TestAspect"

    def after(self, wobj, data, *args, **kwargs):
        print "Test aspect"


class MyAroundAspect:
    __metaclass__ = MetaAspect
    name = "MyAround"

    def around(self, wobj, data, *args, **kwargs):
        print "running around."
        ret = self.proceed(wobj, data, *args, **kwargs)
        print "do something with return value"
        return ret

