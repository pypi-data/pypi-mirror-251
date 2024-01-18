"""PWMService integration test"""
import time
import pytest
from edgepi_rpc_client.services.pwm.client_pwm_service import ClientPWMService
from edgepi_rpc_client.services.pwm.pwm_pb_enums import PWMPins, Polarity


@pytest.fixture(name="pwm_service")
def fixture_test_pwm_service():
    """Inits new PWM service client for testing"""
    return ClientPWMService('tcp://localhost:5555')

@pytest.mark.parametrize(
    "args",
    [
        {"pwm_num": PWMPins.PWM1, "polarity": Polarity.NORMAL},
        {"pwm_num": PWMPins.PWM2, "polarity": Polarity.INVERSED},
        {"pwm_num": PWMPins.PWM1, "frequency": 1000},
        {"pwm_num": PWMPins.PWM1, "duty_cycle": 0},
    ]
)
def test_set_config(pwm_service, args):
    """Test for set_config"""
    response_init = pwm_service.init_pwm(pwm_num=args['pwm_num'])
    assert response_init == f"Successfully initialized {args['pwm_num']}."
    response_config = pwm_service.set_config(**args)
    assert response_config == "Successfully applied pwm configurations."

@pytest.mark.parametrize(
    'pwm_num',
    [
        (PWMPins.PWM1),
        (PWMPins.PWM2),
    ]
)
def test_enable(pwm_service, pwm_num):
    """Test for set_enable"""
    pwm_service.init_pwm(pwm_num)
    response = pwm_service.enable(pwm_num)
    assert response == f"Successfully enabled {pwm_num}."

@pytest.mark.parametrize(
    'pwm_num',
    [
        (PWMPins.PWM1),
        (PWMPins.PWM2),
    ]
)
def test_disable(pwm_service, pwm_num):
    """Test for set_disable"""
    pwm_service.init_pwm(pwm_num)
    response = pwm_service.disable(pwm_num)
    assert response == f"Successfully disabled {pwm_num}."

@pytest.mark.parametrize(
    'pwm_num',
    [
        (PWMPins.PWM1),
        (PWMPins.PWM2),
    ]
)
def test_close(pwm_service, pwm_num):
    """Test for close"""
    pwm_service.init_pwm(pwm_num)
    response = pwm_service.close(pwm_num)
    assert response == f"Successfully closed {pwm_num}."


@pytest.mark.parametrize(
    'pwm_num',
    [
        (PWMPins.PWM1),
        (PWMPins.PWM2),
    ]
)
def test_get_frequency(pwm_service, pwm_num):
    """Test for get_frequency"""
    pwm_service.init_pwm(pwm_num)
    frequency = pwm_service.get_frequency(pwm_num)
    assert isinstance(frequency, float)

@pytest.mark.parametrize(
    'pwm_num',
    [
        (PWMPins.PWM1),
        (PWMPins.PWM2),
    ]
)
def test_get_duty_cycle(pwm_service, pwm_num):
    """Test for get_duty_cycle"""
    pwm_service.init_pwm(pwm_num)
    duty_cycle = pwm_service.get_duty_cycle(pwm_num)
    assert isinstance(duty_cycle, float)

@pytest.mark.parametrize(
    'pwm_num',
    [
        (PWMPins.PWM1),
        (PWMPins.PWM2),
    ]
)
def test_get_polarity(pwm_service, pwm_num):
    """Test for get_polarity"""
    pwm_service.init_pwm(pwm_num)
    polarity = pwm_service.get_polarity(pwm_num)
    assert polarity in Polarity

@pytest.mark.parametrize(
    'pwm_num',
    [
        (PWMPins.PWM1),
        (PWMPins.PWM2),
    ]
)
def test_get_enabled(pwm_service, pwm_num):
    """Test for get_enabled"""
    pwm_service.init_pwm(pwm_num)
    enabled = pwm_service.get_enabled(pwm_num)
    assert isinstance(enabled, bool)

def test_with_edgepi(pwm_service):
    """Used for manual testing of PWM functionality."""
    pwm_service.init_pwm(pwm_num=PWMPins.PWM2)
    pwm_service.set_config(pwm_num=PWMPins.PWM2, polarity=Polarity.NORMAL)
    pwm_service.enable(PWMPins.PWM2)
    time.sleep(3)
    pwm_service.set_config(pwm_num=PWMPins.PWM2, polarity=Polarity.INVERSED)
    time.sleep(3)
    pwm_service.set_config(pwm_num=PWMPins.PWM2, polarity=Polarity.NORMAL)
    