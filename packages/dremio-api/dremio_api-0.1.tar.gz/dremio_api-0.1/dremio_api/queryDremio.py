import logging
from pyarrow import flight
from functools import reduce
from http.cookies import SimpleCookie
from pandas import DataFrame, concat
import certifi


class DremioClientAuthMiddlewareFactory(flight.ClientMiddlewareFactory):
    """A factory that creates DremioClientAuthMiddleware(s)."""

    def __init__(self):
        self.call_credential = []

    def start_call(self, info):
        return DremioClientAuthMiddleware(self)

    def set_call_credential(self, call_credential):
        self.call_credential = call_credential


class DremioClientAuthMiddleware(flight.ClientMiddleware):
    """
    A ClientMiddleware that extracts the bearer token from
    the authorization header returned by the Dremio
    Flight Server Endpoint.
    Parameters
    ----------
    factory : ClientHeaderAuthMiddlewareFactory
        The factory to set call credentials if an
        authorization header with bearer token is
        returned by the Dremio server.
    """

    def __init__(self, factory):
        self.factory = factory

    def received_headers(self, headers):
        auth_header_key = "authorization"
        authorization_header = reduce(
            lambda result, header: header[1]
            if header[0] == auth_header_key
            else result,
            headers.items(),
        )
        if not authorization_header:
            raise Exception("Did not receive authorization header back from server.")
        bearer_token = authorization_header[1][0]
        self.factory.set_call_credential(
            [b"authorization", bearer_token.encode("utf-8")]
        )


class CookieMiddlewareFactory(flight.ClientMiddlewareFactory):
    """A factory that creates CookieMiddleware(s)."""

    def __init__(self):
        self.cookies = {}

    def start_call(self, info):
        return CookieMiddleware(self)


class CookieMiddleware(flight.ClientMiddleware):
    """
    A ClientMiddleware that receives and retransmits cookies.
    For simplicity, this does not auto-expire cookies.
    Parameters
    ----------
    factory : CookieMiddlewareFactory
        The factory containing the currently cached cookies.
    """

    def __init__(self, factory):
        self.factory = factory

    def received_headers(self, headers):
        for key in headers:
            if key.lower() == "set-cookie":
                cookie = SimpleCookie()
                for item in headers.get(key):
                    cookie.load(item)

                self.factory.cookies.update(cookie.items())

    def sending_headers(self):
        if self.factory.cookies:
            cookie_string = "; ".join(
                f"{key}={val.value}" for (key, val) in self.factory.cookies.items()
            )
            return {b"cookie": cookie_string.encode("utf-8")}
        return {}


logging.basicConfig(level=logging.INFO)


class DremioFlightEndpointConnection:
    def __init__(self, connection_args: dict) -> None:
        self.hostname = connection_args.get("hostname")
        self.port = connection_args.get("port")
        self.username = connection_args.get("username")
        self.password = connection_args.get("password")
        self.token = connection_args.get("token")
        self.tls = connection_args.get("tls")
        self.disable_certificate_verification = connection_args.get(
            "disable_certificate_verification"
        )
        self.path_to_certs = connection_args.get("path_to_certs")
        self.session_properties = connection_args.get("session_properties")
        self.engine = connection_args.get("engine")
        self._set_headers()

    def connect(self) -> flight.FlightClient:
        """Connects to Dremio Flight server endpoint with the
        provided credentials."""
        try:
            # Default to use an unencrypted TCP connection.
            scheme = "grpc+tcp"
            client_cookie_middleware = CookieMiddlewareFactory()
            tls_args = {}

            if self.tls:
                tls_args = self._set_tls_connection_args()
                scheme = "grpc+tls"

            if self.username and (self.password or self.token):
                return self._connect_to_software(
                    tls_args, client_cookie_middleware, scheme
                )

            elif self.token:
                return self._connect_to_cloud(
                    tls_args, client_cookie_middleware, scheme
                )

            raise ConnectionError(
                "username+password or username+token or token must be supplied."
            )

        except Exception:
            logging.exception(
                "There was an error trying to connect to the Dremio Flight Endpoint"
            )
            raise

    def _connect_to_cloud(
        self,
        tls_args: dict,
        client_cookie_middleware: CookieMiddlewareFactory,
        scheme: str,
    ) -> flight.FlightClient:
        client = flight.FlightClient(
            f"{scheme}://{self.hostname}:{self.port}",
            middleware=[client_cookie_middleware],
            **tls_args,
        )

        self.headers.append((b"authorization", f"Bearer {self.token}".encode("utf-8")))
        logging.info("Authentication skipped until first request")
        return client

    def _connect_to_software(
        self,
        tls_args: dict,
        client_cookie_middleware: CookieMiddlewareFactory,
        scheme: str,
    ) -> flight.FlightClient:
        client_auth_middleware = DremioClientAuthMiddlewareFactory()
        client = flight.FlightClient(
            f"{scheme}://{self.hostname}:{self.port}",
            middleware=[client_auth_middleware, client_cookie_middleware],
            **tls_args,
        )

        # Authenticate with the server endpoint.
        password_or_token = self.password if self.password else self.token
        bearer_token = client.authenticate_basic_token(
            self.username,
            password_or_token,
            flight.FlightCallOptions(headers=self.headers),
        )
        logging.info("Authentication was successful")
        self.headers.append(bearer_token)
        return client

    def _set_tls_connection_args(self) -> dict:
        # Connect to the server endpoint with an encrypted TLS connection.
        logging.debug(" Enabling TLS connection")
        tls_args = {}

        if self.disable_certificate_verification:
            # Connect to the server endpoint with server verification disabled.
            logging.info("Disable TLS server verification.")
            tls_args[
                "disable_server_verification"
            ] = self.disable_certificate_verification

        elif self.path_to_certs:
            logging.info("Trusted certificates provided")
            # TLS certificates are provided in a list of connection arguments.
            with open(self.path_to_certs, "rb") as root_certs:
                tls_args["tls_root_certs"] = root_certs.read()
        else:
            raise Exception(
                "Trusted certificates must be provided to establish a TLS connection"
            )

        return tls_args

    def _set_headers(self) -> list:
        self.headers = self.session_properties
        if not self.headers:
            self.headers = []

        if self.engine:
            self.headers.append((b"routing_engine", self.engine.encode("utf-8")))

        # Two WLM settings can be provided upon initial authentication with the Dremio Server Flight Endpoint:
        # routing_tag
        # routing_queue
        self.headers.append((b"routing_tag", b"test-routing-tag"))
        self.headers.append((b"routing_queue", b"Low Cost User Queries"))


class DremioFlightEndpoint:
    def __init__(self, connection_args: dict) -> None:
        self.connection_args = connection_args
        self.dremio_flight_conn = DremioFlightEndpointConnection(self.connection_args)

    def connect(self) -> flight.FlightClient:
        return self.dremio_flight_conn.connect()

    def execute_query(self, flight_client: flight.FlightClient) -> DataFrame:
        dremio_flight_query = DremioFlightEndpointQuery(
            self.connection_args.get("query"), flight_client, self.dremio_flight_conn
        )
        return dremio_flight_query.execute_query()


class DremioFlightEndpointQuery:
    def __init__(
        self,
        query: str,
        client: flight.FlightClient,
        connection: DremioFlightEndpointConnection,
    ) -> None:
        self.query = query
        self.client = client
        self.headers = getattr(connection, "headers")

    def execute_query(self) -> DataFrame:
        try:
            options = flight.FlightCallOptions(headers=self.headers)
            # Get the FlightInfo message to retrieve the Ticket corresponding
            # to the query result set.
            flight_info = self.client.get_flight_info(
                flight.FlightDescriptor.for_command(self.query), options
            )
            logging.info("GetFlightInfo was successful")
            logging.debug("Ticket: %s", flight_info.endpoints[0].ticket)

            # Retrieve the result set as pandas DataFrame
            reader = self.client.do_get(flight_info.endpoints[0].ticket, options)
            return self._get_chunks(reader)

        except Exception:
            logging.exception(
                "There was an error trying to get the data from the flight endpoint"
            )
            raise

    def _get_chunks(self, reader: flight.FlightStreamReader) -> DataFrame:
        dataframe = DataFrame()
        while True:
            try:
                flight_batch = reader.read_chunk()
                record_batch = flight_batch.data
                data_to_pandas = record_batch.to_pandas()
                dataframe = concat([dataframe, data_to_pandas])
            except StopIteration:
                break

        return dataframe


def run_query(query, token):
    """Run a query against the Dremio Flight endpoint."""
    config = {
        "default": {
            "hostname": "data.dremio.cloud",
            "token": "<token>",
            "port": 443,
            "tls": True,
            "disable_certificate_verification": False,
            "path_to_certs": certifi.where(),
            # "session_properties": [(b"my_property", b"my_value")],
            # "engine": "preview",
            "query": 'SELECT * FROM "@klemen.strojan@gmail.com"."sifrant_drzave"."sifrant_drzave_clean"',
        }
    }
    config["default"]["query"] = query
    config["default"]["token"] = token
    args = config["default"]
    dremio_flight_endpoint = DremioFlightEndpoint(args)
    flight_client = dremio_flight_endpoint.connect()
    dataframe = dremio_flight_endpoint.execute_query(flight_client)
    return dataframe
