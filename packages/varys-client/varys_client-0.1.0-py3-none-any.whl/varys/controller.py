import queue
import os

from varys.consumer import consumer
from varys.producer import producer
from varys.utils import configurator


class varys:
    """
    A high-level wrapper for the producer and consumer classes used by varys, abstracting away the tedious details.

    ...

    Attributes
    ----------
    profile : str
        profile name inside the configuration file to use when connecting to RabbitMQ
    configuration_path : str
        path to varys confiruration JSON file, provided with either the config_path argument or the VARYS_CFG environment variable
    _logfile : str
        the path to the logfile to use for logging, provided with the logfile argument
    _log_level : str
        the log level to use for logging, provided with the log_level argument, defaults to DEBUG (the most verbose logging level)
    _credentials : class
        an instance of the configurator class, used to store the RabbitMQ connection credentials
    _in_channels : dict
        a dictionary of consumer classes and queues that have been connected to for receiving messages
    _out_channels : dict
        a dictionary of producer classes and queues that have been connected to for sending messages

    Methods
    -------
    send(message, exchange, queue_suffix=False, exchange_type="fanout")
        Either send a message to an existing exchange, or create a new exchange connection and send the message to it. queue_suffix must be provided when sending a message to a queue for the first time to instantiate a new connection.
    receive(exchange, queue_suffix=False, block=True, timeout=None, exchange_type="fanout")
        Either receive a message from an existing exchange, or create a new exchange connection and receive a message from it. queue_suffix must be provided when receiving a message from a queue for the first time to instantiate a new connection. block determines whether the receive method should block until a message is received or not.
    receive_batch(exchange, queue_suffix=False)
        Either receive a batch of messages from an existing exchange, or create a new exchange connection and receive a batch of messages from it. queue_suffix must be provided when receiving a message from a queue for the first time to instantiate a new connection.
    get_channels()
        Return a dict of all the channels that have been connected to with the keys "consumer_channels" and "producer_channels"
    close()
        Close all open channels
    """

    def __init__(
        self,
        profile,
        logfile,
        log_level="DEBUG",
        config_path=None,
        routing_key="arbitrary_string",
        auto_acknowledge=True,
    ):
        self.profile = profile

        if config_path is None:
            config_path = os.getenv("VARYS_CFG")

        self.configuration_path = config_path

        self.routing_key = routing_key
        self.auto_ack = auto_acknowledge

        self._logfile = logfile
        self._log_level = log_level

        self._credentials = configurator(self.profile, self.configuration_path)

        self._in_channels = {}
        self._out_channels = {}

    def send(self, message, exchange, queue_suffix=False, exchange_type="fanout"):
        """
        Either send a message to an existing exchange, or create a new exchange connection and send the message to it.
        """

        if not self._out_channels.get(exchange):
            if not queue_suffix:
                raise Exception(
                    "Must provide a queue suffix when sending a message to a queue for the first time"
                )

            self._out_channels[exchange] = producer(
                message_queue=queue.Queue(),
                routing_key=self.routing_key,
                exchange=exchange,
                configuration=self._credentials,
                log_file=self._logfile,
                log_level=self._log_level,
                queue_suffix=queue_suffix,
                exchange_type=exchange_type,
            )
            self._out_channels[exchange].start()

        self._out_channels[exchange]._message_queue.put(message)

    def receive(
        self,
        exchange,
        queue_suffix=False,
        block=True,
        timeout=None,
        exchange_type="fanout",
    ):
        """
        Either receive a message from an existing exchange, or create a new exchange connection and receive a message from it.
        """

        if not self._in_channels.get(exchange):
            if not queue_suffix:
                raise Exception(
                    "Must provide a queue suffix when receiving a message from an exchange for the first time"
                )

            self._in_channels[exchange] = consumer(
                message_queue=queue.Queue(),
                routing_key=self.routing_key,
                exchange=exchange,
                configuration=self._credentials,
                log_file=self._logfile,
                log_level=self._log_level,
                queue_suffix=queue_suffix,
                exchange_type=exchange_type,
            )
            self._in_channels[exchange].start()

        try:
            message = self._in_channels[exchange]._message_queue.get(
                block=block, timeout=timeout
            )
            if self.auto_ack:
                # Only ack a message when it is pulled out of the thread-safe queue and auto_ack is set
                self._in_channels[exchange]._acknowledge_message(
                    message.basic_deliver.delivery_tag
                )
            return message
        except queue.Empty:
            return None

    def receive_batch(self, exchange, queue_suffix=False, exchange_type="fanout"):
        """
        Either receive all messages available from an existing exchange, or create a new exchange connection and receive all messages available from it.
        """

        if not self._in_channels.get(exchange):
            if not queue_suffix:
                raise Exception(
                    "Must provide a queue suffix when receiving a message from an exchange for the first time"
                )

            self._in_channels[exchange] = consumer(
                message_queue=queue.Queue(),
                routing_key=self.routing_key,
                exchange=exchange,
                configuration=self._credentials,
                log_file=self._logfile,
                log_level=self._log_level,
                queue_suffix=queue_suffix,
                exchange_type=exchange_type,
            )
            self._in_channels[exchange].start()

        messages = []

        # This seems like a terrible idea, but it works
        while True:
            try:
                # Block false returns Queue.Empty no matter what, why does Queue have this arg????????
                message = self._in_channels[exchange]._message_queue.get(
                    block=True, timeout=1
                )
                if self.auto_ack:
                    self._in_channels[exchange]._acknowledge_message(
                        message.basic_deliver.delivery_tag
                    )
                messages.append(message)
            except queue.Empty:
                break

        return messages
    
    def acknowledge_message(self, message):
        """
        Acknowledge a message manually. Not necessary by default where auto_acknowledge is set to True.
        """

        self._in_channels[message.basic_deliver.exchange]._acknowledge_message(
            message.basic_deliver.delivery_tag
        )

    def acknowledge_message(self, message):
        """
        Acknowledge a message manually. Not necessary by default where auto_acknowledge is set to True.
        """

        # maybe break this one-liner up differently
        (self
         ._in_channels[message.basic_deliver.exchange]
         ._acknowledge_message(message.basic_deliver.delivery_tag)
        )

    def nack_message(self, message, requeue=True):
        """
        Nack a message manually. Can be used to requeue a message if auto_acknowledge is set to False.

        """

        if self.auto_ack:
            raise Exception(
                "Cannot nack a message when auto_acknowledge is set to True"
            )

        self._in_channels[message.basic_deliver.exchange]._nack_message(
            delivery_tag=message.basic_deliver.delivery_tag, requeue=requeue
        )

    def get_channels(self):
        """Return all open channels."""

        return {
            "consumer_channels": self._in_channels.keys(),
            "producer_channels": self._out_channels.keys(),
        }

    def close(self):
        """Close all open channels."""

        for channel in self._in_channels.values():
            channel.close_connection()
            channel.stop()

        for channel in self._out_channels.values():
            channel.stop()
