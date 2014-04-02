Zen Reactive Platform 
======================

Reactive programming is a declarative programming paradigm much like
functional programming.  It's more suited for defining data flows, and
unlike functional programming, Reactive objects are stateful.

Reactive objects are not directly manipulated, but rather state transitions 
and other object modifications and mutations are explicitly and exclusively 
performed through the use of events.  This is known as Event Sourcing.

Contrast this with imperative style programming where data manipulation occurs
through the use of functions and methods.

In Reactive, objects generally* are not persisted, but rather the events
that are used to construct, manipulate and transition the objects are
persisted.

*For performance reasons, states of objects may be cached in the 
persistence layer to eliminate the need of having to replay all events 
during startup and for comparing states between two event layers.

Reference Implementation
-------------------------

This Python reference implementation of the Zen Reactive Platform, which 
utilizes a reactive stateful event sourcing programming paradigm on top of
an in-memory object oriented database.

The purpose of this reference implementation is to help others understand 
the benefits of such a design with regards to Big Data, data mining, 
enterprise architecture, financial systems, social networks, and a myriad 
of other applications.

Why Python?
-----------

While other languages would be more appropriate as the final 
implementation, Python offers a) ease of legibility and b) quick time
to market while still c) providing a useful implementation.

Why MongoDB?
------------

For the back-end persistence layer I've chosen MongoDB for it's 
scalability, ease of use, and transparency.


