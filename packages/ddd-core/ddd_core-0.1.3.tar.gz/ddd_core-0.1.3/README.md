# Domain Driven Design Core


## Description

The application of Domain Driven Design is not easy in general. The goal of this library is to be easy and well guided to develop ,.
Not only ideas or DDD are used. CQRS and event sourcing are good suplements to this theory and it is a bit merged in this library.

## Installation

This project has an automated deployment to pypi, so only is needed to use pip command:

```
>> pip install ddd-core
```

There is no external requirements for this library.

## Usage

The use of this library is by inheritance. If you want to create a Value Object you only have to inherit from a Value class. If you want to have an aggregate, inherit from a Aggregate class, if a service from a Service class.
It is planned to be widely docummented the behaviour is inherited from these classes.

I know composition is better than inheritance but a base class for each concept is the clearer way to implement DDD with OO programming.

## Support

Send any suggestion to sruiz@indoorclima.com or salvador.ruiz.r@gmail.com. Any ideas or support is well recieved.

## Roadmap

- [ ] Increment versioning when pushing
- [ ] Integrate with gitlab continuous integration to publish to pypi as library
- [ ] Improve coverage rate to > 96%
- [ ] Improve usage documentation with sphinx
- [ ] Upload to readthedocs

## Contributing
State if you are open to contributions and what your requirements are for accepting them.

For people who want to make changes to your project, it's helpful to have some documentation on how to get started. Perhaps there is a script that they should run or some environment variables that they need to set. Make these steps explicit. These instructions could also be useful to your future self.

You can also document commands to lint the code or run tests. These steps help to ensure high code quality and reduce the likelihood that the changes inadvertently break something. Having instructions for running tests is especially helpful if it requires external setup, such as starting a Selenium server for testing in a browser.

## Authors and acknowledgment

For sure the ideas of Eric Evans and Domain Design Development are the base of this project to be used with python language. Without this seed it has not sensse



## License

This is under LGPL lincense. You can use and modify this library.

## Project status

It is used in projects developed currently by the company IndoorClima.
