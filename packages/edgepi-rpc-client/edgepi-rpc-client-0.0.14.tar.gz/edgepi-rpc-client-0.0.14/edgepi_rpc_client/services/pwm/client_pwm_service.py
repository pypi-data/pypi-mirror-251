"""Client for PWM service"""
import logging
from rpc_generated_protobufs import pwm_pb2 as pwm_pb
from edgepi_rpc_client.client_rpc_channel import ClientRpcChannel
from edgepi_rpc_client.util.helpers import (
    filter_arg_values,
    create_config_request_from_args,
    get_server_response,
)
from edgepi_rpc_client.services.pwm.pwm_pb_enums import PWMPins, Polarity

_logger = logging.getLogger(__name__)


# pylint: disable=no-member
class ClientPWMService:
    """Client Methods for PWM Service"""

    def __init__(self, transport):
        self.client_rpc_channel = ClientRpcChannel(transport)
        self.service_stub = pwm_pb.PWMService_Stub(self.client_rpc_channel)
        self.rpc_controller = None

    # pylint: disable=unused-argument
    def set_config(
        self,
        pwm_num: PWMPins,
        frequency: float = None,
        duty_cycle: float = None,
        polarity: Polarity = None,
    ):
        """set_config method for SDK PWM module"""
        config_args_dict = filter_arg_values(locals(), "self", None)
        config_msg = pwm_pb.Config()
        arg_msg = pwm_pb.Config().ConfArg()
        request = create_config_request_from_args(config_msg, arg_msg, config_args_dict)
        return self.perform_call_from_request(
            request, self.service_stub.set_config, pwm_pb.SuccessMsg
        ).content

    def enable(self, pwm_num: PWMPins):
        """enable method for SDK PWM module"""
        return self.perform_rpc_call(
            pwm_num, self.service_stub.enable, pwm_pb.SuccessMsg
        ).content

    def disable(self, pwm_num: PWMPins):
        """disable method for SDK PWM module"""
        return self.perform_rpc_call(
            pwm_num, self.service_stub.disable, pwm_pb.SuccessMsg
        ).content

    def close(self, pwm_num: PWMPins):
        """close method for SDK PWM module"""
        return self.perform_rpc_call(
            pwm_num, self.service_stub.close, pwm_pb.SuccessMsg
        ).content

    def init_pwm(self, pwm_num: PWMPins):
        """init_pwm method for SDK PWM module"""
        return self.perform_rpc_call(
            pwm_num, self.service_stub.init_pwm, pwm_pb.SuccessMsg
        ).content

    def get_frequency(self, pwm_num: PWMPins):
        """get_frequency method for SDK PWM module"""
        return self.perform_rpc_call(
            pwm_num, self.service_stub.get_frequency, pwm_pb.GetFrequency
        ).frequency

    def get_duty_cycle(self, pwm_num: PWMPins):
        """get_duty_cycle method for SDK PWM module"""
        return self.perform_rpc_call(
            pwm_num, self.service_stub.get_duty_cycle, pwm_pb.GetDutyCycle
        ).duty_cycle

    def get_polarity(self, pwm_num: PWMPins):
        """get_polarity method for SDK PWM module"""
        polarity = self.perform_rpc_call(
            pwm_num, self.service_stub.get_polarity, pwm_pb.GetPolarity
        ).polarity
        return Polarity(polarity)

    def get_enabled(self, pwm_num: PWMPins):
        """get_enabled method for SDK PWM module"""
        return self.perform_rpc_call(
            pwm_num, self.service_stub.get_enabled, pwm_pb.GetEnabled
        ).enabled

    # TODO: Potentially these helpers in other services and put them in a separate file
    def perform_rpc_call(self, pwm_num, method, response_type):
        """Performs RPC call with PWM number and specified method"""
        request = pwm_pb.PWM(pwm_num=pwm_num.value)
        return self.perform_call_from_request(request, method, response_type)

    def perform_call_from_request(self, request, method, response_type):
        """Executes RPC call using provided request and method"""
        rpc_response = method(self.rpc_controller, request)
        return get_server_response(rpc_response, response_type)
