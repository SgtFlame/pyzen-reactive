pyzen-reactive
==============

Python reference implementation of the Zen Reactive Database, which 
is a a reactive stateful event driven in-memory database.

The purpose of this reference implementation is to help others
understand the benefits of such a design with regards to Big Data,
data mining, enterprise architecture, financial systems, social networks, 
and a myriad of other applications.

Why Python?
-----------

While other languages would be more appropriate as the final 
implementation, Python offers a) ease of legibility and b) quick time
to market while still c) providing a useful implementation.

Why MongoDB?
------------

For the back-end persistence layer I've chosen MongoDB for it's 
scalability, ease of use, and transparency.

More about Reactive
--------------------

Reactive programming is a declarative programming paradigm much like
functional programming.  It's more suited for defining data flows.

Unlike functional programming, Reactive objects are stateful.

State transitions and other object modifications and mutations are
explicitly and exclusively performed through the use of events.  Contrast
this with imperative style programming where data manipulation occurs
through the use of functions and methods.

In Reactive, objects generally* are not persisted, but rather the events
that are used to construct, manipulate and transition the objects are
persisted.

*For performance reasons, states of objects may be cached in the 
persistence layer to eliminate the need of having to replay all events 
during startup and for comparing states between two event layers.

