from __future__ import print_function

from sestools import email_message_from_s3_bucket, event_msg_is_to_command, msg_get_header, recipient_destination_overlap
from cnc import handle_command

from config import email_bucket

from listobj import List

def lambda_handler(event, context):
    with email_message_from_s3_bucket(event, email_bucket) as msg:
        # If it's a command, handle it as such.
        command_address = event_msg_is_to_command(event, msg)
        if command_address:
            print('Message addressed to command ({}).'.format(command_address))
            handle_command(command_address, msg)
            return
        
        print('Message from {}.'.format(msg_get_header(msg, 'from')))
        # See if the message was sent to any known lists.
        for l in List.lists_for_addresses(recipient_destination_overlap(event)):
            print('Sending to list {}.'.format(l.address))
            l.send(msg)
