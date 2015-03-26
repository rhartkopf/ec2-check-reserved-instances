ec2-check-reserved-instances
============================

EC2 Check Reserved Instances - Compare instance reservations with running instances

Amazon's reserved instances (ec2-describe-reserved-instances, ec2-describe-reserved-instances-offerings) are a great way to save money when using EC2. An EC2 instance reservation is specified by an availability zone, instance type, and quantity. Correlating the reservations you currently have active with your running instances is a manual, time-consuming, and error prone process.

This quick little Python script uses boto to inspect your reserved instances and running instances to determine if you currently have any reserved instances which are not being used. Additionally, it will give you a list of non-reserved instances which could benefit from additional reserved instance allocations.

To use the program, make sure you have boto and docopt installed. If you don't already have boto, run:

$ easy_install boto

or

$ pip install boto


EXAMPLE OUTPUT
===============
```
$ ./ec2-check-reserved-instances.py <accesskey> <secretkey> <region>
Unused reservations:    (#)     Type            AZ              VPC
                        (2)     c3.large        us-west-1a      0
                        (2)     c3.xlarge       us-west-1a      0
                        (1)     m3.medium       us-west-1a      0
                        (1)     m1.small        us-west-1a      0

Instances not reserved: (#)     Type            AZ              VPC
                        (1)     c3.xlarge       us-west-1a      1
                        (1)     t2.small        us-west-1a      1
                        (1)     m3.xlarge       us-west-1a      1
                        (2)     c3.2xlarge      us-west-1a      1
                        (2)     c3.large        us-west-1a      1
                        (1)     m3.medium       us-west-1a      1
                        (1)     m1.small        us-west-1a      1

(9) running on-demand instances
(6) purchased reservations
```


TODO
===============
- Fix VPC support for accounts that do not have EC2 Standard support
