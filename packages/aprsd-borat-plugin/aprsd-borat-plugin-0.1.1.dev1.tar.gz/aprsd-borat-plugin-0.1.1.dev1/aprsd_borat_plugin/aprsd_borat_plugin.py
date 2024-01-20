import logging
import random
import textwrap

from aprsd import packets, plugin
from aprsd.utils import trace
from oslo_config import cfg

import aprsd_borat_plugin
from aprsd_borat_plugin import conf  # noqa
from aprsd_borat_plugin import quotes


CONF = cfg.CONF
LOG = logging.getLogger("APRSD")


class BoratPlugin(plugin.APRSDRegexCommandPluginBase):

    version = aprsd_borat_plugin.__version__
    # Change this regex to match for your plugin's command
    # Tutorial on regex here: https://regexone.com/
    # Look for any command that starts with w or W
    command_regex = "^[bB]"
    # the command is for ?
    # Change this value to a 1 word description of the plugin
    # this string is used for help
    command_name = "Borat"

    enabled = False

    def setup(self):
        """Allows the plugin to do some 'setup' type checks in here.

        If the setup checks fail, set the self.enabled = False.  This
        will prevent the plugin from being called when packets are
        received."""
        # Do some checks here?
        self.enabled = True

    @trace.trace
    def process(self, packet: packets.core.Packet):

        """This is called when a received packet matches self.command_regex.

        This is only called when self.enabled = True and the command_regex
        matches in the contents of the packet["message_text"]."""

        # Now we can process
        text = random.choice(quotes.BORAT_QUOTES)
        LOG.info(text)
        choice = textwrap.wrap(text, 67, break_long_words=False)
        return choice
