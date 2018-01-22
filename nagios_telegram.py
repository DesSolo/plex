#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import argparse
from twx.botapi import TelegramBot

def parse_args():
    parser = argparse.ArgumentParser(description='Nagios notification via Telegram')
    parser.add_argument('-t', '--token', nargs='?', required=True)
    parser.add_argument('-o', '--object_type', nargs='?', required=True)
    parser.add_argument('--contact', nargs='?', required=True)
    parser.add_argument('--notificationtype', nargs='?')
    parser.add_argument('--hoststate', nargs='?')
    parser.add_argument('--hostname', nargs='?')
    parser.add_argument('--hostaddress', nargs='?')
    parser.add_argument('--servicestate', nargs='?')
    parser.add_argument('--servicedesc', nargs='?')
    parser.add_argument('--output', nargs='?')
    parser.add_argument('--servicename', nargs='?')
    parser.add_argument('--datetime', nargs='?')
    args = parser.parse_args()
    return args


def send_notification(token, user_id, message):
    bot = TelegramBot(token)
    bot.send_message(user_id, message, parse_mode='Markdown').wait()


def host_notification(args):
    state = ''
    if args.hoststate == 'UP':
        state = u'\U00002705 '
    elif args.hoststate == 'DOWN':
        state = u'\U0001F525 '
    elif args.hoststate == 'UNREACHABLE':
        state = u'\U00002753 '

    return "%s* %s - %s is %s *\nNotification Type: %s\nHost: %s\nAddress: %s\nState: %s\n\nDate/Time: %s\nAdditional Info:\n`%s`\n" % (
        state,
        args.notificationtype,
        args.hostname.replace("_", "\_"),
        args.hoststate,
        args.notificationtype,
        args.hostname.replace("_", "\_"),
        args.hostaddress,
        args.hoststate,
        str(args.datetime).replace("+", " "),
        args.output
    )


def service_notification(args):
    state = ''
    if args.servicestate == 'OK':
        state = u'\U00002705 '
    elif args.servicestate == 'WARNING':
        state = u'\U000026A0 '
    elif args.servicestate == 'CRITICAL':
        state = u'\U0001F525 '
    elif args.servicestate == 'UNKNOWN':
        state = u'\U00002753 '

    return "%s* %s - %s - %s is %s*\nNotification Type: %s\nService: %s\nHost: %s\nAddress: %s\nState: %s\n\nDate/Time: %s\nAdditional Info:\n`%s`\n" % (
        state,
        args.notificationtype,
        args.hostname.replace("_", "\_"),
        args.servicename.replace("_", "\_"),
        args.servicestate,
        args.notificationtype,
        args.servicedesc.replace("_", "\_"),
        args.hostname.replace("_", "\_"),
        args.hostaddress,
        args.servicestate,
        str(args.datetime).replace("+", " "),
        args.output
    )


def main():
    args = parse_args()
    logging.debug(args)
    user_id = int(args.contact)
    if args.object_type == 'host':
        message = host_notification(args)
    elif args.object_type == 'service':
        message = service_notification(args)
    send_notification(args.token, user_id, message)


if __name__ == '__main__':
    main()
