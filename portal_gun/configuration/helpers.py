import json
from os import path

from portal_gun.configuration.schemas import ConfigSchema, PortalSchema, ValidationError
from portal_gun.context_managers.step import step


def get_config(args):
	# Parse global config
	with step('Parse config file', catch=[IOError, ValueError]):
		with open(args.config) as config_file:
			config_data = json.load(config_file)

	# Validate global config
	with step('Validate config', catch=[ValidationError]):
		config = ConfigSchema().load(config_data)

	return config


def get_portal_spec(args):
	# Get portal name and spec file
	portal_name = args.portal.rsplit('.', 1)[0]
	spec_filename = '{}.json'.format(portal_name)

	# Ensure spec file exists
	with step('Locate portal specification file'):
		if not path.exists(spec_filename):
			raise Exception('Could not find portal specification file `{}`.'.format(spec_filename))

	# Parse portal spec file
	with step('Parse portal specification file', catch=[IOError, ValueError]):
		with open(spec_filename) as spec_file:
			portal_spec_data = json.load(spec_file)

	# Validate portal spec
	with step('Validate portal specification', catch=[ValidationError]):
		portal_spec = PortalSchema().load(portal_spec_data)

	return portal_spec, portal_name