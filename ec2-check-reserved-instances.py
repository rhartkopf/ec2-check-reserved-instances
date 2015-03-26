#!/usr/bin/env python2.7

"""Check for unused Reserved Instances in AWS

Usage:
  check_aws_ris.py <accesskey> <secretkey> [<aws_region>]

"""

from docopt import docopt
import boto.ec2

debug = 0 # Set to 1 for additional output

def main(docopt_args):

  # Set variables from command line args
  if docopt_args['<aws_region>']:
    region = docopt_args['<aws_region>']
  else:
    region = 'us-east-1'
  key = docopt_args['<accesskey>']
  secret = docopt_args['<secretkey>']

  # Initialize connection to CloudWatch
  c = boto.ec2.connect_to_region(region,
  aws_access_key_id=key,
  aws_secret_access_key=secret,)
  
  # Get running instances
  running_instances = {}
  for r in c.get_all_reservations():
    for i in r.instances:
      if i.state == 'running':
        type = i.instance_type
        az = i.placement
        vpc = 0
        if i.vpc_id:
          if 'vpc' in i.vpc_id:
            vpc = 1
        running_instances[ (type, az, vpc) ] = running_instances.get( (type, az, vpc) , 0 ) + 1

  # Get active reservations
  reserved_instances = {}
  for r in c.get_all_reserved_instances():
    if r.state == 'active':
      type = r.instance_type
      az = r.availability_zone
      vpc = 0
      if 'VPC' in r.description:
        vpc = 1
      reserved_instances[ (type, az, vpc) ] = reserved_instances.get( (type, az, vpc) , 0 ) + r.instance_count

  # this dict will have a positive number if there are unused reservations
  # and negative number if an instance is on demand
  instance_diff = dict([(x, reserved_instances[x] - running_instances.get(x, 0 )) for x in reserved_instances])
  
  # instance_diff only has the keys that were present in reserved_instances. There's probably a cooler way to add a filtered dict here
  for placement_key in running_instances:
  	if not placement_key in reserved_instances:
  		instance_diff[placement_key] = -running_instances[placement_key]
  
  # pprint ( instance_diff )
  
  unused_reservations = dict((key,value) for key, value in instance_diff.iteritems() if value > 0)
  if unused_reservations == {}:
    print "Congratulations, you have no unused reservations"
  else:
    for u in unused_reservations:
      print "UNUSED RESERVATION!\t(%s)\t%s\t%s" % ( unused_reservations[ u ], u[0], u[1] )
  
  unreserved_instances = dict((key,-value) for key, value in instance_diff.iteritems() if value < 0)
  if unreserved_instances == {}:
    print "Congratulations, you have no unreserved instances"
  else:
    for u in unreserved_instances:
      print "Instance not reserved:\t(%s)\t%s\t%s" % ( unreserved_instances[ u ], u[0], u[1] )
  
  qty_running_instances = reduce( lambda x, y: x+y, running_instances.values() )
  qty_reserved_instances = reduce( lambda x, y: x+y, reserved_instances.values() )
  
  print "\n(%s) running on-demand instances\n(%s) purchased reservations" % ( qty_running_instances, qty_reserved_instances )


# Run the main function
if __name__ == '__main__':
  args = docopt(__doc__)
  main(args)
