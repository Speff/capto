#/usr/bin/env python3

__all__ = ['validate_args', 'label_type', 'webhook_url_type',
        'twit_target_type', 'yes_no_type', 'uid_type']

def validate_args(args):
    #if args['label'] == '':
    #    return False
    return True

def uid_type(input):
    if len(input) != 36:
        raise ValueError(f'{name} invalid')
    return input
def label_type(input):
    if len(input) > 31:
        raise ValueError(f'{name} must be less than 32 characters')
    return input
def webhook_url_type(input):
    return input
def twit_target_type(input):
    return input
def yes_no_type(input):
    if input not in ['Yes', 'No']:
        raise ValueError(f'{name} must be Yes or No')
    return input

