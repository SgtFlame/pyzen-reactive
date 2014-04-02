Zen Reactive Platform 
======================

Zen Reactive Platform is a reactive, stateful, event sourcing software platform
combined with an enterprise service bus and an in-memory object oriented database.

Reactive programming is a declarative programming paradigm.  Reactive values are
declared much like functional programming, except reactive values maintain dependency
graphs.  If any values that a function relies upon are modified then the function
is flagged for re-evaluation.  If the function has an active subscription then it
is re-evaluated and the results are pushed to subscriber(s).

This makes Reactive very well suited for defining data flows in a very natural 
unintrusive manner.

Reactive objects are not directly manipulated, but rather state transitions 
and other object modifications and mutations are explicitly and exclusively 
performed through the use of events.  This is known as Event Sourcing.

Contrast this with imperative style programming where data manipulation occurs
through the use of functions and methods.

In Reactive, objects generally* are not persisted, but rather the events that 
are used to construct, manipulate and transition the objects are persisted.

*For performance reasons, states of objects may be cached in the 
persistence layer to eliminate the need of having to replay all events 
during startup and for comparing states between two event layers.

References
----------
Event Sourcing: 
 * http://martinfowler.com/eaaDev/EventSourcing.html
 * http://en.wikipedia.org/wiki/Domain-driven_design
 * http://codebetter.com/gregyoung/2010/02/20/why-use-event-sourcing/
 
Reactive: 
 * http://news.dice.com/2013/12/06/why-reactive-programming-for-databases-is-awesome/
 * http://en.wikipedia.org/wiki/Reactive_programming
 * https://www.coursera.org/course/reactive

Reference Implementation
-------------------------

This git repository is a reference implementation of the Zen Reactive Platform.

The purpose of this reference implementation is to help others understand 
the benefits of such a design with regards to Big Data, data mining, 
enterprise architecture, financial systems, social networks, and a myriad 
of other applications.  

As a reference implementation, the goal is to experiment, explore, learn, and 
teach without the complexity of a production quality system with redundancy, 
high availability, etc.

Why Python?
-----------

While other languages would be more appropriate as the final production quality 
implementation, Python offers a) ease of legibility and b) quick time
to market while still c) providing a useful implementation.

Why MongoDB?
------------

For the back-end persistence layer I've chosen MongoDB for it's 
scalability, ease of use, and transparency.


