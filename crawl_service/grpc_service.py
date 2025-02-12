from concurrent import futures

import grpc

from crawl_service import crawl_service_pb2_grpc
from crawl_service.crawl_service_impl import CrawlServiceImpl
from crawl_service.util.config import Config


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=Config.get("service.grpc.worker", 10)))
    crawl_service_pb2_grpc.add_CrawlServiceServicer_to_server(CrawlServiceImpl(), server)
    host = Config.get("service.grpc.host", '0.0.0.0')
    port = Config.get("service.grpc.port", 50051)
    server.add_insecure_port(f'{host}:{port}')
    server.start()
    print(f'grpc crawl service is serving on {host}:{port}')
    server.wait_for_termination()
