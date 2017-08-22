import discord
import asyncio

import apsbot.base as base


@base.apsfunc
async def help(client, message): # pylint: disable=W0622
    '''
    *Cheeky, ain't ya?*
    **{0}help** [*cmd*]
    Displays a list of commands. If [*cmd*] is supplied, provides help about a specific command.
    *Example: `{0}help help`*
    '''

    params = message.content.split()
    if len(params) == 1:
        msg = 'These are my commands:\n'

        dect = {} # Oh god here we go

        for x in base.functions: # in with dictionaries gives keys, which are strings.
            # If a function is based upon a specific server (defined by a function's "server" attribute, which it may or may not have)
            if hasattr(base.functions[x], 'server'):
                if base.functions[x].server != 'hidden':
                    # Append to a key with that server's name
                    try:
                        dect[base.functions[x].server].append(x)
                    except KeyError:
                        dect[base.functions[x].server] = []
                        dect[base.functions[x].server].append(x)
            else:
                try:
                    dect['all'].append(x)
                except KeyError:
                    dect['all'] = []
                    dect['all'].append(x)

        msg += '__**Global Commands**__\n'
        msg += ' '.join(sorted(dect['all']))
        msg += '\n\n'
        for x in sorted(dect):
            if x != 'all':
                msg += '__**{}**__\n'.format(x)
                msg += ' '.join(sorted(dect[x]))
                msg += '\n\n'

        msg += 'Use `{0}help [`*`command`*`]` to get more information about a command. **Please look up the help string for a command before using it or asking questions about it. Thank you!**'.format(
            base.config['invoker']
            )
        await client.send_message(message.channel, msg)
    else:
        if params[1] in base.functions:
            # check for docstring
            if base.functions[params[1]].__doc__:
                # Use inspect.getdoc() to clean the docstring up.
                await client.send_message(message.channel, inspect.getdoc(base.functions[params[1]]).format(
                    base.config['invoker'],
                    base.config['git']['repo_author'],
                    base.config['git']['repo_name']
                ))
            else:
                await client.send_message(message.channel, ':heavy_exclamation_mark: This command has no docstring! Go tell UnFUsion that it\'s broken.')
        else:
            for x in base.functions:
                if hasattr(base.functions[x], 'server') and params[1].lower() == base.functions[x].server.lower():
                    await client.send_message(message.channel, '{}: ...Why did you just try to look up the help for a command category? I tried to split up the help message into categories so they could be read easier. Those big headers with the underlines and everything? Those are *categories*. There isn\'t a command called {}. (Why do so many people get this wrong? It\'s infuriating.)\n\n*~Orangestar, Bot maintainer.*'.format(
                        message.author.display_name,
                        params[1]
                        ))
                    return
            await client.send_message(message.channel, ':no_entry_sign: That command does not exist.')
		
