import logging
import time
import uuid

from tamqp.consumers.job_consumer import JobConsumer
from tamqp.consumers.models.communication_model import to_message
from tamqp.consumers.models.execute_flight_scrape_model import ExecuteFlightScrapeModel
from tamqp.consumers.models.test_model import TestMessage
from tamqp.consumers.models.test_publish_model import TestPublishMessageModel, TestPublishMessage
from tamqp.models.amqp_init import AMQPInit
from tamqp.models.rabbit_library import QueueSubscribed
from tamqp.services.amqp import AMQP
from tamqp.services.amqp_provider import AMQPProvider


class Main:

    def __init__(self):
        self.logger = logging.getLogger('main')

    def initialize_rmq(self) -> AMQP:
        params = AMQPInit(
            username="rhgckyay",
            password="fiviFVvrBYvlEf0mKVmR1TNVQPIkZd60",
            hostname="shark-01.rmq.cloudamqp.com",
            port=5672,
            virtual_host="rhgckyay",
            encryption_key="taekus_key",
            is_tls=False
            # settings.AMQP_USER,
            # settings.AMQP_PASSWORD,
            # settings.AMQP_HOST,
            # settings.AMQP_PORT,
            # settings.AMQP_VIRTUAL_HOST,
            # settings.AMQP_JWT_KEY,
            # is_tls=settings.AMQP_IS_TLS
        )
        rmq = AMQP(params)
        return rmq

    def initialize_rmq_subscriptions(self, job_consumer: JobConsumer, rmq: AMQP) -> AMQPProvider:
        rmq.subscriptions = [
            QueueSubscribed(TestMessage.queue_name, callback=job_consumer.handle_scrape_flight(rmq))
        ]
        rmq.subscribe()
        return rmq

    def initialize_rmq_publisher(self, rmq: AMQP) -> None:
        try:
            self.logger.info("AMQP publisher has been started successfully")
        except Exception as e:
            self.logger.error("Unable to start AMQP publisher", e)

    def main(self):
        rmq = self.initialize_rmq()
        job_consumer = JobConsumer()

        x = ExecuteFlightScrapeModel(
            job_id=str(uuid.uuid4()),
            departure_airport="SFO",
            arrival_airport="CDG",
            date="2023-07-30"
        )

        print("Base model: ", x)
        print("Converted model: ", to_message(x))

        y = TestPublishMessageModel(job_id=str(uuid.uuid4()), message="testing this, hope it works")

        print("\nTesting publishing now:\n")
        rmq.publish(TestPublishMessage.queue_name, to_message(y))

        print("\nDone publishing now:\n")

        self.initialize_rmq_publisher(rmq)
        self.initialize_rmq_subscriptions(job_consumer, rmq)
        time.sleep(1)


if __name__ == "__main__":
    main = Main()
    main.main()
